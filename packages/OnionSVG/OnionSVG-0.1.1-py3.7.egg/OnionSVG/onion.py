from OnionSVG.__init__ import OnionSVG
import argparse

# todo: possible to add a setup option to install as an executable in $PATH?


def str2bool(value):
    if value.lower() in ('yes', 'y', 'true', 't', '1'):
        return True
    elif value.lower in ('no', 'n', 'false', 'f', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError(f"Boolean value expected; received {value}")


parser = argparse.ArgumentParser()
parser.add_argument('path', default = '', help = 'Path to .svg file')
parser.add_argument(
    'peel', nargs = '*', default = 'all',
    help = "Layers to render. \n 'all'/None -> all layers, ['re', '*pattern*']/"
           "['*pattern*'] -> match regular expression")
parser.add_argument('--dpi', default = 200, type = int, help = 'DPI of .svg render')
parser.add_argument('--to', default = None, help = 'Output folder')
parser.add_argument('--list', default = False, const = True, type = str2bool, nargs = '?',
                    help = 'List all layers in the file (does not peel the file!).'
                    )

if __name__ == '__main__':
    args = parser.parse_args()

    svg = OnionSVG(args.path, int(float(args.dpi)), args.to)

    if args.list:
        svg.list()
    else:
        if args.peel is None:
            svg.peel('all', to = args.to, dpi = args.dpi)
        elif args.peel[0] == 're':
            svg.peel(args.peel[1], to = args.to, dpi = args.dpi)
        elif len(args.peel) == 1 and args.peel is not 'all':
            svg.peel(args.peel[0], to = args.to, dpi = args.dpi)
        elif args.peel == 'all':
            svg.peel('all', to = args.to, dpi = args.dpi)
        else:
            argparse.ArgumentTypeError(f"Expected value: ['re', *pattern*], [*pattern*], ['all'] or []")
