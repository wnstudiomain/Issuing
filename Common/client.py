import requests


class APIClient:

    def __init__(self, base_path):
        self.base_path = base_path

    def make_url(self, path):
        return '/'.join([self.base_path, path])

    def post(self, path=None, params=None, json=None, headers=None, auth=None):
        url = self.make_url(path)
        return requests.post(url=url, params=params, json=json, headers=headers, auth=auth)

    def put(self, path=None, params=None, json=None, headers=None, auth=None):
        url = self.make_url(path)
        return requests.put(url=url, params=params, json=json, headers=headers, auth=auth)

    def get(self, path=None, params=None, auth=None):
        url = self.make_url(path)
        return requests.get(url=url, params=params, auth=auth)
