import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt

from core.vars import VARS

import os
import json

names_without_target = list(set(VARS.NAMES) - {'wealth'})


def read_file(path):
    df = pd.read_csv(path, names=VARS.NAMES)
    return df


def remove_missing_value(df, path):
    df = df.replace(' ?', np.NaN)
    df.dropna(inplace=True)
    df.to_csv(path)
    return df


def convert_qualitative_data_to_quantitative(df, names,
                                             path_for_save_converted_qualitative_data_to_quantitative_dict):
    converted_qualitative_data_to_quantitative_dict = {}
    for name in names:
        column = df[name]
        if column.dtype != "int64":
            distinct_elements = column.drop_duplicates()
            separation_length = 100 / (len(distinct_elements) + 1)
            for i, elem in enumerate(distinct_elements):
                b = separation_length * (i + 1)
                df = df.replace(str(elem), b)
                if name not in converted_qualitative_data_to_quantitative_dict:
                    converted_qualitative_data_to_quantitative_dict[name] = {b: elem}
                else:
                    converted_qualitative_data_to_quantitative_dict[name].update({b: elem})
    with open(path_for_save_converted_qualitative_data_to_quantitative_dict, 'w') as file:
        file.write(json.dumps(converted_qualitative_data_to_quantitative_dict))
    return df


def draw_box_plot(df, plots_directory):
    for name in names_without_target:
        sns.boxplot(data=df, x=df[name])
        plt.savefig(plots_directory + "/" + name + ".png")


def json_from_txt(path):
    with open(path) as json_file:
        fetched_dict = json.load(json_file)
        return fetched_dict


def back_quantitative_data_to_qualitative(df, path_for_save_converted_qualitative_data_to_quantitative_dict, path):
    converted_qualitative_data_to_quantitative_dict = json_from_txt(
        path_for_save_converted_qualitative_data_to_quantitative_dict)
    for name in converted_qualitative_data_to_quantitative_dict:
        k = converted_qualitative_data_to_quantitative_dict[name]
        df[name] = df[name].map(k)
    df.to_csv(path)


def remove_outliers_by_column(df, name):
    column = df[name]
    quantile1, quantile3 = np.percentile(column, [25, 75])
    lower_bound_val = quantile1
    upper_bound_val = quantile3
    for i in range(len(df)):
        if i in df.index:
            if column[i] < lower_bound_val or column[i] > upper_bound_val:
                df = df.drop(i)
    return df


def remove_outliers(df, path):
    for name in names_without_target:
        print(name)
        df = remove_outliers_by_column(df, name)
        print("*******************************************")
    df.to_csv(path)
    return df
