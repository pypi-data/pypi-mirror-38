"""Entry point for package.

To play with scripts parameters, you must use the configuration
file instead of the direct enumeration of filenames.

"""

import os
import argparse
import itertools
from . import core
from . import __version__


def parse_cli(args:iter=None) -> dict:
    # main parser
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('infiles', type=str, nargs='*', metavar='MODULE',
                        default=[], help='files containing ASP or Python code')
    parser.add_argument('--outfile', '-o', type=str, default='out.png',
                        help="output file. Will be overwritten with png data. Can be templated with '{}'")
    parser.add_argument('--dotfile', '-d', type=str, default=None,
                        help="output file. Will be overwritten with dot data. Can be templated with '{}'")
    parser.add_argument('--config', '-c', type=str, default=None,
                        help="configuration file, specifying scripts and their options")
    parser.add_argument('--gif-duration', '-gd', type=int, default=500,
                        help="gif duration in millisecond")
    parser.add_argument('--nb-model', '-n', type=int, default=0,
                        help="number of model of the final context to handle. 0 for all.")
    parser.add_argument('-v', '--verbosity', action='count', default=0)
    parser.add_argument('--version', action='version', version=f'biseau {__version__}')

    # flags
    parser.add_argument('--gif', '-g', action='store_true', default=None,
                        help="Do not merge graphs ; build a gif with frame for each model")

    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_cli()
    all_infiles = args.infiles
    if args.config:
        all_infiles = itertools.chain(
            all_infiles,
            core.build_pipeline.from_configfile(args.config, verbosity=args.verbosity)
        )
    if os.path.splitext(args.outfile)[1] == '.gif' and args.gif is None:
        args.gif = True  # turn on the gif behavior

    if args.gif:
        core.gif_from_filenames(
            all_infiles,
            giffile=args.outfile,
            dotfile_template=args.dotfile,
            duration=args.gif_duration,
            verbosity=args.verbosity,
            nb_model=args.nb_model,
        )
    else:
        if args.outfile and '{}' in args.outfile:
            builder = core.multiple_images_from_filenames
        else:
            builder = core.single_image_from_filenames
        builder(
            all_infiles,
            dotfile=args.dotfile,
            outfile=args.outfile,
            return_image=False,
            verbosity=args.verbosity,
            nb_model=args.nb_model,
        )
