import requests


class Client:


    def __init__(self):
        pass

    def set_photo_urls(self, url:str):
        response = requests.request(method="PUT",url="http://localhost:8000/photo", json={"url": url})
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

