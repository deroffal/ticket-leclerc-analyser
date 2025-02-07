import logging
import os
import re
from datetime import datetime

from bs4 import BeautifulSoup

from src.utils.processed_files import save_to_processed
from src.utils.raw_files import list_raw_files, open_raw_file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def process_raw_file(_filename):
    with open_raw_file(_filename) as _file:
        _ticket = parse_html_ticket(_file.read())
        _content = clean_data(_ticket['content'])
        _ticket['content'] = _content
        return _ticket


def parse_html_ticket(html):
    soup = BeautifulSoup(html, 'html.parser')

    _ticket = dict()

    _content = dict()
    _ticket['content'] = _content

    _metadata = dict()
    _ticket['metadata'] = _metadata

    current_category = None

    for td in soup.find_all('td'):

        text = td.find("span").text.replace('\xa0', ' ')

        # shopping date
        match = re.search(r'(\d{2}/\d{2}/\d{2})', text)
        if match:
            date = match.group(1)
            formated = datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d')
            _metadata['date'] = formated
            continue

        # start of category
        if text.__contains__('>>'):
            current_category = text
            _content[current_category] = []
            continue

        # Total&nbsp;58&nbsp;articles
        match = re.search(r'Total \d* articles\s+([\d.]+)', text)
        if match:
            _totalPrice = match.group(1)
            _metadata['totalPrice'] = _totalPrice
            continue

        match = re.search(r'Remises lots\s+(-?[\d.]+)', text)
        if match:
            _remiseLot = match.group(1)
            _metadata['remiseLot'] = _remiseLot
            continue

        # end of articles
        if text.__contains__('----------'):
            current_category = None

        if not current_category is None:
            _content.get(current_category).append(text)
    return _ticket


def clean_data(raw):
    content = dict()
    for category in raw:
        cat = category.replace('>>', '').replace(' ', '')

        lines = []

        iterator = iter(raw[category])
        #
        while (_line := next(iterator, None)) is not None and _line.strip() != '':
            # single_line_pattern
            matches = re.match(r"^\s*(.+?)\s+([\d.]+)\s+(\d+)\s*$", _line)
            if matches:
                name, price, tax = matches.groups()
                lines.append({
                    'name': name,
                    'quantity': '1',
                    'unit_price': price,
                    'total_price': price,
                    'tax': tax
                })
            else:
                name = _line.strip()
                _line = next(iterator)
                # multi_lines_pattern
                matches = re.match(r"^\s*(\d+)\s+X\s+([\d.]+)(€|\\u20ac)?\s+([\d.]+)\s+(\d+)\s*$", _line)
                if matches:
                    quantity, unit_price, currency, total_price, tax = matches.groups()
                    lines.append({
                        'name': name,
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'total_price': total_price,
                        'tax': tax
                    })
                else:
                    logger.warning(f"Warning : cannot parse this line : {_line}")

        content[cat] = lines
    return content


def category_to_lines(_filename, _category, _products) -> list[str]:
    lines = []
    for _product in _products:
        lines.append(
            f"""{_filename};{_category};{_product['name']};{_product['quantity']};{_product['unit_price']};{_product['total_price']};{_product['tax']}""")
    return lines


if __name__ == "__main__":

    for filename in list_raw_files():
        logger.info(f"processing {filename} file")
        categories = process_raw_file(filename)['content']

        csv = map(lambda category: category_to_lines(filename, category, categories[category]), categories)
        csvLines = [item for row in list(csv) for item in row]

        base, _ = os.path.splitext(filename)
        save_to_processed(base + ".csv", "filename;category;product_name;quantity;unit_price;total_price;tax", csvLines)
