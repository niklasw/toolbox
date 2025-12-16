#!/usr/bin/env python3

import requests
import json
from pathlib import Path
from datetime import datetime, timedelta
from dateutil import tz, parser
import pytz
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import pandas as pd


class SpotpriceRequest:
    TIME_ZONE = 'Europe/Stockholm'
    TZ = tz.gettz(TIME_ZONE)
    pyTZ = pytz.timezone(TIME_ZONE)
    time_fmt = "%Y-%m-%dT%H:%M:%S"  # "2023-05-29T11:00:00"
    region = 'SE3'
    cache = Path('/tmp/spotprice.json')

    def __init__(self):
        self.price_list: pd.Series = None

    def request(self, from_file: Path = None):
        print('Requesting new data')
        try:
            r = requests.get(self.url, timeout=5)
        except:
            return None
        if not r.status_code == 200:
            info = {'error': 'status',
                    'status': r.status_code}
            print(json.dumps(info))
            return None
        else:
            try:
                data = r.json()
            except requests.RequestException as e:
                info = {'error': 'json_data',
                        'json_data': str(e)}
                print(json.dumps(info))
                return None
        return data

    def cache_read(self):
        try:
            p = pd.read_json(self.cache, typ='series').tz_localize('UTC')
            return p.tz_convert(self.TZ)
        except Exception as e:
            print(e)
            print('cache_read failed')

    def cache_write(self):
        if self.price_list is not None:
            try:
                self.price_list.to_json(self.cache)
            except Exception as e:
                print(e)
                print('cache_write failed')

    def fetch_prices(self):
        import sys
        self.price_list = self.cache_read()
        if self.price_list is None:
            self.parse_data(self.request())
            self.cache_write()
        else:
            cache_left = max(self.price_list.index) - datetime.now(self.TZ)
            if cache_left < timedelta(hours=8):
                self.parse_data(self.request())
                self.cache_write()
        return self.price_list



class Elprisetjustnu(SpotpriceRequest):
    """
    request delivers json as a list of elements like:
    {
      "SEK_per_kWh": 1.10534,
      "EUR_per_kWh": 0.0979,
      "EXR": 11.290508,
      "time_start": "2023-12-07T20:00:00+01:00",
      "time_end": "2023-12-07T21:00:00+01:00"
    }
    URL path is on format
    https://www.elprisetjustnu.se/api/v1/prices/2023/12-07_SE3.json
    """
    url = "https://www.elprisetjustnu.se/api/v1/prices"
    cache = Path('/tmp/elprisetjustnu.json')


    def __init__(self, when=datetime.now()):
        super().__init__()
        path=when.strftime(f'%Y/%m-%d_{self.region}.json')
        self.url = f'{self.url}/{path}'

    def parse_data(self, data: list = None):
        if not data:
            return
        if self.price_list is None:
            self.price_list = pd.Series()
        if isinstance(data, list):
            for item in data:
                try:
                    sek = float(item.get('SEK_per_kWh'))
                except:
                    print('Elprisetjustnu parse value error')
                    sek = None
                time_str = item.get('time_start')
                try:
                    time = parser.parse(time_str)
                except:
                    print('Elprisetjustnu parse time error')
                    time = None

                if sek and time:
                    self.price_list[time] = sek*100
        else:
            raise(ValueError)



class Nordpool(SpotpriceRequest):
    url = "https://www.nordpoolgroup.com/api/marketdata/page/10"
    url += "?currency=SEK,SEK,SEK,SEK"
    cache = Path('/tmp/nordpool.json')

    def __init__(self):
        super().__init__()

    def parse_data(self, data: dict):
        if not data:
            return
        if self.price_list is None:
            self.price_list = pd.Series()
        rows = data.get('data').get('Rows')
        for row in rows:
            if 'Columns' in row.keys():
                time_string = row.get('StartTime')
                measurementName = row.get('Name')
                if time_string and '&' in measurementName:
                    time = self.pyTZ.localize(parser.parse(time_string))
                    for cell in row.get('Columns'):
                        if cell.get('Name') == self.region:
                            try:
                                cell_str = cell['Value'].replace(',', '.')
                                cell_str = cell_str.replace(' ', '')
                                price = float(cell_str)/10.0 # data in kr/MWh
                            except ValueError as e:
                                price = None
                                print('Could not read price Value')
                                print(e)
                            self.price_list[time] = price


def main(plot=False):
    service = Nordpool()
    prices = service.fetch_prices()

    service2 = Elprisetjustnu()
    prices2 = service2.fetch_prices()
    service2 = Elprisetjustnu(datetime.now()+timedelta(days=1))
    prices2._append(service2.fetch_prices())

    if plot:
        all_prices = pd.concat([prices, prices2], axis=1)
        ax = all_prices.plot(drawstyle="steps-post", linewidth=2)

        now = datetime.now(SpotpriceRequest.TZ)
        now_line = lines.Line2D([now,now], [0,300], linewidth=1)
        ax.add_line(now_line)

        plt.grid(True)
        plt.show()
        print(all_prices)


def test():
    pass

if __name__ == '__main__':
    import sys
    from time import sleep
    try:
        loop = sys.argv[1] == 'daemon'
    except:
        loop = False
        pass

    if loop:
        while True:
            sleep(10)
            main()
            sleep(3600*1)
    else:
        main(True)
