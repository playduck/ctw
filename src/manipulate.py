import logging

import numpy as np
from pandas import DataFrame
import scipy.interpolate

log = logging.getLogger("rich")


def manipulate_data(args, data):
    return handle_clipping(
        args, interpolate_data(
            args, add_bias(
                args, normalize_data(
                    args, validate_data(
                        args, data)))))

# replace NaN with 0


def validate_data(args, data):
    log.debug("Validating Data")
    for col in data.columns:
        if col == "x":
            if not np.all(np.diff(data[col]) >= 0):
                log.warning(
                    "X-Axis is not strictly monotonously increasing.")

        np.nan_to_num(data[col], copy=False, nan=0.0, posinf=None, neginf=None)
    return data

# divide everything by max value


def normalize_data(args, data):
    maxValue = 0

    if args.maxVal is None:
        log.debug("No Max Value specified, finding one from given Data")
        for col in data.columns:
            if col == "x":
                continue
            # optimize?
            maxColVal = max(data[col].max(), abs(data[col].min()))
            maxValue = max(maxColVal, maxValue)
    else:
        maxValue = args.maxVal

    log.debug("Max Value is {}".format(maxValue))

    for col in data.columns:
        if col == "x":
            continue
        data[col] = np.true_divide(data[col], maxValue)
        print(data[col])

    return data

# add bias value


def add_bias(args, data):
    log.debug("Adding Bias ({})".format(args.bias))

    if args.bias != 0.0:
        for col in data.columns:
            if col == "x":
                continue
            data[col] = np.add(data[col], args.bias)

    return data

# interpolate value


def interpolate_data(args, data):
    log.debug("Interpolating Data")

    start = data["x"].values[0].astype(np.int64)
    stop = data["x"].values[-1].astype(np.int64)
    delta = stop - start
    samples = int(args.samplerate * delta)

    log.debug(
        "from {} s to {} s (delta: {} s) with {} samples".format(
            start, stop, delta, samples))

    # generate new x-axis
    #xnew = np.linspace(start=start, stop=stop, num=samples, dtype=np.int64)

    axis_fragments = list()
    max_frament = 1000000
    # if we have too many samples 
    if samples > max_frament:
        delta_time = round(max_frament / args.samplerate)
        amt_time =  int(round(delta / delta_time))

        for i in range(amt_time):
            fragment_start = int(round(i * delta_time + start))
            fragment_end = int(round(min(((i+1) * delta_time + start, stop))))
            fragment_samples = (fragment_end - fragment_start) * args.samplerate
            
            axis_fragments.append(
                # type of fragments must be float, otherwise interp1d acts like kind=="next"
                # i don't know why (presumably since data["x"] is also float)
                # just roll with it
                np.linspace(start=fragment_start, stop=fragment_end, num=fragment_samples, dtype=np.float32)
            )
    else:
        axis_fragments.append(
            np.linspace(start=start, stop=stop, num=samples, dtype=np.int64)
        )

    values = {}
    for index, col in enumerate(data.columns):
        if col == "x":
            # TODO this isn't better than just not fragementing,
            # maybe use multiple object (might break plugins)
            # or use memory to disk mapping
            for i, f in enumerate(axis_fragments):
                if i == 0:
                    values[col] = f
                else:
                    values[col] = np.concatenate((values[col] ,f))
            continue

        spl = scipy.interpolate.interp1d(
            data["x"].values,
            data[col].values,
            kind=args.interpolation,
            copy=False,
            assume_sorted=True,
            bounds_error=True,
        )

        for i, f in enumerate(axis_fragments):
            render = spl(f)

            if i == 0:
                y = render
            else:
                y = np.concatenate((y ,render))

        values[col] = y

    df = DataFrame(data=values)

    return df

# apply clipping function


def handle_clipping(args, data):
    log.debug("Clipping Data ({})".format(args.clipping))
    for col in data.columns:
        if col == "x":
            continue

        if args.clipping == "hard":
            data[col] = np.clip(data[col], -1.0, 1.0)

        elif args.clipping == "soft":
            # \alpha=7
            # a=\frac{2}{0.434}\cdot\frac{1}{\alpha}
            # a\cdot\log\left(\frac{1+e^{\alpha\left(x+0.5\right)}}{1+e^{\alpha\left(x-0.5\right)}}\right)-1
            # https://www.desmos.com/calculator/kumbehzhoi
            alpha = 7
            a = (2.0 / 0.434) * (1.0 / alpha)
            data[col] = (a * np.log10(np.true_divide(
                (1.0 + np.exp(alpha * (data[col] + 0.5))),
                (1.0 + np.exp(alpha * (data[col] - 0.5)))
            ))) - 1.0

    return data
