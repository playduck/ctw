import logging

import numpy as np
import pandas as pd
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

    return data

# add bias value


def add_bias(args, data):
    log.debug("Adding Bias")
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

    xnew = np.linspace(start=start, stop=stop, num=samples)

    values = {}
    for col in data.columns:
        if col == "x":
            values[col] = xnew
            continue

        spl = scipy.interpolate.interp1d(
            data["x"].values,
            data[col].values,
            kind=args.interpolation,
            copy=False,
            assume_sorted=False,
            bounds_error=False,
            fill_value="extrapolate"
        )

        y = spl(xnew)
        values[col] = y

    df = pd.DataFrame(data=values)

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
