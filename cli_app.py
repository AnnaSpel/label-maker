import argparse
import logging
import textwrap
from pathlib import Path

from calc import calculate_unit_price
from inputs import csv_input, user_input
from outputs import to_word

log = logging.getLogger(__name__)


def cli_main(args):
    log.info('cli start')
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            '''\
            Label Maker
            Defaults to user input from console.
            If you wish, you may specify input and template file.
            Input must be a csv file, output then a jinja formatted docx.
            '''
        ),
    )
    parser.add_argument(
        'data-input',
        choices=['file', 'user'],
        default='file',
        const='file',
        nargs='?',
    )

    parser.add_argument(
        '-i',
        '--input-file',
        type=Path,
        default='input/sample_data.csv',
        const='input/sample_data.csv',
        nargs='?',
        help='specify input data csv file(defaults to: %(default)s)',
    )

    args = parser.parse_args(args)

    data = []
    data_input = args.data_input

    if data_input == 'file':
        file_path = args.input_file
        data = csv_input(file_path)
    elif data_input == 'user':
        data = user_input()
    else:
        log.warning(f'neznám možnost vstupu:{data_input}')
        exit()

    calculated_data = calculate_unit_price(data)
    to_word(calculated_data, 'templates/labels_template.docx')
    log.info(' program end '.center(80, '-'))
