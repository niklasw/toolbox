#!/usr/bin/env python3

import requests
import json
from pathlib import Path
from datetime import datetime, timedelta
from dateutil import tz
import matplotlib.pyplot as plt
import pandas as pd

url = "https://www.nordpoolgroup.com/api/marketdata/page/" \
      "10?currency=SEK,SEK,SEK,SEK"
region = 'SE3'
time_fmt = "%Y-%m-%dT%H:%M:%S"  # "2023-05-29T11:00:00"

local_cache = Path('/tmp/nordpool.json')

TIME_ZONE = 'Europe/Stockholm'
TZ = tz.gettz(TIME_ZONE)

def request_data(url: str):
    print('New data request')
    r = requests.get(url, timeout=5)
    if not r.status_code == 200:
        data = {'error': 'status',
                'status': r.status_code}
    else:
        try:
            data = r.json()
        except requests.RequestException as e:
            data = {'error': 'json_data',
                    'json_data': str(e)}
    return data


def read_data(file: Path):
    if file and file.is_file():
        try:
            data = json.load(file.open())
        except json.JSONDecodeError as e:
            data = {'error': 'json_error', 'json_error': str(e)}
            print(e)
        return data


def get_data(url: str, file: Path):
    data = read_data(file)
    if data:
        price_list = parse_data(data)
        times = [datetime.fromtimestamp(t / 1e3) for t in price_list.keys()]
        expiring = (datetime.now() - max(times)) > timedelta(hours=3)
    if not data or expiring:
        data = request_data(url)
    if file and data:
        with file.open('w') as fp:
            json.dump(data, fp)
    return data


def parse_data(data: dict):
    rows = data.get('data').get('Rows')
    price_list = {}
    for row in rows:
        if 'Columns' in row.keys():
            time_string = row.get('StartTime')
            if time_string:
                time_stamp = 1000 * \
                    datetime.strptime(time_string, time_fmt).timestamp()
                for cell in row.get('Columns'):
                    if cell.get('Name') == region:
                        try:
                            cell_str = cell['Value'].replace(',', '.')
                            cell_str = cell_str.replace(' ', '')
                            price = float(cell_str)/10.0 # data in kr/MWh
                        except ValueError as e:
                            price = None
                            print('Could not read price Value')
                            print(e)
                        price_list[time_stamp] = price
    return price_list


def to_time_series(price_list: dict) -> pd.Series:

    tuples = [(datetime.fromtimestamp(ts/1e3), v) 
              for ts, v in price_list.items()]
    index, values = list(zip(*tuples))

    return pd.Series(values, index=index)



def plot_prices(price_list: dict):
    def parse():
        for key, val in price_list.items():
            try:
                timestamp = float(key)
                date = datetime.fromtimestamp(timestamp / 1e3)
                date_str = date.strftime(time_fmt)
                print(f'{date_str} == {val}')
                yield date, val
            except ValueError as e:
                print('Price list parse error')
                print(e)

    unzipped = list(zip(*(parse())))
    plt.step(unzipped[0], unzipped[1], where='post')
    plt.grid()
    plt.show()


def main():
    data = get_data(url, local_cache)
    price_list = parse_data(data)
    print(json.dumps(price_list, indent=4))
    # plot_prices(price_list)
    series = to_time_series(price_list)
    print(series.to_json(indent=2))


if __name__ == '__main__':
    main()
