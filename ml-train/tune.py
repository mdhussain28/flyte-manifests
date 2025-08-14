from flytekit import task
import optuna
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from src.core.core import generate_synthetic_data
from typing import NamedTuple

class HyperParams(NamedTuple):  # Define structured output
    lr: float
    hidden_size: int

@task(container_image="eyesoncloud/ml-train:v1", requests=Resources(cpu="1", mem="2Gi"), limits=Resources(cpu="1", mem="3Gi"))
def tune_hyperparameters(n_trials: int = 20) -> HyperParams:  # Change return type to HyperParams
    X, y = generate_synthetic_data()
    X_tensor = torch.FloatTensor(X.values)
    y_tensor = torch.LongTensor(y)

    def objective(trial):
        lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
        hidden_size = trial.suggest_int("hidden_size", 32, 128)

        model = nn.Sequential(
            nn.Linear(X.shape[1], hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 2)
        )
        optimizer = optim.Adam(model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()
        dataset = TensorDataset(X_tensor, y_tensor)
        loader = DataLoader(dataset, batch_size=32, shuffle=True)

        for epoch in range(10):
            for data, target in loader:
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
            trial.report(loss.item(), epoch)
            if trial.should_prune():
                raise optuna.TrialPruned()

        model.eval()
        with torch.no_grad():
            outputs = model(X_tensor)
            _, predicted = torch.max(outputs, 1)
            accuracy = (predicted == y_tensor).float().mean().item()
        return accuracy

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)
    best_params = study.best_params
    return HyperParams(lr=best_params["lr"], hidden_size=best_params["hidden_size"])  # Return structured instance
