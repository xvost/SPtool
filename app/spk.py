import requests
import os
from app.config import Config
from app.workers import *


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
        count = 1
        print(file)
        url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
        headers = {"Authorization": "Api-Key {}".format(self.apikey)}
        for sentence in text_prepare(text):
            data = {"text": sentence,
                    "lang": lang,
                    "voice": voice,
                    "speed": speed,
                    "folderId": self.folderid}
            with requests.post(url, headers=headers, data=data, stream=True) as resp:
                if resp.status_code != 200:
                    raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
                with open(f'{file}_{count}', 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=None):
                        f.write(chunk)
            count += 1
        with open("filelist.txt", "w") as f:
            for i in range(1, count + 1):
                filename = f'{file}_{i}'
                try:
                    open(filename, 'r')
                    line = f"file '{filename}'\n"
                except:
                    pass
                f.write(line)
        os.system(f"{Config.ffmpeg} -safe 0 -f concat -i filelist.txt -c copy {file}.ogg")
        os.remove('filelist.txt')
        for i in range(1, count + 1):
            filename = f'{file}_{i}'
            try:
                os.remove(filename)
            except:
                pass

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

    def stt_long_create(self, url, params):
        return 'Not implemented'

    def stt_long_result(self, url, params):
        return 'Not implemented'