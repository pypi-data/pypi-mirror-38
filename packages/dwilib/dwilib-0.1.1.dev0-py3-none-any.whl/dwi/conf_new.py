"""Conf - new."""

# import argparse

import configargparse

import dwi.conf
# import dwi.files
# from .types import Path
import dwi.util


####
# rcParams['texture.methods'] = ['hu', 'zernike', 'gabor']
# #rcParams['texture.winsizes.small'] = (3, 6, 2)
####


####


# class RcParser(argparse.ArgumentParser):
#     """Configuration parser."""
#     def __init__(self, **kwargs):
#         kwargs.setdefault('fromfile_prefix_chars', '@')
#         kwargs.setdefault('add_help', False)
#         self_as_super = super(self.__class__, self)
#         self_as_super.__init__(**kwargs)
#
#     def convert_arg_line_to_args(self, line):
#         """Treat each space-separated word as an argument. Allow comments."""
#         line = line.split(dwi.files.COMMENT_PREFIX, 1)[0]
#         return line.split()
#
#
# def parse_rc(paths=None):
#     if paths is None:
#         paths = ['dwilib.rc']
#         paths = [Path(x) for x in paths]
#     p = RcParser()
#     p.add_argument('path', nargs=1,
#                    help='input pmap files')
#     p.add_argument('-v', '--verbose', action='count',
#                    help='increase verbosity')
#     p.add_argument('-b1', type=int, nargs='*')
#     p.add_argument('-b2', type=int, nargs='*')
#     # p.add_argument('-k', '--keys', default='shape,path')
#     # p.add_argument('--texture_winsizes_large', type=int, nargs=2)
#     p.add_argument('--texture.winsizes.large', type=float, nargs=3)
#     args = [p.fromfile_prefix_chars[0]+str(x) for x in paths if x.exists()]
#     namespace = p.parse_args(args=args)
#     return namespace
#
#
# # args = parse_rc()
# # print(args)
# # print(args.__dict__['texture.winsizes.large'])


def get_basic_parser(**kwargs):
    """Get an argument parser with standard arguments ready."""
    files = ['/etc/dwilib/*.cfg', '~/.config/dwilib/*.cfg', './dwilib.cfg']
    p = configargparse.get_parser(default_config_files=files, **kwargs)
    p.add('-v', '--verbose', action='count', default=0,
          help='increase verbosity')
    p.add('--logfile', help='log file')
    p.add('--loglevel', default='WARNING', help='log level name')
    p.add('--cfg', is_config_file_arg=True, metavar='PATH',
          help='spesify config file')
    p.add('--dumpcfg', is_write_out_config_file_arg=True, metavar='PATH',
          help='dump current config file and exit')
    return p


# XXX: How to arrange these...
def parse_core_args():
    """Parse command-line arguments for core library."""
    p = get_basic_parser(name='core', add_help=False)
    p.add('--maxjobs', type=int,
          help='limit the number of concurrent jobs')
    # p.add('-m', '--modes', nargs='*', metavar='MODE', type=dwi.ImageMode,
    #       default=['DWI-Mono-ADCm', 'DWI-Kurt-ADCk', 'DWI-Kurt-K'],
    #       help='imaging modes')
    # p.add('-t', '--thresholds', nargs='*', type=dwi.GleasonScore,
    #       default=['0+0', '3+3'],
    #       help='classification thresholds (maximum negative)')
    p.add('--nboot', type=int, default=0,
          help='number of bootstraps (try 2000)')
    p.add('--texture_methods', nargs='*',
          help='texture methods')
    # args, unknown = p.parse_known_args()
    # Call without cmdline args to avoid confusion with doit args.
    args, unknown = p.parse_known_args(args=[])
    return args, unknown


# XXX: Problem: if called by doit, tries to parse doit's args.
# I guess I could just not use doit's args.
# Or use a parser here that doesn't do cmdline?
# Or do doit stuff in dedicated program.
# Now I get it, must parse with no args, like this: p.parse_known_args(args=[])
args, unknown = parse_core_args()
dwi.conf.init_logging(args)
if args.texture_methods:
    dwi.conf.rcParams['texture.methods'] = args.texture_methods
