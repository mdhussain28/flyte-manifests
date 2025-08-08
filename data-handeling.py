from flytekit import task, workflow, FlyteFile, container_image
from flytekit.types.structured import StructuredDataset
import pandas as pd

@task(container_image="eyesoncloud/python-flyte")
def upload_raw_csv() -> FlyteFile:
    """Creates a CSV file locally and uploads it as FlyteFile."""
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Carol"],
        "sales": [1200, 1500, 1300]
    })
    filepath = "/tmp/sales.csv"
    df.to_csv(filepath, index=False)
    return FlyteFile(filepath)  # Implicit upload to remote storage

@task(container_image="eyesoncloud/python-flyte")
def summarize_sales(file: FlyteFile) -> int:
    """
    Demonstrates explicit download of FlyteFile.
    file.download() → Downloads to local temp file, returns local path.
    """
    local_path = file.download()
    df = pd.read_csv(local_path)
    return int(df["sales"].sum())

@task(container_image="eyesoncloud/python-flyte")
def create_parquet_dataset() -> StructuredDataset:
    """Creates a Parquet StructuredDataset (implicit upload)."""
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "score": [85, 92, 78]
    })
    return StructuredDataset(dataframe=df)  # Implicit upload
  
@task(container_image="eyesoncloud/python-flyte")
def avg_score(ds: StructuredDataset) -> float:
    """
    Demonstrates implicit read of StructuredDataset.
    ds.open(pd.DataFrame).all() → Reads directly without manual download.
    """
    df = ds.open(pd.DataFrame).all()
    return float(df["score"].mean())

@workflow
def combined_data_wf() -> (int, float):
    # FlyteFile part
    file = upload_raw_csv()
    total_sales = summarize_sales(file=file)
    # StructuredDataset part
    ds = create_parquet_dataset()
    average_score = avg_score(ds=ds)
    return total_sales, average_score
