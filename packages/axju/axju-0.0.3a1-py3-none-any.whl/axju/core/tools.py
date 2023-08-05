import logging
import argparse

def setup_logger(verbose, file):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    if verbose:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    if file:
        fh = logging.FileHandler(file)
        fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

    return logger


def setup_parser():
    parser = argparse.ArgumentParser(description='Some atomation stuff, have fun')
    parser.add_argument('-v', '--verbose', action='store_true', help='For debugging ;)')
    parser.add_argument('-l', '--log', type=str, help='Logfile')
    parser.add_argument('-s', '--steps', nargs='+', type=str, default=['run'], help='All the steps')
    parser.add_argument('--json', type=argparse.FileType('r'), help='Load the steps json-file')
    parser.add_argument('--show', action='store_true', help='Show the steps.')

    return parser


class SmartCLI(object):
    """This only works, if the argument are for the init. There is no support
    for None."""

    def __init__(self, cls):
        self.cls = cls
        self.parser = setup_parser()
        self.additional = []

    def add_argument(self, *args, **kwargs):
        action = self.parser.add_argument(*args, **kwargs)
        self.additional.append(action.dest)

    def run(self):
        args = self.parser.parse_args()
        setup_logger(args.verbose, args.log)

        kwargs = {}
        for arg, value in vars(args).items():
            if arg in self.additional and value:
                kwargs[arg] = value

        worker = self.cls(**kwargs)

        if args.show: return worker.show(args.show)

        for step in args.steps: worker.run(step)
