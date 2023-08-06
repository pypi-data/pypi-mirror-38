from . import parse
import argparse

def main():
    cli_arguments = argparse.ArgumentParser()
    cli_arguments.add_argument('template', help='Template file to process')
    cli_arguments.add_argument('-o', '--output', default='config.out',
            help='Output file')
    cli_arguments.add_argument('-P', '--parent', default='~/.config/i3',
            type=str, help='Parent directory to look files in')
    args = cli_arguments.parse_args()

    try:
        template = open(args.template, 'r')
    except OSError:
        raise OSError("Error: Cannot open {}".format(args.template))

    try:
        output = open(args.output, 'w')
    except OSError:
        template.close()
        raise OSError("Error: Cannot open {}".format(args.output))

    config = parse(template.read())

    output.write(config)

    output.close()
    template.close()
