import math
import json
import time
import requests
import fire
from tqdm import tqdm


class ESDump:
    def __init__(self, input, output, size=100, delay=1):
        self.input = input
        self.output = output
        self.size = size
        self.params = {"size": self.size, "sort": [{"_id": {"order": "asc"}}]}
        self.pages = 1
        self.delay = delay

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
        return r.json()["count"]

    def _write_values(self, data_list):
        with open(self.output, "a") as output_file:
            for d in data_list:
                output_file.write(json.dumps(d) + "\n")

    def _store_values(self, es_id, data):
        r_url = self.input + f"/_doc/{es_id}"
        headers = {"Content-type": "application/json"}
        r = requests.post(r_url, json=data, headers=headers)
        if r.status_code > 400:
            return f"failed: {es_id}"
        else:
            return f"success: {es_id}"

    def _load_to_es(self, data):
        while True:
            line = input_file.readline()
            if not line:
                print(f"finished restoring {self.input}")
                break
            json_data = json.loads(line)
            res = self._store_values(json_data["_id"], json_data["_source"])
            print(res)
        return True

    def restore(self):
        with open(self.input, "r") as input_file:
            self._load_to_es(input_file)

    def dump(self):
        num_entries = self._count_entries()
        self.pages = math.ceil(num_entries / self.size)
        params = None
        for p in tqdm(range(1, self.pages + 1)):
            time.sleep(self.delay)
            data = self._fetch_data(params)
            sort_id = data["hits"]["hits"][-1]["_id"]
            params = self.params.copy()
            params["search_after"] = [sort_id]
            self._write_values(data["hits"]["hits"])
        return f"{self.input} - {self.output}"


def main():
    fire.Fire(ESDump)
