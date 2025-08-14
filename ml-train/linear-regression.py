from flytekit import workflow, Resources
import pandas as pd
from src.tasks.data import load_data
from src.tasks.train import train_model
from src.tasks.predict import predict
from src.orchestration.tune import tune_hyperparameters

@workflow(container_image="eyesoncloud/ml-train:v1", requests=Resources(cpu="1", mem="2Gi"), limits=Resources(cpu="1", mem="3Gi"))
def ml_workflow(n_samples: int = 1000, n_features: int = 12) -> pd.DataFrame:
    best_params = tune_hyperparameters(n_trials=20)
    X, y = load_data(n_samples=n_samples, n_features=n_features)
    model_path = train_model(X=X, y=y, lr=best_params.lr, hidden_size=best_params.hidden_size)  # Use .lr and .hidden_size
    predictions = predict(model_path=model_path, input_data=X)
    return predictions
