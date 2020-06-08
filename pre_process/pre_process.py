from pre_process.utils import read_file, remove_missing_value, convert_qualitative_data_to_quantitative, draw_box_plot, \
    back_quantitative_data_to_qualitative, remove_outliers, json_from_txt
from core.vars import VARS

import os
import json

NAMES = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'post',
         'relationship', 'nation', 'gender', 'capital_gain', 'capital_loss', 'hours_per_week',
         'country',
         'wealth']
converted_qualitative_data_to_quantitative_dict = {}
names_without_target = list(set(VARS.NAMES) - {'wealth'})


def pre_process(project_directory):
    pre_process_directory = os.path.join(project_directory, "pre_process")
    print("____________________read_file_______________________________")
    df = read_file(path=os.path.join(pre_process_directory, "fout.csv"))

    print("____________________remove_missing_value_______________________________")
    df = remove_missing_value(df=df, path=os.path.join(pre_process_directory, "deleted_missing_value.csv"))

    print("____________________convert_quantitative_data_to_qualitative_______________________________")
    df = convert_qualitative_data_to_quantitative(df=df, names=VARS.NAMES,
                                                  path_for_save_converted_qualitative_data_to_quantitative_dict=os.path.join(
                                                      pre_process_directory,
                                                      "converted_qualitative_data_to_quantitative_dict.txt"))

    print("____________________draw_box_plot______________________________")
    draw_box_plot(df=df, plots_directory=os.path.join(pre_process_directory, "plots"))

    print("____________________remove_outliers______________________________")
    remove_outliers(df=df, path=os.path.join(pre_process_directory, "removed_outliers_quantitative_data.csv"))

    print("____________________back_to_qualitative_______________________________")
    back_quantitative_data_to_qualitative(df=df.copy(),
                                          path_for_save_converted_qualitative_data_to_quantitative_dict=os.path.join(
                                              pre_process_directory,
                                              "converted_qualitative_data_to_quantitative_dict.txt"),
                                          path=os.path.join(pre_process_directory,
                                                            "removed_outliers_qualitative_data.csv"))
