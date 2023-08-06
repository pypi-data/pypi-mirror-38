# -*- coding: utf-8 -*-

from Misskey.Exceptions import *

import requests
import json
import pprint
import hashlib

from urllib.parse import urlparse

def isAdministrator(isAdminFlag):
    pass

class Misskey:
    """
    MISSKEY API LIBRARY
    """
    def __init__(self, instanceAddress='https://misskey.xyz', appSecret=None, accessToken=None, apiToken=None):
        """
        INITIALIZE LIBRARY

        Attribute:
        * : Required
        - instanceAddress : Instance Address
        - appSecret : Application Secret Key
        - accessToken : accessToken key from authorized api
        - apiToken : sha256 hashed from appSecret and accessToken (If this is set, we will preferentially use this.)
        """
        self.instanceAddress = instanceAddress
        self.appSecret = appSecret
        self.accessToken = accessToken
        self.apiToken = apiToken

        self.headers = {'content-type': 'application/json'}
        self.metaDic = None
        self.res = None

        if self.apiToken == None and self.appSecret != None and self.accessToken != None:
            tokenraw = self.accessToken + self.appSecret
            self.apiToken = hashlib.sha256(tokenraw.encode('utf-8')).hexdigest()

        ParseRes = urlparse(self.instanceAddress)
        if ParseRes.scheme == '':
            ParseRes = urlparse("https://{}".format(self.instanceAddress))
        self.PRscheme = ParseRes.scheme
        self.instanceAddressUrl = "{0}://{1}".format(self.PRscheme, ParseRes.netloc)
        self.instanceAddressApiUrl = self.instanceAddressUrl + "/api"

        meta = requests.post(self.instanceAddressApiUrl + "/meta")

        if meta.status_code != 200:
            raise MisskeyInitException("API Meta check failed: Server returned HTTP {}\nHave you entered an address that is not a Misskey instance?".format(meta.status_code))

        self.metaDic = json.loads(meta.text)

        if self.apiToken != None:
            self.credentials = self.i()

    def meta(self,useCache=False):
        """
        LOAD INSTANCE META INFORMATION
        """
        if useCache == True and self.metaDic != None:
            return self.metaDic

        self.res = requests.post(self.instanceAddressApiUrl + "/meta")
        if self.res.status_code != 200:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return json.loads(self.res.text)

    @classmethod
    def create_app(instanceAddress, appName, description, permission, callbackUrl=None):
        """
        CREATE APP FUNCTION

        Attribute:
        * : Required
        - appName * : Application's Name
        - description * : Application's Description
        - permission * : Application's Permission (See "Available Permissions" Section)
        - callbackUrl : Application's Callback URL

        Return:
        - Responce (type: dict)

        Avaliable Permissions:
        - account-read
        - account-write
        - note-read
        - note-write
        - reaction-read
        - reaction-write
        - following-read
        - following-write
        - drive-read
        - drive-write
        - notification-read
        - notification-write
        - favorite-read
        - favorites-read
        - favorite-write
        - account/read
        - account/write
        - messaging-read
        - messaging-write
        - vote-read
        - vote-write
        """
        headers = {'content-type': 'application/json'}

        ParseRes = urlparse(instanceAddress)
        if ParseRes.scheme == '':
            ParseRes = urlparse("https://{}".format(instanceAddress))
        PRscheme = ParseRes.scheme
        instanceAddressUrl = "{0}://{1}".format(PRscheme, ParseRes.netloc)
        instanceAddressApiUrl = instanceAddressUrl + "/api"

        payload = {'name': appName, 'description': description, 'permission': permission, 'callbackUrl': callbackUrl}

        app = requests.post(instanceAddressApiUrl + "/app/create", data=json.dumps(payload), headers=headers)
        appjson = json.loads(app.text)

        if app.status_code != 200:
            if app.status_code == 400:
                raise MisskeyBadRequestException("Server returned HTTP 400: code: {0}, param: {1}, reason: {2}".format(appjson['error']['code'], appjson['error']['param'], appjson['error']['reason']))
            else:
                raise MisskeyResponseException("Server returned HTTP {}\nHave you entered an address that is not a Misskey instance?".format(app.status_code))

        return appjson

    @classmethod
    def auth_session_generate(instanceAddress, appSecret):
        """
        AUTHORIZE APPLICATION

        Attribute: 
        - instanceAddress * : Instance Address
        - appSecret * : Application Secret Key
        """
        headers = {'content-type': 'application/json'}

        ParseRes = urlparse(instanceAddress)
        if ParseRes.scheme == '':
            ParseRes = urlparse("https://{}".format(instanceAddress))
        PRscheme = ParseRes.scheme
        instanceAddressUrl = "{0}://{1}".format(PRscheme, ParseRes.netloc)
        instanceAddressApiUrl = instanceAddressUrl + "/api"

        payload = {'appSecret': appSecret}

        auth = requests.post(instanceAddressApiUrl + "/auth/session/generate", data=json.dumps(payload), headers=headers)
        authjson = json.loads(auth.text)

        if auth.status_code != 200:
            if auth.status_code == 400:
                raise MisskeyBadRequestException("Server returned HTTP 400: {}".format(authjson['error']))
            else:
                raise MisskeyResponseException("Server returned HTTP {}\nHave you entered an address that is not a Misskey instance?".format(auth.status_code))

        return authjson

    @classmethod
    def auth_session_userkey(instanceAddress, appSecret, token):
        """
        CHECK AUTHORIZED TOKEN

        Attribute:
        - instanceAddress * : Instance Address
        - appSecret * : Application Secret Key
        - token * : authorize token

        Return:
        - authorizejson (type: dict)
        """
        headers = {'content-type': 'application/json'}
        ParseRes = urlparse(instanceAddress)
        if ParseRes.scheme == '':
            ParseRes = urlparse("https://{}".format(instanceAddress))
        PRscheme = ParseRes.scheme
        instanceAddressUrl = "{0}://{1}".format(PRscheme, ParseRes.netloc)
        instanceAddressApiUrl = instanceAddressUrl + "/api"

        payload = {'appSecret': appSecret, 'token': token}

        authorize = requests.post(instanceAddressApiUrl + "/auth/session/userkey", data=json.dumps(payload), headers=headers)
        authorizejson = json.loads(authorize.text)
        if authorize.status_code != 200:
            if authorize.status_code == 400:
                raise MisskeyBadRequestException("Server returned HTTP 400: {}".format(authorizejson['error']))
            else:
                raise MisskeyResponseException("Server returned HTTP {}\nHave you entered an address that is not a Misskey instance?".format(authorize.status_code))

        return authorizejson

    def i(self, useCache=False):
        """
        RETURNS YOUR CREDENTIAL

        Attribute:
        - useCache : use from class variable
        Return:
        - res (type: dict)
        """

        if useCache == True:
            return self.credentials

        self.res = requests.post(self.instanceAddressApiUrl + "/i", data=json.dumps({'i': self.apiToken}), headers=self.headers)

        if self.res.status_code != 200:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        self.credentials = json.loads(self.res.text)
        return json.loads(self.res.text)

    def notes_create(self, body, cw=None, visibility='public', visibleUserIds=None, viaMobile=False, geo=None, fileIds=None, replyId=None, renoteId=None):
        """
        POST NOTE

        Attribute:
        - body * : Note body
        - cw : Content Warning
        - visibility : visibility
        - viaMobile : Is it mark as Mobile
        """
        payload = {'i': self.apiToken, 'text': body, 'cw': cw, 'visibility': visibility, 'viaMobile': viaMobile, 'geo': geo}

        if visibleUserIds != None:
            payload['visibleUserIds'] = visibleUserIds

        if fileIds != None:
            payload['fileIds'] = fileIds

        if replyId != None:
            payload['replyId'] = replyId

        if renoteId != None:
            payload['renoteId'] = renoteId

        self.res = requests.post(self.instanceAddressApiUrl + "/notes/create", data=json.dumps(payload), headers=self.headers)

        if self.res.status_code != 200:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return json.loads(self.res.text)

    def notes_renote(self, renoteId):
        """
        RENOTE FUNCTION

        Attribute:
        - renoteId : ID of will renote
        """
        payload = {'i': self.apiToken, 'renoteId': renoteId}
        self.res = requests.post(self.instanceAddressApiUrl + "/notes/create", data=json.dumps(payload), headers=self.headers)

        if self.res.status_code != 200:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return json.loads(self.res.text)

    def notes_show(self, noteId):
        """
        POST SHOW
        
        Attribute:
        noteId * : Note ID
        """
        payload = {'i': self.apiToken, 'noteId': noteId}
        self.res = requests.post(self.instanceAddressApiUrl + "/notes/show", data=json.dumps(payload), headers=self.headers)

        if self.res.status_code != 200:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return json.loads(self.res.text)

    def notes_delete(self, noteId):
        """
        POST SHOW

        Attribute:
        - noteId * : Note ID

        Return:
        - [boolean] (True: success)
        """
        payload = {'i': self.apiToken, 'noteId': noteId}
        self.res = requests.post(self.instanceAddressApiUrl + "/notes/delete", data=json.dumps(payload), headers=self.headers)

        if self.res.status_code != 204:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return True

    def notes_conversation(self, noteId, limit=None, offset=None):
        """
        POST SHOWS NOTES CONVERSATION

        Attribute:
        - noteId * : Note ID
        - limit : recieve limit
        - offset : pagenation
        """
        payload = {'noteId': noteId}

        if limit != None:
            payload['limit'] = int(limit)

        if offset != None:
            payload['offset'] = int(offset)

        self.res = requests.post(self.instanceAddressApiUrl + "/notes/conversation", data=json.dumps(payload), headers=self.headers)

        if self.res.status_code != 200:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return json.loads(self.res.text)

    def notes_reactions(self, noteId, limit=None, offset=None):
        """
        POST SHOW REACTIONS

        Attribute:
        - noteId * : Note ID
        - limit : recieve limit
        - offset : pagenation
        """
        payload = {'noteId': noteId}

        if limit != None:
            payload['limit'] = int(limit)

        if offset != None:
            payload['offset'] = int(offset)

        self.res = requests.post(self.instanceAddressApiUrl + "/notes/reactions", data=json.dumps(payload), headers=self.headers)

        if self.res.status_code != 200:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return json.loads(self.res.text)

    def notes_reactions_create(self, noteId, reaction='pudding'):
        """
        CREATE REACTION

        Attribute:
        - noteId * : Note ID
        - reaction : to send reaction
        """
        payload = {'i': self.apiToken, 'noteId': noteId, 'reaction': reaction}
        self.res = requests.post(self.instanceAddressApiUrl + "/notes/reactions/create", data=json.dumps(payload), headers=self.headers)

        if self.res.status_code != 204:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return True

    def notes_reactions_delete(self, noteId):
        """
        CREATE REACTION

        Attribute:
        - noteId * : Note ID
        - reaction : to send reaction
        """
        payload = {'i': self.apiToken, 'noteId': noteId}
        self.res = requests.post(self.instanceAddressApiUrl + "/notes/reactions/delete", data=json.dumps(payload), headers=self.headers)

        if self.res.status_code != 204:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return True

    def local_timeline(self, withFiles=False, fileType=None, excludeNsfw=False, limit=None, offset=None, sinceId=None, untilId=None, sinceDate=None, untilDate=None):
        """
        READ TIMELINE OF LOCAL

        Attribute:
        - withFiles : show only include files
        - fileType : fileType dict
        - excludeNsfw : Don't show if it has NSFW flag
        - limit : receive limit
        - offset : pagination
        - sinceId : Since Note Id
        - untilId : Until Note Id
        - sinceDate : Since Date
        - untilDate : Until Date
        """
        payload = {'i': self.apiToken, 'excluceNsfw': excludeNsfw, 'withFiles': withFiles}

        if fileType != None:
            payload['fileType'] = fileType

        if limit != None:
            payload['limit'] = int(limit)

        if offset != None:
            payload['offset'] = int(offset)

        if sinceId != None:
            payload['sinceId'] = str(sinceId)

        if untilId != None:
            payload['untilId'] = str(untilId)

        if sinceDate != None:
            payload['sinceDate'] = int(sinceDate)

        if untilDate != None:
            payload['untilDate'] = int(untilDate)


        self.res = requests.post(self.instanceAddressApiUrl + "/notes/local-timeline", data=json.dumps(payload), headers=self.headers)

        if self.res.status_code != 200:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return json.loads(self.res.text)

    def global_timeline(self, withFiles=False, fileType=None, excludeNsfw=False, limit=None, offset=None, sinceId=None, untilId=None, sinceDate=None, untilDate=None):
        """
        READ TIMELINE OF GLOBAL

        Attribute:
        - withFiles : show only include files
        - fileType : fileType dict
        - excludeNsfw : Don't show if it has NSFW flag
        - limit : receive limit
        - offset : pagination
        - sinceId : Since Note Id
        - untilId : Until Note Id
        - sinceDate : Since Date
        - untilDate : Until Date
        """
        payload = {'i': self.apiToken, 'excludeNsfw': excludeNsfw, 'withFiles': withFiles}

        if fileType != None:
            payload['fileType'] = fileType

        if limit != None:
            payload['limit'] = int(limit)

        if offset != None:
            payload['offset'] = int(offset)

        if sinceId != None:
            payload['sinceId'] = str(sinceId)

        if untilId != None:
            payload['untilId'] = str(untilId)

        if sinceDate != None:
            payload['sinceDate'] = int(sinceDate)

        if untilDate != None:
            payload['untilDate'] = int(untilDate)


        self.res = requests.post(self.instanceAddressApiUrl + "/notes/global-timeline", data=json.dumps(payload), headers=self.headers)

        if self.res.status_code != 200:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return json.loads(self.res.text)

    def hybrid_timeline(self, withFiles=False, fileType=None, excludeNsfw=False, limit=None, offset=None, sinceId=None, untilId=None, sinceDate=None, untilDate=None, includeMyRenotes=True, includeRenotedMyNotes=True, includeLocalRenotes=True):
        """
        READ TIMELINE OF HYBRID(SOCIAL)

        Attribute:
        - withFiles : show only include files
        - fileType : fileType dict
        - excludeNsfw : Don't show if it has NSFW flag
        - limit : receive limit
        - offset : pagination
        - sinceId : Since Note Id
        - untilId : Until Note Id
        - sinceDate : Since Date
        - untilDate : Until Date
        - includeMyRenotes : include My Notes
        - includeRenotedMyNotes : include renoted my notes
        - includeLocalRenotes: include local renotes
        """
        payload = {'i': self.apiToken, 'withFiles': withFiles, 'excludeNsfw': excludeNsfw, 'includeMyRenotes': includeMyRenotes, 'includeRenotedMyNotes': includeMyRenotes, 'includeLocalRenotes': includeLocalRenotes}

        if fileType != None:
            payload['fileType'] = fileType

        if limit != None:
            payload['limit'] = int(limit)

        if offset != None:
            payload['offset'] = int(offset)

        if sinceId != None:
            payload['sinceId'] = str(sinceId)

        if untilId != None:
            payload['untilId'] = str(untilId)

        if sinceDate != None:
            payload['sinceDate'] = int(sinceDate)

        if untilDate != None:
            payload['untilDate'] = int(untilDate)


        self.res = requests.post(self.instanceAddressApiUrl + "/notes/hybrid-timeline", data=json.dumps(payload), headers=self.headers)

        if self.res.status_code != 200:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return json.loads(self.res.text)

    def timeline(self, withFiles=False, fileType=None, excludeNsfw=False, limit=None, offset=None, sinceId=None, untilId=None, sinceDate=None, untilDate=None, includeMyRenotes=True, includeRenotedMyNotes=True, includeLocalRenotes=True):
        """
        READ TIMELINE OF HOME

        Attribute:
        - withFiles : show only include files
        - fileType : fileType dict
        - excludeNsfw : Don't show if it has NSFW flag
        - limit : receive limit
        - offset : pagination
        - sinceId : Since Note Id
        - untilId : Until Note Id
        - sinceDate : Since Date
        - untilDate : Until Date
        - includeMyRenotes : include My Notes
        - includeRenotedMyNotes : include renoted my notes
        - includeLocalRenotes: include local renotes
        """
        payload = {'i': self.apiToken, 'withFiles': withFiles, 'excludeNsfw': excludeNsfw, 'includeMyRenotes': includeMyRenotes, 'includeRenotedMyNotes': includeMyRenotes, 'includeLocalRenotes': includeLocalRenotes}

        if fileType != None:
            payload['fileType'] = fileType

        if limit != None:
            payload['limit'] = int(limit)

        if offset != None:
            payload['offset'] = int(offset)

        if sinceId != None:
            payload['sinceId'] = str(sinceId)

        if untilId != None:
            payload['untilId'] = str(untilId)

        if sinceDate != None:
            payload['sinceDate'] = int(sinceDate)

        if untilDate != None:
            payload['untilDate'] = int(untilDate)


        self.res = requests.post(self.instanceAddressApiUrl + "/notes/timeline", data=json.dumps(payload), headers=self.headers)

        if self.res.status_code != 200:
            raise MisskeyResponseException("Server returned HTTP {}".format(self.res.status_code))

        return json.loads(self.res.text)