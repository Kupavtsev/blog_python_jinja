# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from datetime import date

# from models import *
# from forms import *

import config as config

from flask_wtf import FlaskForm
from wtforms import fields, validators
from wtforms_alchemy import ModelForm

__author__ = 'OlegKupavtsev'
# Теория 41, 51 стр. конспекта.

app = Flask(__name__, template_folder='template')
app.config.from_object(config)

db = SQLAlchemy(app)


# Models
class Article(db.Model):    # Данный Класс наследуется от метода Model БД. Модель в Python это Таблица в БД
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(140), unique = True, nullable = False)
    article_url = db.Column(db.String(300), unique = True, nullable = False)
    content = db.Column(db.String(2000), nullable = False)
    date_created = db.Column(db.Date, default = date.today)
    
    def __str__(self):  # Сам объект этого класса становится строкой ?
        return '<Article: {}>'.format(self.title)

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    article_id = db.Column(                      # 56 стр. конспекта
                 db.Integer,                     # Integer потому что id(9стр) - Integer
                 db.ForeignKey('article.id'),    # Внешний ключ к таблице Article .Связь с колонкой в 9ой строке.
                 nullable = False,
                 index = True)
    article = db.relationship(Article, foreign_keys=[article_id, ]) # Отношение с Классом Article. Сама переменная
                                                                    # является объктом класса Article
    #27 При помощи внешенего ключа foreign_keys=[article_id, ] он понимает с каким классом Article устанавливается отношение
    #27 Отношение будет является объектом класса Article, таким, что его id лежит в 22
    #22 Мы возьмем article_id сделаем JOIN(соединение двух таблиц). И при помощи JOIN у нас будут данные из Article&Comment
    
    content = db.Column(db.String(3000), nullable = False)
    date_created = db.Column(db.Date, default = date.today)

    def __str__(self):
        return '<Comment {} to Article{}>'.format(self.title, self.article.title)


# FORMS
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        

class CommentForm(ModelForm):
    class Meta:
        model = Comment     
        include = [         
            'article_id',   
            ]               




@app.route('/', methods=['GET', 'POST'])
def index():

    '''
    Основная страница блога, на которой выводится форма для ввода статьи и ниже все введенные статьи
    с возможностью перейти на страницу любой из них
    '''

    if request.method == 'POST':            # Если метод запроса POST
        form = ArticleForm(request.form)    # То мы используем следующую форму запроса

        if form.validate():                 # Если форма проходит Валидацию
            article = Article(**form.data)  # Мы делаем предварительный commit, пока без id
            db.session.add(article)
            db.session.commit()

            article.article_url = str(article.id)
            db.session.commit()
            return redirect(url_for('index'))   # Для построения URL для специфической функции, вы можете использовать функцию url_for()
        else:                                   # В качестве первого аргумента она принимает имя функции
            return render_template('errors.html', errors_text=str(form.errors))
    
    all_articles = Article.query.all()

    return render_template('index.html', articles=all_articles, date_today=date.today())

@app.route('/article/<article_url>', methods=['GET', 'POST'])
def new_article(article_url):
    
    #Страница для вывода конкретной статьи по сгенерированному url
    #На этой странице можно добаваить коммент к статье или выйти на главную с помощью кнопок
   
    form = CommentForm(request.form)
    article = Article.query.filter_by(article_url = article_url).first()
    if request.method == 'POST':
        print(request.form)

        if form.validate():
            comment = Comment(**form.data)
            db.session.add(comment)
            db.session.commit()
        else:
            return render_template('errors.html', errors_text = str(form.errors))

    all_comments = Comment.query.filter_by(article=article)

    return render_template('article.html', comments=all_comments, article=article, date_today=date.today())


if __name__ == '__main__':


    db.create_all()

    app.run()