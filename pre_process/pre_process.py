import pandas as pd
import numpy as np
import os

names = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'post',
         'relationship', 'nation', 'gender', 'capital_gain', 'capital_loss', 'hours_per_week',
         'country',
         'wealth']

converted_quantitative_data_to_qualitative_dict = {}


def read_file():
    project_path = os.path.join("/", *(str(os.getcwd()).split("/")[0:-1]))
    data_path = os.path.join(project_path, "fout.csv")
    df = pd.read_csv(str(data_path),
                     names=names)

    # df = pd.read_csv(str(data_path))
    return df


def remove_missing_value(data):
    data = data.replace(' ?', np.NaN)
    data.dropna(inplace=True)
    return data


def remove_outliers_by_age(data):
    column = data['age']
    quantile1, quantile3 = np.percentile(column, [25, 75])
    iqr = quantile3 - quantile1
    lower_bound_val = quantile1
    upper_bound_val = quantile3
    for i in range(len(data)):
        # a = column[i]
        if i in data.index:
            if column[i] < lower_bound_val or column[i] > upper_bound_val:
                data = data.drop(i)
    return data


def remove_outliers_by_work_class(data):
    pass


#
def convert_quantitative_data_to_qualitative(data):
    for name in names:
        column = data[name]
        if column.dtype != "int64":
            distinct_elements = column.drop_duplicates()
            separation_length = 100 / (len(distinct_elements) + 1)
            for i, elem in enumerate(distinct_elements):
                b = separation_length * (i + 1)
                data = data.replace(str(elem), b)
                converted_quantitative_data_to_qualitative_dict[str(elem)] = b
    return data


print("____________________read_file_______________________________")
df = read_file()
print(len(df))
print("_____________________________________________________________")

print("____________________remove_missing_value_______________________________")
df = remove_missing_value(read_file())
print(len(df))
print("_____________________________________________________________")
print(df.head())
print("_____________________________________________________________")
print(convert_quantitative_data_to_qualitative(df).head())
print(converted_quantitative_data_to_qualitative_dict)
# print(df.head())

#
# print(df.head())
#
# print("____________________remove_outliers_by_one_column_______________________________")
# df = remove_outliers_by_age(df)
# print(len(df))

# print(remove_outliers_by_on_column(df, 'age')[1])
# for key, value in df.iteritems():
#     print(key)
#     print(value)
