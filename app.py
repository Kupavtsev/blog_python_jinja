# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from datetime import date

import config as config

__author__ = 'OlegKupavtsev'
# Теория 41, 51 стр. конспекта.

app = Flask(__name__, template_folder='template')
app.config.from_object(config)

db = SQLAlchemy(app)

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

    from models import *
    from forms import *

    db.create_all()

    app.run()