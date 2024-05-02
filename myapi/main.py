from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from local import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///localhost.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

dp.init_app(app)

with app.app_context():
    dp.create_all()


@app.route('/')
def index():
    return "hello"


@app.route('/data')
def data():
    users = Users.query.all()
    user_list = []

    for user in users:
        user_dict = {
            "name": user.name,
            "surname": user.surname,
            "phone": user.phone,
            "year": user.year
        }
        user_list.append(user_dict)
    if user_list == []:
        return jsonify({"message": "Нет пользователей"}), 200
    else:
        return jsonify(user_list)


@app.route('/create_user', methods=['POST'])
def create_user():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']
        year = request.form['year']

        user = Users(name=name, surname=surname, phone=phone, year=year)

        try:
            dp.session.add(user)
            dp.session.commit()
            return jsonify({"message": "Успешно добавлен"})
        except:
            return jsonify({"message": "Ошибка, пользователь не добавлен "}), 500

    else:
        return "user"


@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = Users.query.get(user_id)
    if user is not None:
        dp.session.delete(user)
        dp.session.commit()
        return jsonify({"message": "Успешно удален с базы"})


# ________________________________________________________________
@app.route('/pro')
def product_index():
    items = Products.query.all()
    return render_template('prod.html', data=items)


@app.route('/list_products')
def product_data():
    products = Products.query.all()
    product_list = []

    for product in products:
        product_dict = {
            "name": product.name,
            "description": product.description,
            "quantity": product.quantity,
            "datatod": product.datatod
        }
        product_list.append(product_dict)

    if product_list == []:
        return jsonify({"message": "Нет product"}), 200
    else:
        return product_list


@app.route('/create_product', methods=['POST'])
def create_product():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        quantity = request.form['quantity']
        datatod = datetime.utcnow()

        product = Products(name=name, description=description, quantity=quantity, datatod=datatod)

        try:
            dp.session.add(product)
            dp.session.commit()
            return jsonify({"message": "Успешно добавлен"})
        except:
            return jsonify({"message": "Ошибка, product не добавлен "}), 500

    else:
        return "product"


@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Products.query.get(product_id)
    if product is not None:
        dp.session.delete(product)
        dp.session.commit()
        return jsonify({"message": "Успешно удален"})


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if len(name) > 4 and len(email) > 4 and len(password) > 4 and password == confirm_password:
            hash = generate_password_hash(password)
            res = dp.base.Users(name, email, hash)
            if res:
                jsonify({"message": "Successfully registered"})
                return redirect(url_for('/'))
            else:
                jsonify({"message": "Registration failed"})

    return render_template('register.html')


@app.route('/login_user', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Login failed. Please check your email and password.', 'error')

    return render_template('login.html')


@app.route('/profile')
def profile():
    return 'Welcome to your profile'


if __name__ == '__main__':
    app.run()
