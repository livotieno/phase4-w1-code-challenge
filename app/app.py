#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate
from flask_cors import CORS
from flask import jsonify 



from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return "<h1>SUPER HEREOS</h1>"

@app.route('/heroes', methods=['GET','POST'])
def hereos():
    if request.method =='GET':
        heroes = Hero.query.all()
        hero_list = [hero.to_dict() for hero in heroes]
        response = make_response(jsonify(hero_list),200)
        return response

if __name__ == '__main__':
    app.run(port=5555)
