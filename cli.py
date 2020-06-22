import sys
import os
import io
import csv
import logging
import warnings
import argparse
import chardet
import tqdm
import comparesv
from version import __version__

from pprint import pprint

# This file is derived from https://github.com/maxharlow/csvmatch/blob/master/cli.py

def main():
    logging.captureWarnings(True)
    logging.basicConfig(level=logging.WARN, format='Warning: %(message)s')
    warnings.formatwarning = lambda e, *args: str(e)
    sys.stderr.write('Starting up...\n')
    try:
        file1, file2, args = arguments()
        data1, headers1 = read(*file1)
        data2, headers2 = read(*file2)
        results = comparesv.run(data1, headers1, data2, headers2, ticker=ticker, **args)
        # formatted = format(results['values'],results['headers'])
        if args.get("save_output"):
            save_file("values.csv", results['headers'], results['values'])
            save_file("results.csv", results['headers'], results['results'])
        pprint(results['stats'])
        sys.stdout.flush()
    except BaseException as e:
        sys.exit(e)


def ticker(text, total):
    progress = tqdm.tqdm(bar_format=text + ' |{bar}| {percentage:3.0f}% / {remaining} left', total=total)
    return progress.update


def read(filename, encoding):
    if not os.path.isfile(filename) and filename != '-':
        raise Exception(filename + ': no such file')
    file = sys.stdin if filename == '-' else io.open(filename, 'rb')
    text = file.read()
    if text == '':
        raise Exception(filename + ': file is empty')
    if not encoding:
        detector = chardet.universaldetector.UniversalDetector()
        text_lines = text.split(b'\n')
        for i in range(0, len(text_lines)):
            detector.feed(text_lines[i])
            if detector.done:
                break
        detector.close()
        encoding = detector.result['encoding']  # can't always be relied upon
        sys.stderr.write(filename + ': autodetected character encoding as ' + encoding.upper() + '\n')
    try:
        text_decoded = text.decode(encoding)
        reader = csv.reader(io.StringIO(text_decoded, newline=None))
        headers = next(reader)
        return list(reader), headers
    except UnicodeDecodeError as e:
        raise Exception(filename + ': could not read file -- try specifying the encoding')
    except csv.Error as e:
        raise Exception(filename + ': could not read file as a CSV')


def arguments():
    parser = argparse.ArgumentParser(description='CSV files comparison')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('FILE1', nargs='?', default='-', help='the first CSV file')
    parser.add_argument('FILE2', nargs='?', default='-', help='the second CSV file')
    parser.add_argument('--enc1', type=str, metavar='ENCODING', help='encoding of the first file (default is to autodetect)')
    parser.add_argument('--enc2', type=str, metavar='ENCODING', help='encoding of the second file (default is to autodetect)')
    parser.add_argument('-i', '--ignore-case', action='store_true', help='ignore case (default is case-sensitive)')
    parser.add_argument('-rm', '--row-match', default='order', help='Logic to be used to identify the rows. Possible options \'order\', \'fuzzy\', \'deep\' (default is order)')
    parser.add_argument('-cm', '--column-match', default='exact', help='Logic to be used to identify the columns. Possible options \'exact\',\'fuzzy\' (default is exact)')
    parser.add_argument('-sm', '--string-match', default='exact', help='Logic to be used to identify the columns. Possible options \'exact\',\'fuzzy\' (default is exact)')
    parser.add_argument('-ir', '--include-addnl-rows', action='store_true', help='Include additional rows from second file (default is false)')
    parser.add_argument('-ic', '--include-addnl-columns', action='store_true', help='Include additional columns from second file (default is false)')
    parser.add_argument('-is', '--include-stats', default=True, action='store_true', help='Include stats (default is true)')
    parser.add_argument('-s', '--save-output', default=True, action='store_true', help='Save output to file. This saves the output in the current directory (default is true)')

    args = vars(parser.parse_args())
    if args['FILE1'] == '-' and args['FILE2'] == '-':
        parser.print_help(sys.stderr)
        parser.exit(1)
    file1 = args.pop('FILE1')
    file2 = args.pop('FILE2')
    enc1 = args.pop('enc1')
    enc2 = args.pop('enc2')
    return (file1, enc1), (file2, enc2), args

def save_file(file_name, keys, results):
    updated_keys = ['S.No'] + keys
    updated_results = [[idx+1]+result for idx,result in enumerate(results)]

    curr_dir = os.getcwd()
    with open(os.getcwd() + os.path.sep + file_name, 'w') as file:
        writer = csv.writer(file, lineterminator='\n')  # can't use dictwriter as headers are printed even when there's no results
        writer.writerow(updated_keys)
        writer.writerows(updated_results)

def format(results, keys):
    writer_io = io.StringIO()
    writer = csv.writer(writer_io, lineterminator='\n')  # can't use dictwriter as headers are printed even when there's no results
    writer.writerow(keys)
    writer.writerows(results)
    return writer_io.getvalue()[:-1]


if __name__ == '__main__':
    main()