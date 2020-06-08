from pre_process.pre_process import pre_process
from graphs_of_income_impact.graphs_of_income_impact import draw_graphs
import os

print("__________________________pre_process_____________________________")
pre_process(os.getcwd())
print("__________________________graphs_of_income_impact_____________________________")
draw_graphs(os.getcwd())
