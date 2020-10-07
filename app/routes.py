# -*- coding: utf-8 -*-
import os

from app import app
from app.forms import *
from app.spk import *
from app.iam import *
from app.models import *
from app.config import Config
from datetime import datetime
from flask import send_from_directory, abort
from flask import render_template, request, redirect

speechkit = Speech()

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
        iambase = Iam(name=name,
                      folderid=folderid,
                      said=serviceaccount,
                      keyid=cloudiam.apikeyid,
                      key=apikey,
                      date=datetime.now()
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
    form = SttForm()
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
        voice = Config.voices[form.voice.data]
        filename = str(datetime.timestamp(datetime.now()))+'.ogg'
        fullpath = Config.FILEPATH + '\\' + filename
        print(speed, lang, voice)
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
    return send_from_directory('..\\files\\', name)


@app.route('/settings/deletesa/<said>', methods=['GET'])
def deletesa(said=None):
    try:
        said = Iam.query.get(said)
        oauth = request.args['oauth']
        iamapi = IamApi(oauth=oauth)
        iamapi.deletesa(said=said.said)
        db.session.delete(said)
        db.session.commit()
        return (f'Аккаунт {said.name} удален', 200)
    except db.exc as error:
        abort(500, error)
