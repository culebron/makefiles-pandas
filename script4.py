import argh

@argh.dispatch_command
def main(input_file, output_file, dry_run=False, router_mode='transit'):
    with open(source_file) as src, open(target_file) as trg:
        reader = csv.DictReader(h)
        writer = csv.DictWriter(h, ['A', 'B', 'X'])
        writer.writeheader()

        for line in reader:
            line['X'] = line['A'] * line['B']
            writer.write(line)
