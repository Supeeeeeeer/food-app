from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'iloveamogus'
db = SQLAlchemy(app)
rests = ['KFC', "McDonald's"]
foodes = {
    'Burger': 15,
    'French Fries': 11
}
session = {}
status = {
    'logged_in': False
}
us = []


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.Text, nullable=False)

class Rest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.Text, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    age = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def main():  # put application's code here
    if request.method == 'POST':
        db.session.query(Rest).delete()
        restaurant = request.form['rest']
        if restaurant in rests:
            res = Rest(restaurant=restaurant)
            db.session.add(res)
            db.session.commit()
            return redirect('/food')
        else:
            return redirect('/')
    return render_template('main.html')


@app.route('/food', methods=['POST', 'GET'])
def food():
    if request.method == 'POST':
        db.session.query(Food).delete()
        food = request.form['food']
        if food in foodes.keys():
            new_food = Food(food=food)
            db.session.add(new_food)
            db.session.commit()
            return redirect('/offered_food')
        else:
            return redirect('/food')
    return render_template('restaurans.html')


@app.route('/offered_food')
def offered():
    sel_res = Rest.query.all()
    sel_food = Food.query.all()
    return render_template('offered_food.html', sel_res=sel_res, sel_food=sel_food)

@app.route('/reg_page')
def reg_page():
    return render_template('reg.html')

@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']

        users = User(name=name, age=age, email=email)
        db.session.add(users)
        db.session.commit()
        return redirect(url_for('user'))


@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']

        user = User.query.filter_by(name=name, age=age, email=email).first()
        if user:
            return redirect(url_for('main'))
        else:
            return redirect(url_for('user'))
    return render_template('user.html')
    

@app.route('/admin_code')
def admin_code():
    return render_template('admin_code.html')


@app.route('/enter_code', methods=['GET', 'POST'])
def enter():
    if request.method == 'POST':
        code = request.form['code']
        if code.lower() == 'foodwareinsiders(admin)':
            return redirect('/admin')
    return redirect('/admin_code')
    
            

@app.route('/clear')
def clear():
    try:
        db.session.query(User).delete()
        db.session.commit()
        return redirect('/admin')
    except Exception as e:
        return(f'Cannot clear account database. Error: {str(e)}')

@app.route('/clear_offer')
def clear_offer():
    try:
        db.session.query(Food).delete()
        db.session.query(Rest).delete()
        db.session.commit()
        return redirect('/offered_food')
    except Exception as ex:
        return(f"Cannot clear offer database. Error: {str(ex)}")

@app.route('/admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)



if __name__ == '__main__':
    app.run()
