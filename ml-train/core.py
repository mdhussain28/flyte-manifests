import numpy as np
import torch
import torch.nn as nn
import pandas as pd
import mlflow
from mlflow.models import infer_signature
mlflow.set_tracking_uri("http://192.168.100.11:30050")

class SimpleNet(nn.Module):
    def __init__(self, input_size=12, hidden_size=64, output_size=2):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        return self.fc2(x)

def generate_synthetic_data(n_samples=1000, n_features=12, seed=42):
    np.random.seed(seed)
    torch.manual_seed(seed)
    X = np.random.rand(n_samples, n_features)
    y = (X.sum(axis=1) > n_features / 2).astype(int)
    return pd.DataFrame(X, columns=[f"feat_{i}" for i in range(n_features)]), y

def save_model(model, path, params, metrics, example_input=None):
    """Save model with MLflow and return run ID."""
    with mlflow.start_run() as run:
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

        # Handle example input
        if example_input is None:
            example_input = np.random.rand(1, 12).astype(np.float32)  # default dummy input
        else:
            if isinstance(example_input, np.ndarray):
                example_input = example_input.astype(np.float32)
            elif isinstance(example_input, torch.Tensor):
                example_input = example_input.detach().cpu().numpy().astype(np.float32)
            else:
                raise ValueError("example_input must be a numpy array or torch tensor")

        # Generate output for signature
        output = model(torch.FloatTensor(example_input)).detach().numpy()
        signature = infer_signature(example_input, output)

        mlflow.pytorch.log_model(
            model,
            name=path,
            input_example=example_input,
            signature=signature
        )
        return run.info.run_id
