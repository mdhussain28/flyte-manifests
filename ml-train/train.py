from flytekit import task
from src.core.core import SimpleNet, save_model
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd

@task(container_image="eyesoncloud/ml-train:v1", requests=Resources(cpu="1", mem="2Gi"), limits=Resources(cpu="1", mem="3Gi"))
def train_model(X: pd.DataFrame, y: pd.DataFrame, lr: float = 0.01, hidden_size: int = 64, epochs: int = 10) -> str:
    torch.manual_seed(42)
    X_tensor = torch.FloatTensor(X.values)
    y_tensor = torch.LongTensor(y["label"].values)
    dataset = TensorDataset(X_tensor, y_tensor)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model = SimpleNet(input_size=X.shape[1], hidden_size=hidden_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        for data, target in loader:
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        outputs = model(X_tensor)
        _, predicted = torch.max(outputs, 1)
        accuracy = (predicted == y_tensor).float().mean().item()

    run_id = save_model(
    model,
    "model_v1",
    params={"lr": lr, "hidden_size": hidden_size},
    metrics={"accuracy": accuracy},
    example_input=X_tensor[:5]  # small batch to define schema
)
    return f"runs:/{run_id}/model_v1"  # Return MLflow artifact URI
