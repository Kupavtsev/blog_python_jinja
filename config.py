# -*- coding: utf-8 -*-

__author__ = 'OlegKupavtsev'

DEBUG = True    # Перезапускает сервер при изменении кода
SECRET_KEY = 'KOVSecretKey'

SQLALCHEMY_DATABASE_URI = 'sqlite:///myblog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False #Отслежиывет изменения и посылает синалы

WTF_CSRF_ENABLED = False    # Снимает защиту для упрощения. CSFR запрещает посторонним делать POST запрос.