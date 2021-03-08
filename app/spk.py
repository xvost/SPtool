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
                "voice": voice,
                "speed": speed,
                "folderId": self.folderid}
        with requests.post(url, headers=headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
            with open(file, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=None):
                    print(len(chunk))
                    f.write(chunk)

    def stt_short(self, filepath: str, params: dict):
        with open(filepath, "rb") as f:
            data = f.read()
        if params.get('format') == 'Opus':
            params['format'] = 'oggopus'
        else:
            params['format'] = 'lpcm'
        headers = {"Authorization": "Api-Key {}".format(self.apikey)}
        req = requests.post('https://stt.api.cloud.yandex.net/speech/v1/stt:recognize',
                            headers=headers,
                            params=params,
                            data=data)
        if req.status_code != 200 or req.json().get("error_code"):
            return req.status_code, req.text
        else:
            return req.json().get("result")

    def stt_long(self, url, params):
        return 'Not implemented'
