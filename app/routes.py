# -*- coding: utf-8 -*-
import os

from app import app
from app.forms import *
from app.spk import *
from app.iam import *
from app.models import *
from app.storage import Storage
from app.config import Config
from datetime import datetime
from flask import send_from_directory, abort
from flask import render_template, request, redirect
from pymediainfo import MediaInfo

speechkit = Speech()
iam = IamApi()
storage = Storage()

@app.route('/')
@app.route('/index')
def index():
    accounts = db.session.query(Iam).all()
    if accounts:
        accounts = 1
    else:
        accounts = 0
    return render_template('index.html',
                           title='Main',
                           state=accounts)


@app.route('/settings', methods=['GET', 'POST'])
def config():
    form = SettingsForm()
    accounts = db.session.query(Iam).all()
    select = [{'id': account.id, 'name': account.name}
              for account in accounts]
    if form.validate_on_submit():
        oauth = form.oauth.data
        folderid = form.folderid.data
        name = form.name.data
        cloudiam = IamApi(oauth=oauth, folderid=folderid)
        cloudiam.getiamtokenoauth()
        serviceaccount = cloudiam.createsa()
        cloudiam.seteditorsa()
        apikey = cloudiam.createapikey()
        staticid, statickey = cloudiam.createstatickey()
        iambase = Iam(name=name,
                      folderid=folderid,
                      said=serviceaccount,
                      keyid=cloudiam.apikeyid,
                      key=apikey,
                      date=datetime.now(),
                      statickey=statickey,
                      staticid=staticid
                      )
        db.session.add(iambase)
        db.session.commit()
        return render_template('settings.html',
                               title='Main',
                               form=form,
                               salist=select,
                               state=1)
    else:
        accounts = db.session.query(Iam).all()
        if accounts:
            accounts = 1
        else:
            accounts = 0
        return render_template('settings.html',
                               title='Main',
                               form=form,
                               state=accounts,
                               salist=select,)


@app.route('/stt', methods=['GET', 'POST'])
def stt():
    accounts = db.session.query(Iam).all()
    select = [(account.id, account.name) for account in accounts]
    form = SttForm()
    form.account.choices = select
    if form.validate_on_submit():
        account = form.account.data
        f = form.pathtofile.data
        fname = f.filename
        path = os.path.join(Config.UPLOAD, fname)
        f.save(path)
        mediainfo = MediaInfo.parse(path)
        for track in mediainfo.tracks:
            if track.track_type == "Audio":
                if track.format not in ['Opus', 'Wav', 'LPCM']:
                    abort(400, 'Wrong audio format')
                params = {'channels': track.channel_s,
                          'format': track.format,
                          'duration': track.duration,
                          'sampleRateHertz': track.sampling_rate}
            elif track.track_type == "General":
                pass
            else:
                abort(500, 'Wrong file format')
        apikey = db.session.query(Iam.key).filter(Iam.id == account)[0][0]
        speechkit.setauth(apikey=apikey)
        if params['duration'] < 30000:
            response = speechkit.stt_short(path, params)
            print(response)
            return render_template('stt.html', title='Main', form=form, text=response)
        else:
            storage.statickey, storage.statickeyid = db.session.query(Iam.statickey,
                                                                      Iam.staticid).filter(Iam.id == account)[0]
            response = storage.putfile(path, filename=fname)
            if response:
                response = speechkit.stt_long(response.get('url'), params)
                return render_template('stt.html', title='Main', form=form, text=response)
            else:
                abort(500, response)
        return render_template('stt.html', title='Main', form=form)
    else:
        return render_template('stt.html', title='Main', form=form)


@app.route('/tts', methods=['GET', 'POST'])
def tts():
    accounts = db.session.query(Iam).all()
    select = [(account.id, account.name) for account in accounts]
    form = TtsForm()
    form.account.choices = select
    form.voice.choices = [(v, '{v}_{lang}'.format(v=v, lang=Config.voices[v]['lang']))
                          for v in Config.voices.keys()]
    form.speed.choices = []
    files = os.listdir(Config.FILEPATH)
    if form.validate_on_submit():
        text = form.text.data
        account = form.account.data
        speed = form.speed.data
        lang = Config.voices[form.voice.data]['lang']
        voice = form.voice.data
        filename = str(datetime.timestamp(datetime.now()))
        fullpath = Config.FILEPATH + '\\' + filename
        apikey, folderid = db.session.query(Iam.key, Iam.folderid).filter(Iam.id == account)[0]
        speechkit.setauth(apikey=apikey, folderid=folderid)
        speechkit.tts(text=text,
                      lang=lang,
                      speed=speed,
                      voice=voice,
                      file=fullpath)
        return redirect('/tts')
    return render_template('tts.html', title='Main', form=form, files=files)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


@app.route('/files/<name>', methods=['GET'])
def getfiles(name=None):
    return send_from_directory(Config.CURENT_DIR+'\\files\\', name)


@app.route('/settings/deletesa/<said>', methods=['DELETE'])
def deletesa(said=None):
    try:
        said = Iam.query.get(said)
        oauth = request.args['oauth']
        iam.oauth = oauth
        iam.deletesa(said=said.said)
        db.session.delete(said)
        db.session.commit()
        return (f'Аккаунт {said.name} удален', 200)
    except db.exc as error:
        abort(500, error)
