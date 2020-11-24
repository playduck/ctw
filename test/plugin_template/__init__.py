import numpy as np
import pandas as pd


# called once as soon as the plugin is imported
def init_hook(args) -> None:
    print(">>> Plugin Init")

# called after Data has been read and tagged
def read_hook(args, dataframe: pd.DataFrame) -> pd.DataFrame:
    print(">>> Plugin Read Hook")
    return dataframe

# called after Data has been modified
def modify_hook(args, dataframe: pd.DataFrame) -> pd.DataFrame:
    print(">>> Plugin Modify Hook")
    return dataframe

# called after Data has been scaled
def scale_hook(args, dataframe: pd.DataFrame) -> pd.DataFrame:
    print(">>> Plugin Scale Hook")
    return dataframe

# called after Data has been saved
def save_hook(args, dataframe: pd.DataFrame) -> None:
    print(">>> Plugin Save Hook")
