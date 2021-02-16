# -*- coding: utf-8 -*-

from datetime import date

from app import db

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