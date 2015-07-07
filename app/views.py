
from flask import render_template, flash, make_response, jsonify, request, abort
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from app import forms, models, app, db


@app.route('/', methods=['GET', 'POST'])
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = forms.RegistrationForm()

    if form.validate_on_submit():
        user = models.User(
            email=form.email.data,
            password=form.password.data,
            other=form.other.data
        )

        db.session.add(user)
        db.session.commit()
        flash("New user has been registered")

    return render_template('registration.html', form=form)



@app.route('/api/users', methods=['POST'])
def register_new_user():
    if not request.json:
        abort(400)
    form = forms.RegistrationForm()
    form.email = request.json.get('email')
    form.password = request.json.get('password')
    form.other = request.json.get('other')

    if form.validate():
        user = models.User(
            email=request.json['email'],
            password=request.json['password'],
            other=request.json.get('other')
        )
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'status': 'success'}), 201)
    else:
        return make_response(jsonify(form.errors), 400)






@app.route('/api/users', methods=['GET'])
def get_users():
    users = models.User.query
    sort = request.args.get('sort')

    if sort:
        desc_order = False
        if sort[0] == "-":
            sort = sort[1:]
            desc_order = True

        if sort == 'email':
            users = users.order_by(desc(models.User.email) if desc_order
                                   else models.User.email )
        elif sort == 'date':
            users = users.order_by(desc(models.User.timestamp) if desc_order
                                   else models.User.timestamp)
    else:
        users = users.all()

    response = []
    for user in users:
        response.append(user.serialize())

    return jsonify({'users': response})





@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = models.User.query.get(id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)

    return jsonify({'user': user.serialize()})


