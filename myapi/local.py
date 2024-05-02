from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime

dp = SQLAlchemy()


class Users(dp.Model):
    id = dp.Column(dp.Integer, primary_key=True)
    name = dp.Column(dp.String(30), nullable=False)
    # surname = dp.Column(dp.String(30), nullable=False)
    # phone = dp.Column(dp.Integer, nullable=False)
    # year = dp.Column(dp.Integer, nullable=False)
    email = dp.Column(dp.String(120), unique=True, nullable=False)
    password = dp.Column(dp.String(128), nullable=False)
    hash = dp.Column(dp.Text, primary_key=True)

class Products(dp.Model):
    id = dp.Column(dp.Integer, primary_key=True)
    name = dp.Column(dp.String(30), nullable=False)
    description = dp.Column(dp.Text, nullable=False)
    quantity = dp.Column(dp.Integer, nullable=False)
    datatod = dp.Column(DateTime, default=datetime.utcnow)


    def __repr__(self):
        return self.name


def __repr__(self):
    return '<User %r>' % self.id

def __repr__(self):
    return '<Product %r>' % self.id