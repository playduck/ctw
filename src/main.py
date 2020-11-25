#!/usr/bin/env python3

import logging
from rich.logging import RichHandler
from rich.traceback import install
import os
import sys
from timeit import default_timer as timer

import manipulate
import parse
# import plot
import reader
import wave_writer as wave
import plugin_handler

# setup logging
# needs to be global, since other files rely on it
install() # install rich exception handler
loglevel = {
    "none": logging.NOTSET,
    "info": logging.INFO,
    "debug": logging.DEBUG
}
log = logging.getLogger("rich")
logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(
        rich_tracebacks=True,
        markup=True
    )]
)

def main():
    start = timer()
    args = parse.parse_args()

    #  set log level
    logging.getLogger("rich").setLevel(loglevel[args.loglevel])

    log.debug(args)
    log.info("Converting {} to {}".format(
        args.infile, args.outfile
    ))

    plugin_handler.import_plugin(args)

    dataframe = reader.read_file(args)
    if dataframe is None:
        log.error(
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

    log.info("Done in [bold blue]{}s[/]".format(
        str(round(end - start, 3))
    ))


if __name__ == "__main__":
    main()
