import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        prog='tool',
        description="CSV to Wav Converter",
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog,
            max_help_position=48
        )
    )

    # File Options
    parser.add_argument('infile', nargs=1, help='input file',
                        type=str)
    parser.add_argument('outfile', nargs=1, help='output file',
                        type=str)

    # CSV Options
    csv_group = parser.add_argument_group('csv reader')
    csv_group.add_argument("-sep", "--seperator", dest="seperator",
                           help="CSV Value Seperator",
                           default=";", type=str)
    csv_group.add_argument("-dec", "--decimal", dest="decimal",
                           help="CSV Value Decimal Point",
                           default=".", type=str)
    xaxis_group = csv_group.add_mutually_exclusive_group()
    xaxis_group.add_argument("-x", "--x-axis", dest="xaxis",
                             help="x-axis header name",
                             default=None, type=str)
    xaxis_group.add_argument("--gen-x", dest="genx", help="Generate X-Axis",
                             action="store_true")

    # Wav Options
    wav_group = parser.add_argument_group('wav writer')
    wav_group.add_argument("-bps", "--bits-per-sample", dest="bps",
                           help="Bits per Sample",
                           choices=["u8", "16", "32", "32f"],
                           default="16", type=str)
    wav_group.add_argument("-sr", "--samplerate", dest="samplerate",
                           help="output samplerate in Hz",
                           default=44100, type=int)
    wav_group.add_argument("--bias", dest="bias",
                           help="Value Bias ",
                           default=0.0, type=float)
    wav_group.add_argument("-c", "--clipping", dest="clipping",
                           help="clipping handling",
                           choices=["hard", "soft"],
                           default="hard", type=str)
    wav_group.add_argument("-i", "--interpolation", dest="interpolation",
                           help="data interpolation between samples",
                           choices=["nearest", "linear", "quadratic", "cubic"],
                           default="linear", type=str)
    wav_group.add_argument(
        "--multichanel",
        dest="multichanel",
        help="generate multichanel wav file, otherwise multiple single channel files",
        action="store_true")

    # programm options
    prog_group = parser.add_argument_group('program options')
    prog_group.add_argument(
        "-l",
        "--log-level",
        dest="loglevel",
        help="Logging Level",
        choices=[
            "none",
            "info",
            "debug"],
        default="info",
        type=str)
    # Plugin
    prog_group.add_argument("-p", "--plugin", dest="plugin",
                            help="Custom python plugin path",
                            default=16, type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args
