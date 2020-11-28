#!/usr/bin/env python3
from timeit import default_timer as timer
start = timer()

import logging
from rich.logging import RichHandler
from rich.traceback import install
import sys
from pathlib import Path

import parse
import plugin_handler

# setup logging
# needs to be global, since other files rely on it
install()  # install rich exception handler
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
loglevel = {
    "info": logging.INFO,
    "debug": logging.DEBUG
}

def main():
    args = parse.parse_args()

    #  set log level
    if args.loglevel == "none":
        log.propagate = False
    else:
        logging.getLogger("rich").setLevel(loglevel[args.loglevel])
    log.debug(args)

    if not Path(args.infile[0]).exists():
        log.critical("File [bold red]{}[/] (infile) does not exist or could not be found!".format(
            str(Path(args.infile[0]))
        ))
        sys.exit(1)

    log.info("Converting {} to {}".format(
        str(Path(args.infile[0]).resolve()),
        str(Path(args.outfile[0]).resolve())
    ))

    plugin_handler.import_plugin(args)

    log.debug(str(timer()) +" importing reader module")
    import reader
    log.debug(str(timer()) +" imported reader module")
    dataframe = reader.read_file(args)

    if dataframe is None:
        log.critical(
            "Dataframe could not be parsed. There probably is additional output above. Exiting")
        sys.exit(0)

    dataframe = plugin_handler.call_plugin(1, args, dataframe)

    log.debug(str(timer()) +" importing manipulate module")
    import manipulate
    log.debug(str(timer()) +" imported manipulate module")
    dataframe = manipulate.manipulate_data(args, dataframe)

    dataframe = plugin_handler.call_plugin(2, args, dataframe)

    log.debug(str(timer()) +" importing wave_writer module")
    import wave_writer
    log.debug(str(timer()) +" imported wave_writer module")
    dataframe = wave_writer.scale_data(args, dataframe)

    dataframe = plugin_handler.call_plugin(3, args, dataframe)

    files = wave_writer.write_wav(args, dataframe)

    # for f in files:
    # plot.draw_window(f)

    plugin_handler.call_plugin(4, args, dataframe)

    end = timer()

    log.info("Done in [bold blue]{}s[/]".format(
        str(round(end - start, 3))
    ))


if __name__ == "__main__":
    main()
