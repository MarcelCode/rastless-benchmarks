import pandas as pd
from typing import List


def read_result(path: str, columns: List = None) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.index = df['Timestamp'].diff().fillna(0).cumsum()
    df.index.name = "Elapsed Time [s]"
    df.drop(columns=["Timestamp", "Type", "Name"], inplace=True)

    if columns:
        df = df[columns]

    return df


def combine_result(rastless: pd.DataFrame, rasdaman_proxy: pd.DataFrame, rasdaman_local: pd.DataFrame,
                   column: str) -> pd.DataFrame:
    rastless_series = rastless[column]
    rastless_series.name = "RastLess"

    rasdaman_proxy_series = rasdaman_proxy[column]
    rasdaman_proxy_series.name = "Rasdaman Proxy"

    rasdaman_local_series = rasdaman_local[column]
    rasdaman_local_series.name = "Rasdaman Local"

    df = pd.concat([rastless_series, rasdaman_proxy_series, rasdaman_local_series], axis=1)
    df.name = column

    return df


def stat_aggregate_dfs(dataframes: List[pd.DataFrame], stat_func="median") -> pd.DataFrame:
    df = pd.concat(dataframes)
    return getattr(df.groupby(df.index), stat_func)()

