# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import fields, validators
from wtforms_alchemy import ModelForm

from models import Article, Comment

# Every ModelForm must define model parameter in the Meta arguments
#https://wtforms-alchemy.readthedocs.io/en/latest/introduction.html

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        

class CommentForm(ModelForm):
    class Meta:
        model = Comment     # Мы используем модель Comment для того, чтобы создать из нее форму
        include = [         # Дополнительно включаем поле article_id
            'article_id',   # По причине того, что ПО УМОЛЧАНИЮ это поле не включется!
            ]               # By the way... Это поле внешнего ключа!