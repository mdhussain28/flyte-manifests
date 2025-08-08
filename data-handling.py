from flytekit import task, workflow, FlyteFile, FlyteDirectory
import pandas as pd
import os
import pyarrow as pa
import pyarrow.parquet as pq

IMAGE = "eyesoncloud/python-flyte"
OUTPUT_DIR = "/tmp/output"

@task(container_image=IMAGE)
def create_sales_csv() -> FlyteFile:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Carol"],
        "sales": [1200, 1500, 1300]
    })
    sales_path = os.path.join(OUTPUT_DIR, "sales.csv")
    df.to_csv(sales_path, index=False)
    return FlyteFile(sales_path)

@task(container_image=IMAGE)
def create_scores_parquet() -> FlyteFile:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "score": [85, 92, 78]
    })
    parquet_path = os.path.join(OUTPUT_DIR, "scores.parquet")
    table = pa.Table.from_pandas(df)
    pq.write_table(table, parquet_path)
    return FlyteFile(parquet_path)

@task(container_image=IMAGE)
def process_files(sales_file: FlyteFile, scores_file: FlyteFile) -> FlyteFile:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sales_path = sales_file.download()
    scores_path = scores_file.download()

    sales_df = pd.read_csv(sales_path)
    scores_df = pq.read_table(scores_path).to_pandas()

    total_sales = int(sales_df["sales"].sum())
    avg_score = float(scores_df["score"].mean())

    output_txt_path = os.path.join(OUTPUT_DIR, "output.txt")
    with open(output_txt_path, "w") as f:
        f.write(f"Total Sales: {total_sales}\n")
        f.write(f"Average Score: {avg_score}\n")

    return FlyteFile(output_txt_path)

@task(container_image=IMAGE)
def package_directory(sales_file: FlyteFile, scores_file: FlyteFile, output_file: FlyteFile) -> FlyteDirectory:
    base_dir = OUTPUT_DIR
    subfolder = os.path.join(base_dir, "Files_Folder")
    os.makedirs(subfolder, exist_ok=True)

    sales_path = sales_file.download()
    scores_path = scores_file.download()
    output_path = output_file.download()

    os.rename(sales_path, os.path.join(subfolder, "sales.csv"))
    os.rename(scores_path, os.path.join(subfolder, "scores.parquet"))
    os.rename(output_path, os.path.join(subfolder, "output.txt"))

    # Return the base directory so the subfolder structure is preserved on upload
    return FlyteDirectory(base_dir)

@task(container_image=IMAGE)
def read_output_file(directory: FlyteDirectory) -> str:
    local_dir = directory.download()
    output_file_path = os.path.join(local_dir, "Files_Folder", "output.txt")
    with open(output_file_path, "r") as f:
        content = f.read()
    return content

@workflow
def full_pipeline_wf() -> str:
    sales_file = create_sales_csv()
    scores_file = create_scores_parquet()
    output_file = process_files(sales_file, scores_file)
    directory = package_directory(sales_file, scores_file, output_file)
    output_content = read_output_file(directory)
    return output_content
