from typing import Dict
import numpy as np
import pandas as pd
from flytekit import task, workflow

# Task to generate financial data using pandas and numpy
@task(cache=True, cache_version="1.0", container_image="eyesoncloud/python-flyte")
def generate_financial_data(num_records: int) -> pd.DataFrame:
    np.random.seed(42)
    data = {
        "transaction_id": range(num_records),
        "amount": np.random.uniform(10, 1000, num_records),
        "fee": np.random.uniform(0.5, 5, num_records)
    }
    return pd.DataFrame(data)

# Task to compute summary statistics from the DataFrame
@task(container_image="eyesoncloud/python-flyte")
def compute_summary_stats(df: pd.DataFrame) -> Dict[str, str]:
    total_amount = df["amount"].sum()
    avg_fee = df["fee"].mean()
    return {
        "total_amount": str(total_amount),
        "average_fee": str(avg_fee)
    }

# Workflow that connects the two tasks
@workflow
def financial_data_workflow(num_records: int) -> Dict[str, str]:
    df = generate_financial_data(num_records=num_records)
    return compute_summary_stats(df=df)
