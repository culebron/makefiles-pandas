import argparse
import csv

def make_parser():
    parser = argparse.ArgumentParser(description="Wand script")
    subparsers = parser.add_subparsers(help='sub-command help')
    parser = subparsers.add_parser('export', help='export dataset from different sources')
    parser.set_defaults(which='export')
    parser.add_argument('source_file', help='name of the source dataset')
    parser.add_argument('target_file', help='name of the source dataset')
    parser.add_argument('router_mode', help='transport mode of router', default='transit')

    parser.add_argument('-d', '--dry-run', default=False, help='only test the output on a small sample')
    return parser

def main(source_file, target_file, router_mode, dry_run):
    # ваш скрипт здесь
    with open(source_file) as src, open(target_file) as trg:
        reader = csv.DictReader(h)
        writer = csv.DictWriter(h, ['A', 'B', 'X'])
        writer.writeheader()

        for line in reader:
            line['X'] = line['A'] * line['B']

            writer.write(line)

if __name__ == '__main__':
    parser = make_parser()
    main(**parser.parse_args().as_dict())
