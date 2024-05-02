from flask_sqlalchemy import SQLAlchemy

dp = SQLAlchemy()


class Users(dp.Model):
    id = dp.Column(dp.Integer, primary_key=True)
    name = dp.Column(dp.String(30), nullable=False)
    surname = dp.Column(dp.String(30), nullable=False)
    phone = dp.Column(dp.Integer, nullable=False)


def __repr__(self):
    return '<User %r>' % self.id

# если какая нибудь ошибка то он просто отправляет id юсера и по нему ищет


# nullable = возможность оставить пустым
# primary_key = автоматически подставляет
