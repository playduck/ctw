#!/usr/bin/env python3

import argparse
import importlib
import logging
import os
import sys
from timeit import default_timer as timer

import manipulate
import parse
# import plot
import reader
import wave_writer as wave

loglevel = {
    "none": logging.NOTSET,
    "info": logging.INFO,
    "debug": logging.DEBUG
}


def import_plugin(args) -> object:
    if (args.plugin is not None) and (
            args.plugin != []) and (os.path.exists(args.plugin)):
        # split plugin path
        plugin_path, plugin_name = os.path.split(args.plugin)

        logging.debug(
            "loading plugin at {} {}".format(
                plugin_path, plugin_name))

        # add plugins path to python search path
        sys.path.insert(0, plugin_path)
        # dynamically import plugin
        try:
            plugin = importlib.import_module(plugin_name)
        except Exception as e:
            logging.error(
                'Exception Occured while importing plugin',
                exc_info=e)
            return None

        # call plugins init
        try:
            plugin.init(args)
        except Exception as e:
            logging.error(
                'Exception Occured while calling plugin.init',
                exc_info=e)
    else:
        plugin = None
    return plugin


def main():
    start = timer()
    logging.basicConfig(format="[%(levelname)s]: %(message)s")
    args = parse.parse_args()
    logging.getLogger().setLevel(loglevel[args.loglevel])

    plugin = import_plugin(args)

    dataframe = reader.read_file(args)
    if dataframe is None:
        logging.error(
            "Dataframe could not be parsed. There probably is additional output above. Exiting")
        sys.exit(0)

    if plugin is not None:
        try:
            plugin_dataframe = plugin.read_hook(args, dataframe)
        except Exception as e:
            logging.error(
                'Exception Occured while calling plugin.read_hook',
                exc_info=e)
        finally:
            if plugin_dataframe is not None:
                dataframe = plugin_dataframe

    dataframe = manipulate.manipulate_data(args, dataframe)

    # TODO plugin hook after_modify

    dataframe = wave.scale_data(args, dataframe)
    # TODO plugin hook after_scale

    files = wave.write_wav(args, dataframe)

    # for f in files:
    #     plot.draw_window(f)

    # TODO pluin hook after_save

    end = timer()

    logging.info("Done in {}s".format(
        round(end - start, 3)
    ))


if __name__ == "__main__":
    main()
