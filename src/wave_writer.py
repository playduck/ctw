import logging
import os

import numpy as np
from scipy.io.wavfile import write

log = logging.getLogger("rich")

dt = None


def scale_data(args, data):
    global dt

    log.debug("scaling data to {}".format(args.bps))

    # floating
    if args.bps == "32f":
        for col in data.columns:
            if col == "x":
                continue
            data[col] = data[col].astype(np.float32)
        dt = np.float32
        return data

    # fixed
    if args.bps == "u8":
        output_range = (0, 2**8 - 1)
        dt = np.uint8
    elif args.bps == "16":
        output_range = (-2**15, 2**15 - 1)
        dt = np.int16
    elif args.bps == "32":
        output_range = (-2**31, 2**31 - 1)
        dt = np.int32

    for col in data.columns:
        if col == "x":
            continue
        data[col] = np.round(
            np.interp(
                data[col],
                (-1.0,
                 1.0),
                output_range),
            decimals=0)
        data[col] = data[col].astype(dt)
    return data


def write_wav(args, data):
    global dt

    if args.multichanel:
        log.debug("Writing multichanel file at {}".format(
            args.outfile[0]
        ))

        del data["x"]
        values = np.array(data.values.tolist(), dtype=dt)
        write(args.outfile[0], args.samplerate, values)
        return args.outfile
    else:
        # generate file names if not enough were supplied

        files = args.outfile
        diff = (len(data.columns) - 1) - len(args.outfile)
        last_file_name, extension = os.path.splitext(files[-1])
        for i in range(diff):
            files.append("{}_{}{}".format(last_file_name, i, extension))

        log.debug("Writing files at {}".format(
            files
        ))

        for index, col in enumerate(data.columns):
            if col == "x":
                continue
            write(files[index - 1], args.samplerate, data[col].values)

        return files
