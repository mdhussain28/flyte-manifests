from flytekit import task, Resources
from src.core.core import generate_synthetic_data
import pandas as pd

@task(container_image="eyesoncloud/ml-train:v1", requests=Resources(cpu="1", mem="2Gi"), limits=Resources(cpu="1", mem="3Gi"))
def load_data(n_samples: int = 1000, n_features: int = 12) -> tuple[pd.DataFrame, pd.DataFrame]:
    X, y = generate_synthetic_data(n_samples, n_features)
    return X, pd.DataFrame(y, columns=["label"])
