import matplotlib.pyplot as plt
import numpy as np

import random as rd

def model_scores(  scores : list[list[float]]  , legends : list[str]):
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

model_scores([
    [ rd.uniform(0, 1) for _ in range(1, 200) ],
    [ rd.uniform(0, 1) for _ in range(1, 200) ],
    [ rd.uniform(0, 1) for _ in range(1, 200) ]], ['model1', 'model2', 'model3']
)