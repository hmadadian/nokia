import requests
import json


class Http2Json:
    def __init__(self):
        self.__headers = {
            'authority': 'www.convertonline.io',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
            'dnt': '1',
            'origin': 'https://www.convertonline.io',
            'referer': 'https://www.convertonline.io/convert/query-string-to-json',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' +
                          '102.0.0.0 Safari/537.36',
        }

    def convert(self, data):
        json_data = {'payload': data}
        response = requests.post('https://www.convertonline.io/api/qs-2-json', headers=self.__headers, json=json_data)
        if json.loads(response.text)["ok"]:
            m = json.loads(response.text)["content"]
            return m
        else:
            return False
