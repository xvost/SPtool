import requests
import json
import uuid
from flask import abort

class IamApi:
    def __init__(self, oauth=None, folderid=None):
        self.oauth = oauth
        self.expireat = None
        self.iamtoken = None
        self.said = None
        self.folderid = folderid
        self.apikeyid = None
        self.apikey = None

    def getiamtokenoauth(self, oauth=None):
        if not oauth:
            oauth = self.oauth
        if self.iamtoken:
            iamtoken = self.iamtoken
        else:
            url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
            data = {"yandexPassportOauthToken": oauth}
            data = json.dumps(data)
            req = requests.post(url, data=data)
            if req.status_code != 200:
                abort(req.status_code, req.text)
                # add logging
            reqdata = json.loads(req.text)
            expireat = reqdata['expiresAt']
            self.expireat = expireat
            iamtoken = reqdata['iamToken']
            self.iamtoken = iamtoken
        return iamtoken

    def createsa(self, folderid=None):
        if not folderid:
            folderid = self.folderid
        url = 'https://iam.api.cloud.yandex.net/iam/v1/serviceAccounts'
        speechkit = uuid.uuid4()

        data = {
            "folderId": folderid,
            "name": f"speechkit-{speechkit}",
            "description": "created by sptool"
        }
        data = json.dumps(data)
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {self.iamtoken}"}
        req = requests.post(url, data=data, headers=headers)
        reqdata = json.loads(req.text)
        print(reqdata)
        operationid = reqdata["id"]
        url = 'https://operation.api.cloud.yandex.net/operations/{}'
        headers = {'Authorization': f"Bearer {self.iamtoken}"}
        req = requests.get(url.format(operationid), headers=headers)
        reqdata = json.loads(req.text)
        said = reqdata['metadata']['serviceAccountId']
        self.said = said
        return said

    def seteditorsa(self, folderid=None, said=None):
        if not folderid:
            folderid = self.folderid
        if not said:
            said = self.said
        url = "https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders/{}:updateAccessBindings"
        body = {
            "accessBindingDeltas": [{
                "action": "ADD",
                "accessBinding": {
                    "roleId": "editor",
                    "subject": {
                        "id": self.said,
                        "type": "serviceAccount"
                        }
                }
        }]
        }
        data = json.dumps(body)
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer {}".format(self.iamtoken)}
        req = requests.post(url=url.format(self.folderid), headers=headers, data=data)
        if req.status_code != 200:
            pass
            #add warning and logging
        else:
            pass
            #add notice
        return None

    def createapikey(self, folderid=None, said=None, apikey=None):
        if not folderid:
            folderid = self.folderid
        if not said:
            said = self.said
        url = "https://iam.api.cloud.yandex.net/iam/v1/apiKeys"
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer {}".format(self.iamtoken)}
        data = {"serviceAccountId": self.said}
        data = json.dumps(data)
        req = requests.post(url=url.format(folderid), headers=headers, data=data)
        if req.status_code != 200:
            pass
            # add warning and logging
        else:
            pass
            # add notice
        reqdata = json.loads(req.text)
        self.apikeyid = reqdata["apiKey"]["id"]
        self.apikey = reqdata["secret"]
        return self.apikey

    def deletesa(self, said=None, oauth=None):
        if not said:
            said = self.said
        token = self.getiamtokenoauth(oauth=oauth)
        url = f'https://iam.api.cloud.yandex.net/iam/v1/serviceAccounts/{said}'
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}
        req = requests.delete(url, headers=headers)
        if req.status_code != 200:
            abort(req.status_code, req.text)
            pass
            # add warning and logging
        else:
            pass
            # add notice
        pass
