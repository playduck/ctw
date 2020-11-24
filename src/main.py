#!/usr/bin/env python3

import logging
import os
import sys
from timeit import default_timer as timer

import manipulate
import parse
# import plot
import reader
import wave_writer as wave
import plugin_handler

loglevel = {
    "none": logging.NOTSET,
    "info": logging.INFO,
    "debug": logging.DEBUG
}

def main():
    start = timer()
    logging.basicConfig(format="[%(levelname)s]: %(message)s")
    args = parse.parse_args()
    logging.getLogger().setLevel(loglevel[args.loglevel])

    logging.debug(args)
    logging.info("Converting {} to {}".format(
        args.infile, args.outfile
    ))

    plugin_handler.import_plugin(args)

    dataframe = reader.read_file(args)
    if dataframe is None:
        logging.error(
            "Dataframe could not be parsed. There probably is additional output above. Exiting")
        sys.exit(0)

    dataframe = plugin_handler.call_plugin(1, args, dataframe)

    dataframe = manipulate.manipulate_data(args, dataframe)

    dataframe = plugin_handler.call_plugin(2, args, dataframe)

    dataframe = wave.scale_data(args, dataframe)

    dataframe = plugin_handler.call_plugin(3, args, dataframe)

    files = wave.write_wav(args, dataframe)

    # for f in files:
        # plot.draw_window(f)

    plugin_handler.call_plugin(4, args, dataframe)

    end = timer()

    logging.info("Done in {}s".format(
        round(end - start, 3)
    ))


if __name__ == "__main__":
    main()
