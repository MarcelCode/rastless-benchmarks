import os
import pandas as pd
from typing import List
from settings import Settings


def read_result(path: str, columns: List = None) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.index = df['Timestamp'].diff().fillna(0).cumsum()
    df.index.name = "Elapsed Time [s]"
    df.drop(columns=["Timestamp", "Type", "Name"], inplace=True)

    if columns:
        df = df[columns]

    return df


def combine_result(system_dfs: dict,
                   column: str) -> pd.DataFrame:
    system_series = []
    for name, df in system_dfs.items():
        series = df[column]
        series.name = name
        system_series.append(series)

    df = pd.concat(system_series, axis=1)
    df.name = column

    return df


def stat_aggregate_dfs(dataframes: List[pd.DataFrame], stat_func="median") -> pd.DataFrame:
    df = pd.concat(dataframes)
    return getattr(df.groupby(df.index), stat_func)()


def read_stat_history_date(environment, test_type, user, spawn_rate, runtime, iso_date, layers=None):
    dfs = dict()

    for system in ["rastless", "rasdaman-proxy", "rasdaman-local"]:
        try:
            folder_path = os.path.join(Settings.base_dir,
                                       f"benchmark_results/{environment}/{system}/{test_type}/user_{user}_spawn-rate_{spawn_rate}_runtime_{runtime}")

            if layers:
                folder_path += f"_layers_{layers}"

            filename = f"test_{iso_date}_stats_history.csv"

            dfs[system] = read_result(os.path.join(folder_path, filename))
        except:
            continue

    return dfs


def read_stat_history_dates_combined(environment, test_type, user, spawn_rate, runtime, combine_method="median",
                                     layers=None):
    dfs = dict()

    for system in ["rastless", "rasdaman-proxy", "rasdaman-local"]:
        try:
            folder_path = os.path.join(Settings.base_dir,
                                       f"benchmark_results/{environment}/{system}/{test_type}/user_{user}_spawn-rate_{spawn_rate}_runtime_{runtime}")
            if layers:
                folder_path += f"_layers_{layers}"

            file_paths = [os.path.join(folder_path, x) for x in os.listdir(folder_path) if x.endswith("stats_history.csv")]
            date_dfs = [read_result(path) for path in file_paths]
            dfs[system] = stat_aggregate_dfs(date_dfs, combine_method)
        except:
            continue

    return dfs


def create_pdf_filename(folder, filename, metadata):
    info = "_".join([str(x) for x in metadata.values()])
    return os.path.join(folder, f"{filename}_{info}.pdf")


if __name__ == '__main__':
    test_setup = {"user": 25, "spawn_rate": 1, "runtime": "31s", "test_type": "visualization", "environment": "local",
                  "combine_method": "median"}
    print(create_pdf_filename("./result_images", "user_count", test_setup))
