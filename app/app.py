from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/')
    def home():
        return ''

    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        heroes_data = [{"id": hero.id, "name": hero.name,
                        "super_name": hero.super_name} for hero in heroes]
        return jsonify(heroes_data)

    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero(id):
        hero = Hero.query.get(id)

        if hero:
            hero_data = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": [{"id": hero_power.power.id, "name": hero_power.power.name, "description": hero_power.power.description} for hero_power in hero.hero_powers]
            }
            return jsonify(hero_data)
        else:
            return jsonify({"error": "Hero not found"}), 404

    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        powers_data = [{"id": power.id, "name": power.name,
                        "description": power.description} for power in powers]
        return jsonify(powers_data)

    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power(id):
        power = Power.query.get(id)

        if power:
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            return jsonify(power_data)
        else:
            return jsonify({"error": "Power not found"}), 404

    @app.route('/powers/<int:id>', methods=['PATCH'])
    def update_power(id):
        power = Power.query.get(id)

        if power:
            data = request.get_json()
            power.description = data.get('description', power.description)

            try:
                db.session.commit()
                return jsonify({"id": power.id, "name": power.name, "description": power.description})
            except:
                return jsonify({"errors": ["validation errors"]}), 400
        else:
            return jsonify({"error": "Power not found"}), 404

    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        data = request.get_json()

        hero = Hero.query.get(data.get('hero_id'))
        power = Power.query.get(data.get('power_id'))

        if hero and power:
            hero_power = HeroPower(strength=data.get(
                'strength'), hero=hero, power=power)

            try:
                db.session.add(hero_power)
                db.session.commit()
                return jsonify({"id": hero.id, "name": hero.name, "super_name": hero.super_name, "powers": [{"id": p.id, "name": p.name, "description": p.description} for p in hero.powers]})
            except:
                return jsonify({"errors": ["validation errors"]}), 400
        else:
            return jsonify({"errors": ["Invalid hero or power"]}), 400

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5555)