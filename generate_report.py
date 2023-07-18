import pandas as pd
import json
import os
import argparse
import numpy as np
import csv


def flatten_dict(d, prefix=''):
    flat_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            flat_dict.update(flatten_dict(v, f'{prefix}{k}-'))
        else:
            flat_dict[f'{prefix}{k}'] = v
    return flat_dict


with open('indices_old.json', 'r') as f:
    old_data = json.load(f)
    old_data = {k: flatten_dict(v) for k, v in old_data.items()}

with open('indices_new.json', 'r') as f:
    new_data = json.load(f)
    new_data = {k: flatten_dict(v) for k, v in new_data.items()}

old_data_rt = {k: v for k, v in old_data.items() if k.split('_')[-1] not in ["LDN", 'NYC', "SGP"] and k.startswith("KK")}
old_data_fx = {k: v for k, v in old_data.items() if k.split('_')[-1] in ["LDN", 'NYC', "SGP"] and k.startswith("KK")}
new_data_rt = {k: v for k, v in new_data.items() if k.split('_')[-1] not in ["LDN", 'NYC', "SGP"] and k.startswith("KK")}
new_data_fx = {k: v for k, v in new_data.items() if k.split('_')[-1] in ["LDN", 'NYC', "SGP"] and k.startswith("KK")}


def make_comparison(RT=True):
    if RT:
        old_file = pd.DataFrame(old_data_rt).T
        new_file = pd.DataFrame(new_data_rt).T

        diff = new_file.compare(old_file)
        # Drop the rows without any changes
        # diff.dropna(how='all', inplace=True)
        # print(diff)
        # diff.to_csv("temp_diff.csv")

        # diff = diff.dropna(how='all').groupby(level=0, axis=1).apply(
        #     lambda frame: frame.apply(
        #         lambda series: series.dropna().tolist(), axis=1
        #     )
        # ).replace({np.nan: None})
        #
        # # Name 'self' and 'other' as 'old' and 'new'
        # diff.columns = diff.columns.map('-'.join).str.replace('self', 'old').str.replace('other', 'new')
        #
        # # Adding the column 'comment'
        # diff["comment"] = "Changed values"
        #
        # # Save the differences to a new CSV
        # diff.to_csv('differences.csv')

prediction interval?


if __name__ == "__main__":
    res = make_comparison()
    # res.to_csv("temp.csv")

