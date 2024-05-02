from flask import Flask, request, jsonify
from local import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaseprodcrm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dp.init_app(app)

with app.app_context():
    dp.create_all()


@app.route('/')
def index():
    return "Hello"


@app.route('/data')
def data():
    users = Users.query.all()
    user_list = []

    for user in users:
        user_dict = {
            "name": user.name,
            "surname": user.surname,
            "phone": user.phone,
        }
        user_list.append(user_dict)
    if user_list == []:
        return jsonify({"message": "Ошибка"}), 200
    else:
        return jsonify(user_list)


@app.route('/new_user', methods=['POST'])
def new_user():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']

        user = Users(name=name, surname=surname, phone=phone)

        try:
            dp.session.add(user)
            dp.session.commit()
            return jsonify({"message": "Пользователь успешно добавлен"})
        except:
            return jsonify({"message": "Ошибка"})

    else:
        return "user"


@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = Users.query.get(user_id)
    if user is not None:
        dp.session.delete(user)
        dp.session.commit()
        return jsonify({"message": "Пользователь успешно удален"})


if __name__ == "__main__":
    app.run()
