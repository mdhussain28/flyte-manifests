from flytekit import task
import mlflow.pytorch
import torch
import pandas as pd

@task
def predict(model_path: str, input_data: pd.DataFrame) -> pd.DataFrame:
    model = mlflow.pytorch.load_model(model_path)
    model.eval()
    X_tensor = torch.FloatTensor(input_data.values)
    with torch.no_grad():
        outputs = model(X_tensor)
        _, predicted = torch.max(outputs, 1)
    return pd.DataFrame(predicted.numpy(), columns=["prediction"])
