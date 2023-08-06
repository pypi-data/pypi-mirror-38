import argparse
import logging
import sys

class ArgparseMixin(object):

    def __init__(self):
        super(ArgparseMixin, self).__init__()
        self.parser = self.setup_parser()

    def setup_parser(self):
        parser = argparse.ArgumentParser(description='Some atomation stuff, have fun')
        parser.add_argument('-v', '--verbose', action='store_true', help='For debugging ;)')
        parser.add_argument('-l', '--log', type=str, help='Logfile')
        parser.add_argument('-s', '--steps', nargs='+', type=str, default=['run'], help='All the steps')
        parser.add_argument('--json', type=argparse.FileType('r'), help='Load the steps json-file')
        parser.add_argument('--show', action='store_true', help='Show the steps.')
        return parser

    def setup_logger(self, **kwargs):
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        if kwargs.get('verbose', False):
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.INFO)
        self.logger.addHandler(ch)

        if kwargs.get('file', False):
            fh = logging.FileHandler(kwargs.get('file'))
            fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
            fh.setLevel(logging.DEBUG)
            self.logger.addHandler(fh)

    def parse(self, args=None):
        self.args, unknown = self.parser.parse_known_args(args)
        self.setup_logger(verbose=self.args.verbose, file=self.args.log)

    def run(self, args=None):
        if not hasattr(self, 'args') or args:
            self.parse(args)

        if self.args.show: return self.show()

        for step in self.args.steps:
            super(ArgparseMixin, self).run_step(step)
