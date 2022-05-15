import math
import json
import time
import requests
import fire
from tqdm import tqdm


class ESDump:
    def __init__(self, input, output, size=100):
       self.input = input
       self.output = output
       self.size = size
       self.params = {
           "size": self.size,
           "sort": [{"_id": {"order": "asc"}}]
       }
       self.pages = 1

    def _fetch_data(self, params=None):
        if params is None:
            params = self.params
        r_url = self.input + "/_search"
        headers = {"Content-type": "application/json"}
        r = requests.get(r_url, json=params, headers=headers)
        return r.json()

    def _count_entries(self):
        r_url = self.input + "/_count"
        r = requests.get(r_url)
        return r.json()['count']

    def _write_values(self, data_list):
        with open(self.output, "a") as output_file:
            for d in data_list:
                output_file.write(json.dumps(d) + "\n")

    def esdump(self):
        num_entries = self._count_entries()
        self.pages = math.ceil(num_entries / self.size)
        params = None
        for p in tqdm(range(1, self.pages + 1)):
            time.sleep(1)
            data = self._fetch_data(params)
            sort_id = data['hits']['hits'][-1]['_id']
            params = self.params.copy()
            params["search_after"] = [sort_id]
            self._write_values(data["hits"]["hits"])
        return f"{self.input} - {self.output}"


def main():
    fire.Fire(ESDump)

