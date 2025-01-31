import json

import matplotlib.pyplot as plt
import numpy as np


def model_scores(scores: list[list[float]], legends: list[str]):
    """
    Plots the scores of different models
    """
    for i in range(len(scores)):
        x = np.arange(len(scores[0]))
        scatter = plt.scatter(x, scores[i], label=legends[i])
        avg_score = float(np.mean(scores[i]))
        plt.axhline(y=avg_score, color=scatter.get_facecolor()[0], linestyle='--', label=f'{legends[i]} Promedio')
    plt.legend()
    plt.show()

def load_pipeline_json(json_path):
    with open(json_path, "r") as file:
        scores = json.load(file)
        legends = []
        score_values = []
        for key, value in scores.items():
            legends.append(f"Pipeline {key}")
            score_values.append(value)
        model_scores(score_values, legends)

load_pipeline_json("scores.json")