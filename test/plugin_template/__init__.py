import numpy as np
import pandas as pd
import logging
import argparse


def init_hook(log: logging, args: argparse.Namespace) -> None:
# called once as soon as the plugin is imported
    log.info(">>> Plugin Init")

def read_hook(log: logging, args: argparse.Namespace,
              dataframe: pd.DataFrame) -> pd.DataFrame:
# called after Data has been read and tagged
    log.info(">>> Plugin Read Hook")
    return dataframe

def modify_hook(log: logging, args: argparse.Namespace,
                dataframe: pd.DataFrame) -> pd.DataFrame:
# called after Data has been modified
    log.info(">>> Plugin Modify Hook")
    return dataframe

def scale_hook(log: logging, args: argparse.Namespace,
               dataframe: pd.DataFrame) -> pd.DataFrame:
# called after Data has been scaled
    log.info(">>> Plugin Scale Hook")
    return dataframe

def save_hook(log: logging, args: argparse.Namespace,
              dataframe: pd.DataFrame) -> None:
# called after Data has been saved
    log.info(">>> Plugin Save Hook")
