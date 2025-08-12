from flytekit import task
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
from torch.nn.parallel import DistributedDataParallel as DDP
from src.core.core import generate_synthetic_data
import os

@task
def distributed_train(rank: int, world_size: int, lr: float = 0.01, hidden_size: int = 64) -> str:
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "12355"
    dist.init_process_group("gloo", rank=rank, world_size=world_size)

    X, y = generate_synthetic_data()
    X_tensor = torch.FloatTensor(X.values)
    y_tensor = torch.LongTensor(y)
    dataset = torch.utils.data.TensorDataset(X_tensor, y_tensor)
    sampler = torch.utils.data.distributed.DistributedSampler(dataset)
    loader = torch.utils.data.DataLoader(dataset, batch_size=32, sampler=sampler)

    model = nn.Sequential(
        nn.Linear(X.shape[1], hidden_size),
        nn.ReLU(),
        nn.Linear(hidden_size, 2)
    )
    model = DDP(model)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(10):
        for data, target in loader:
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

    if rank == 0:
        from src.core.core import save_model
        model_path = f"model_distributed_{rank}"
        save_model(model.module, model_path, {"lr": lr, "hidden_size": hidden_size}, {"epoch": epoch})
        dist.destroy_process_group()
        return model_path
    dist.destroy_process_group()
    return ""
