from itertools import product
from pathlib import Path

from core.trainer import train
from utils.data import create_folder_if_not_exists

import matplotlib.pyplot as plt
import json

HYPERPARAM_GRID = {
    "lr": [0.001, 0.005],
    "epochs": [50, 100, 150, 200],
    "dropout": [0.2, 0.3, 0.4],
    "optimizer": ["rmsprop", "adam"]
}

# HYPERPARAM_GRID = {
#     "lr": [0.001],
#     "epochs": [50],
#     "dropout": [0.3],
#     "optimizer": ["rmsprop"]
# }

METRICS_OUTPUT = "output/metrics/"
METRICS_OUTPUT_FILE = "output/metrics/metrics.json"

def get_param_combos():
    keys = HYPERPARAM_GRID.keys()
    values = HYPERPARAM_GRID.values()

    return [dict(zip(keys, combo)) for combo in product(*values)]

def run_grid_search():
    create_folder_if_not_exists(METRICS_OUTPUT)
    
    configs = get_param_combos()

    results = []
    
    for i, config in enumerate(configs):
        print(f"Running config {i + 1} / {len(configs)}: {config}")
        
        metrics = train(
            epochs=config["epochs"],
            lr=config["lr"],
            dropout=config["dropout"],
            optimizer_name=config["optimizer"],
            no_plotting=True
        )

        results.append(metrics)
    
    with open(METRICS_OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=4)
        
    plot_results(results)

def plot_results(results: list):
    if not results:
        # Load saved results if args wasn't provided
        metrics_file = Path(METRICS_OUTPUT_FILE)

        if metrics_file.exists():
            with open(metrics_file, "r") as f:
                res = json.load(f)
        else:
            res = []
    else:
        res = results

    # Extract individual metrics
    rmse_values = [r["rmse"] for r in res]
    mae_values = [r["mae"] for r in res]
    val_loss_values = [r["val_loss"] for r in res]
    configs = [f"{i+1}" for i in range(len(res))]

    # Plot RMSE, MAE, and Validation Loss
    plt.figure(figsize=(10, 5))
    plt.plot(configs, rmse_values, marker="o", label="RMSE")
    plt.plot(configs, mae_values, marker="x", label="MAE")
    plt.plot(configs, val_loss_values, marker="s", label="Validation Loss")

    plt.title("Hyperparameter Tuning Results")
    plt.xlabel("Configuration #")
    plt.ylabel("Metric Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)

    plt.show()

get_param_combos()