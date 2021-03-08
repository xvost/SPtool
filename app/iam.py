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
            print(oauth)
            print(self.oauth)
            url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
            data = {"yandexPassportOauthToken": oauth}
            data = json.dumps(data)
            req = requests.post(url, data=data)
            if req.status_code != 200:
                abort(req.status_code, req.text)
                #ToDo add logging
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
            abort(req.status_code, req.text)
            pass
            #Todo add warning and logging
        else:
            pass
            #ToDo add notice
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
            #ToDo add warning and logging
        else:
            pass
            #ToDo add notice
        reqdata = json.loads(req.text)
        self.apikeyid = reqdata["apiKey"]["id"]
        self.apikey = reqdata["secret"]
        return self.apikey


    def createstatickey(self, folderid=None, said=None):
        '''
        $ curl -X POST \
        -H 'Content-Type: application/json' \
        -H "Authorization: Bearer <IAM-TOKEN>" \
        -d '{
            "serviceAccountId": "aje6o61dvog2h6g9a33s",
            "description": "this key is for my bucket"
        }' \
        https://iam.api.cloud.yandex.net/iam/aws-compatibility/v1/accessKeys

            :return:
        '''
        if not folderid:
            folderid = self.folderid
        if not said:
            said = self.said
        url = 'https://iam.api.cloud.yandex.net/iam/aws-compatibility/v1/accessKeys'
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer {}".format(self.iamtoken)}
        jsondata = {'serviceAccountId': self.said,
                    'description': 'storage key for sptool'}

        req = requests.post(url, headers=headers, params=jsondata)
        staticid = req.json()['accessKey']['keyId']
        statickey = req.json()['secret']
        return staticid, statickey


    def deletesa(self, said=None, oauth=None):
        if not said:
            said = self.said
        token = self.getiamtokenoauth(oauth=oauth)
        url = f'https://iam.api.cloud.yandex.net/iam/v1/serviceAccounts/{said}'
        print(url)
        headers = {"Authorization": f"Bearer {token}"}
        req = requests.delete(url, headers=headers)
        if req.status_code != 200:
            abort(req.status_code, req.text)
            pass
            #ToDo add warning and logging
        else:
            pass
            #ToDo add notice
        pass

