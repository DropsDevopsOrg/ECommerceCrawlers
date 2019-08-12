# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

from exts import db

#诗人表
class Poet(db.Model):
    __tablename__ = 'poet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    dynasty = db.Column(db.String(10))
    introduction = db.Column(db.Text)
    num = db.Column(db.Integer)
    poems = db.relationship('Poem', backref='poet', lazy=True)

#诗词表
class Poem(db.Model):
    __tablename__ = 'poem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)
    analysis = db.Column(db.Text)
    author = db.Column(db.Integer, db.ForeignKey('poet.id'))




