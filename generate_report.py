import pandas as pd
import json
import argparse


def flatten_dict(d, prefix=''):
    flat_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            flat_dict.update(flatten_dict(v, f'{prefix}{k}-'))
        else:
            flat_dict[f'{prefix}{k}'] = v
    return flat_dict


def make_comparison(old_data_file, new_data_file, RT=True):
    with open(old_data_file, 'r') as f:
        old_data = json.load(f)
        old_data = {k: flatten_dict(v) for k, v in old_data.items()}

    with open(new_data_file, 'r') as f:
        new_data = json.load(f)
        new_data = {k: flatten_dict(v) for k, v in new_data.items()}

    old_data_rt = {k: v for k, v in old_data.items() if k.split('_')[-1] not in ["LDN", 'NYC', "SGP"] and k.startswith("KK")}
    old_data_fx = {k: v for k, v in old_data.items() if k.split('_')[-1] in ["LDN", 'NYC', "SGP"] and k.startswith("KK")}
    new_data_rt = {k: v for k, v in new_data.items() if k.split('_')[-1] not in ["LDN", 'NYC', "SGP"] and k.startswith("KK")}
    new_data_fx = {k: v for k, v in new_data.items() if k.split('_')[-1] in ["LDN", 'NYC', "SGP"] and k.startswith("KK")}

    if RT:
        old_file = pd.DataFrame(old_data_rt).T
        new_file = pd.DataFrame(new_data_rt).T

    else:
        old_file = pd.DataFrame(old_data_fx).T
        new_file = pd.DataFrame(new_data_fx).T

    diff = new_file.compare(old_file)

    diff['Change'] = diff.apply(lambda row: ' -> '.join(str(val) for col, val in row.items() if col != 'Change' and str(val) != 'nan'), axis=1)

    diff = diff[('Change', '')]
    diff = pd.DataFrame(diff)
    diff.columns = diff.columns.droplevel(level=1)

    # sort by index
    diff = diff.sort_index()
    return diff


def run():
    RT_result = make_comparison(old_data_file, new_data_file, RT=True)
    FX_result = make_comparison(old_data_file, new_data_file, RT=False)

    # combine
    result = pd.concat([RT_result, FX_result])
    print(result)
    result.to_csv(report_name, index=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare JSON configuration files and create a report CSV.')
    parser.add_argument('-o', '--old_config', type=str, required=True, help='Path to the old config JSON file.')
    parser.add_argument('-n', '--new_config', type=str, required=True, help='Path to the new config JSON file.')
    parser.add_argument('-r', '--report_name', type=str, required=True, help='Name of the report CSV file.')
    args = parser.parse_args()

    # Retrieve the values of the command-line arguments
    old_data_file = args.old_config
    new_data_file = args.new_config
    report_name = args.report_name

    run()

