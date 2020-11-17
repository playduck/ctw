import numpy as np
import pandas as pd


# called once as soon as the plugin is imported
def init(args) -> None:
    print(">>> Plugin Init")

# called after Data has been read and tagged
def read_hook(args, dataframe: pd.DataFrame) -> pd.DataFrame:
    print(">>> Plugin Read Hook")
    return dataframe
