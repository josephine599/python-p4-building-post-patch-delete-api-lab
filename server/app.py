#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


# -----------------------
# Helpers
# -----------------------
def bakery_dict(bakery):
    data = bakery.to_dict()
    data['created_at'] = "exists"
    return data


def baked_good_dict(bg):
    data = bg.to_dict()
    data['created_at'] = "exists"
    return data


# ======================
# POST /baked_goods
# ======================
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    bg = BakedGood(
        name=request.form.get('name'),
        price=request.form.get('price'),
        bakery_id=request.form.get('bakery_id')
    )
    db.session.add(bg)
    db.session.commit()

    return jsonify(baked_good_dict(bg)), 201


# ======================
# PATCH /bakeries/<id>
# ======================
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)

    if 'name' in request.form:
        bakery.name = request.form['name']

    db.session.add(bakery)
    db.session.commit()

    return jsonify(bakery_dict(bakery)), 200


# ======================
# DELETE /baked_goods/<id>
# ======================
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    bg = BakedGood.query.get(id)
    db.session.delete(bg)
    db.session.commit()

    return jsonify({}), 200
