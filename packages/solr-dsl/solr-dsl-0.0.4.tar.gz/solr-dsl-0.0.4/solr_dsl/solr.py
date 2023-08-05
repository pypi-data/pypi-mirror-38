import requests


class Solr:

    def __init__(self, hostport, collection):
        self.hostport = hostport
        self.collection = collection

    def add(self, documents):
        """Document may be a list of doucments or a single document."""
        url = self.make_url()
        params = {'commit': 'true'}
        response = requests.post(url, params=params, json=documents)
        response.raise_for_status()
        return response

    def make_url(self):
        return f'http://{self.hostport}/solr/{self.collection}/update'
