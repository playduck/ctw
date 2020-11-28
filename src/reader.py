import logging
from timeit import default_timer as timer

log = logging.getLogger("rich")

from numpy import linspace, float64
from pandas import DataFrame, read_csv

def rename_axes(args, read_df):
    if args.xaxis is None:
        xaxis = read_df.columns[0]
        log.warning(
            "No X-Axis specified. Using \'{}\' as X-Axis".format(xaxis))
    else:
        xaxis = args.xaxis

    names = {}
    counter = 0
    for axis in read_df.columns:
        if axis == xaxis:
            names[xaxis] = "x"
            length = len(read_df[xaxis].values)

    for axis in read_df.columns:
        if axis != xaxis:
            if len(read_df[axis].values) != length:
                log.error(
                    "Dataframe Length Missmatch! All columns need to have the same length. ({} len: {} !=  {} len: {} )".format(
                        xaxis, length, axis, len(
                            read_df[axis].values)))
                return None
            names[axis] = "y" + str(counter)
            counter += 1

    log.debug("Dataframe output names: {}".format(names.values()))
    return read_df.rename(columns=names, errors="raise",)


def generate_axes(args, read_df):
    # only one column
    log.info("X-Axis is beeing automatically generated")
    if args.xaxis is not None:
        log.warning("X-Axis Argument ignored")

    samples = read_df.axes[0].stop

    log.debug(
        "generating linear X-Axis from {} to {} with {} steps".format(0, samples - 1, samples))
    x = linspace(0, samples - 1, samples)

    tagged_data = {"x": x}
    for index, col in enumerate(read_df.columns):
        tagged_data["y" + str(index)] = read_df[col].values

    log.debug("Dataframe output names: {}".format(tagged_data.keys()))
    return DataFrame(tagged_data)


def read_file(args):
    log.debug("Parsing CSV file {}".format(args.infile[0]))
    read_df = read_csv(args.infile[0],
                          sep=args.seperator,
                          decimal=args.decimal,
                          dtype=float64
                          )

    if (len(read_df.columns) > 1) and not args.genx:
        log.debug("Renaming Axes")
        return rename_axes(args, read_df)
    else:
        log.debug("Generating Axes")
        return generate_axes(args, read_df)
