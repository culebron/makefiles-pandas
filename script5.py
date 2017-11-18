import argh

@argh.dispatch_command
def main(input_file, output_file, dry_run=False, router_mode='transit'):
    # чтение вводного файла
    df1 = pd.read_csv(input_file)

    # операции идут с колонками
    df1['X'] = df1['A'] * df1['B']

    # запись вывода
    df1.to_csv(output_file)
