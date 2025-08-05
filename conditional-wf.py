from typing import List, Dict
import flytekit as fl
from flytekit import conditional, task, workflow

@task
def preprocess_data(dataset_size: int) -> List[float]:
    import random
    random.seed(42)
    return [random.uniform(100, 1000) for _ in range(dataset_size)]

@task
def analyze_large_dataset(sales_data: List[float], threshold: float) -> Dict[str, str]:
    total_sales = sum(sales_data)
    avg_sales = total_sales / len(sales_data)
    high_value_count = sum(1 for sale in sales_data if sale > threshold)
    return {
        "result_type": "large_dataset_analysis",
        "average_sales": str(avg_sales),
        "high_value_count": str(high_value_count)
    }

@task
def analyze_small_dataset(sales_data: List[float], threshold: float) -> Dict[str, str]:
    sorted_sales = sorted(sales_data)
    mid = len(sorted_sales) // 2
    median = (sorted_sales[mid - 1] + sorted_sales[mid]) / 2 if len(sorted_sales) % 2 == 0 else sorted_sales[mid]
    return {
        "result_type": "small_dataset_analysis",
        "median_sales": str(median)
    }

@task
def handle_invalid_dataset() -> Dict[str, str]:
    return {
        "result_type": "error",
        "error": "Dataset size must be between 1 and 10000."
    }

@workflow
def sales_analysis_workflow(dataset_size: int, threshold: float = 500.0) -> Dict[str, str]:
    return (
        conditional("sales_analysis")
        .if_(dataset_size <= 0)
        .then(handle_invalid_dataset())
        .elif_((dataset_size > 1000) & (dataset_size <= 10000))
        .then(analyze_large_dataset(sales_data=preprocess_data(dataset_size=dataset_size), threshold=threshold))
        .elif_((dataset_size >= 1) & (dataset_size <= 1000))
        .then(analyze_small_dataset(sales_data=preprocess_data(dataset_size=dataset_size), threshold=threshold))
        .else_()
        .then(handle_invalid_dataset())
    )
