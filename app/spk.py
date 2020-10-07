import requests


class Speech:
    def __init__(self, apikey=None, folderid=None):
        self.apikey = apikey
        self.folderid = folderid

    def setauth(self, apikey=None, folderid=None):
        self.apikey = apikey
        self.folderid = folderid

    def tts(self, text='',
            lang='ru-RU',
            file=None,
            speed=1,
            voice=None):
        url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
        headers = {"Authorization": "Api-Key {}".format(self.apikey)}
        data = {"text": text,
                "lang": lang,
                "folderId": self.folderid}
        with requests.post(url, headers=headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
            with open(file, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=None):
                    print(len(chunk))
                    f.write(chunk)

