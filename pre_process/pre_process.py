import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os

names = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'post',
         'relationship', 'nation', 'gender', 'capital_gain', 'capital_loss', 'hours_per_week',
         'country',
         'wealth']
names_for_converted_quantitative_data_to_qualitative_dict_ad_outliers = list(set(names) - {'wealth'})
converted_quantitative_data_to_qualitative_dict = {}


def read_file():
    project_path = os.path.join("/", *(str(os.getcwd()).split("/")[0:-1]))
    data_path = os.path.join(project_path, "fout.csv")
    df = pd.read_csv(str(data_path),
                     names=names)

    # df = pd.read_csv(str(data_path))
    return df


def remove_missing_value(df):
    df = df.replace(' ?', np.NaN)
    df.dropna(inplace=True)
    df.to_csv("deletedMissingValue.csv")
    return df


def draw_box_plot(df):
    for name in names_for_converted_quantitative_data_to_qualitative_dict_ad_outliers:
        plt.boxplot(df[name])
        plt.savefig(name + ".png")


def convert_quantitative_data_to_qualitative(data):
    for name in names_for_converted_quantitative_data_to_qualitative_dict_ad_outliers:
        column = data[name]
        if column.dtype != "int64":
            distinct_elements = column.drop_duplicates()
            separation_length = 100 / (len(distinct_elements) + 1)
            for i, elem in enumerate(distinct_elements):
                b = separation_length * (i + 1)
                data = data.replace(str(elem), b)
                if name not in converted_quantitative_data_to_qualitative_dict:
                    converted_quantitative_data_to_qualitative_dict[name] = {b: str(elem)}
                else:
                    converted_quantitative_data_to_qualitative_dict[name].update({b: str(elem)})

    return data


def remove_outliers_by_column(df, name):
    column = df[name]
    quantile1, quantile3 = np.percentile(column, [25, 75])
    iqr = quantile3 - quantile1
    lower_bound_val = quantile1
    upper_bound_val = quantile3
    for i in range(len(df)):
        # a = column[i]
        if i in df.index:
            if column[i] < lower_bound_val or column[i] > upper_bound_val:
                df = df.drop(i)
    return df


def remove_outliers(df):
    for name in names_for_converted_quantitative_data_to_qualitative_dict_ad_outliers:
        print(name)
        df = remove_outliers_by_column(df, name)
        print(remove_outliers_by_column(df, name).head())
        print("___________________________________________")
        print(len(df))
        print("*******************************************")
    df.to_csv("removed_outliers_data.csv")
    return df


print("____________________read_file_______________________________")
df = read_file()
print(len(df))

print("____________________remove_missing_value_______________________________")
df = remove_missing_value(read_file())
print(len(df))

print("____________________convert_quantitative_data_to_qualitative_______________________________")
df = convert_quantitative_data_to_qualitative(df)

print("____________________draw_box_plot______________________________")
draw_box_plot(df)

print("____________________remove_outliers______________________________")
remove_outliers(df)
