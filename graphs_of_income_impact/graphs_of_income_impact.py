import matplotlib.pyplot as plt

from core.vars import VARS
from pre_process.utils import read_file

import os


def draw_graphs(project_directory):
    df = read_file(os.path.join(project_directory, "pre_process", "removed_outliers_quantitative_data.csv"))
    for name in VARS.NAMES[0:-1]:
        ndf = df.copy().sort_values(name)
        plt.scatter(df[name], df[VARS.NAMES[-1]])
        plt.savefig(project_directory + "/graphs_of_income_impact/" + name + ".png")
    # df.sort_values('age')

