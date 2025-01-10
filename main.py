import requests
import ipaddress
import random
import time
from pyquery import PyQuery as pq
import traceback
import sys
import argparse

CR = '--------------------------------------------------------------------------------------------------------------------------\r'

s = requests.session()
s.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}


def generate_form_data(html: pq, ip_address: ipaddress.IPv4Address, isRetry=False):

    form_data = {}

    for node in html('#form1 input[type=hidden]').items():
        form_data[node.attr('name')] = node.attr('value')

    if isRetry:
        form_data['btninfo'] = '   정   보   '
    else:
        form_data['txtAddr'] = ip_address
        form_data['btnAddr2.x'] = random.randrange(0, 68)
        form_data['btnAddr2.y'] = random.randrange(0, 20)

    return form_data


def ip_location(ip: str) -> None:
    ip_address = ipaddress.ip_address(ip)

    with s.get('https://mylocation.co.kr/') as r1:
        time.sleep(3.5)  # 3초 딜레이 없으면 리턴 지랄남

        with s.post(
            'https://mylocation.co.kr/',
            data=generate_form_data(pq(r1.text), ip_address),
        ) as r2:
            lbInfomation = pq(r2.text)('#lbInfomation')

            if not lbInfomation:
                with s.post(
                    'https://mylocation.co.kr/',
                    data=generate_form_data(pq(r2.text), ip_address, True),
                ) as r3:
                    lbInfomation = pq(r3.text)('#lbInfomation')

            lines = (
                lbInfomation.text()
                .replace(f'.'.join(ip.split('.')[:2]) + '.*.*', ip)
                .split('\n')
            )
            entry = lines.index(CR)
            lines.pop(entry)

            print(CR)
            print('\n'.join(lines[entry : lines.index(CR)]))
            print(CR)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='mylocation.co.kr client')
    parser.add_argument("-i", "--ip", required=True)
    args = parser.parse_args()
    print(args)
    ip_location(args.ip)
