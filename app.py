from flask import Flask, request, jsonify
from models import *

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    db.create_all()


# ----------------------------------------------------------------------------------------->

# main page
@app.route('/')
def index():
    return "hello"


# get all data
@app.route('/data')
def data():
    users = Users.query.all()
    user_list = []

    for user in users:
        user_dict = {
            "name": user.name,
            "surname": user.surname,
            "phone": user.phone
        }
        user_list.append(user_dict)

    return jsonify(user_list)


# add user
@app.route('/create_user', methods=['POST'])
def create_user():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']

        user = Users(name=name, surname=surname, phone=phone)

        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "Пользователь успешно добавлен"})
        except:
            return jsonify({"message": "Ошибка"})
    else:
        return "user"


# delete user
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)  # Найдите пользователя по его идентификатору

    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Пользователь успешно удален"}), 200  # 200 OK



if __name__ == '__main__':
    app.run()

