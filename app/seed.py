

from app import create_app, db
from models import Hero, Power, HeroPower

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created.")

    heroes_data = [
        {'name': 'Hulk', 'super_name': 'Bruce Banner'},
        {'name': 'Loki', 'super_name': 'Tom Hiddleston'},
        {'name': 'Hawkeye', 'super_name': 'Clint Barton'},
        {'name': 'Thor', 'super_name': 'Chris Hemsworth'},
        {'name': 'Batman', 'super_name': 'Bruce Wayne'},

    ]

    for hero_info in heroes_data:
        hero = Hero(**hero_info)
        db.session.add(hero)

    db.session.commit()
    print("Heroes data added successfully.")

    powers_data = [
        {'name': 'Flight', 'description': 'Ability to fly'},
        {'name': 'Strength', 'description': 'Superhuman strength'},
        {'name': 'Strength', 'description': 'Superhuman strength'},
        {'name': 'Strength', 'description': 'Superhuman strength'},
        {'name': 'Strength', 'description': 'Superhuman strength'},
        {'name': 'Strength', 'description': 'Superhuman strength'},
    ]

    for power_info in powers_data:
        power = Power(**power_info)
        db.session.add(power)

    db.session.commit()
    print("Powers data added successfully.")

    hero_powers_data = [
        {'hero_id': 1, 'power_id': 1, 'strength': 'Average'},
        {'hero_id': 2, 'power_id': 2, 'strength': 'Weak'},
        {'hero_id': 3, 'power_id': 2, 'strength': 'Average'},
        {'hero_id': 4, 'power_id': 1, 'strength': 'Strong'},
        {'hero_id': 5, 'power_id': 2, 'strength': 'Average'},
        {'hero_id': 6, 'power_id': 1, 'strength': 'Strong'},
    ]

    for hero_power_info in hero_powers_data:
        hero_power = HeroPower(**hero_power_info)
        db.session.add(hero_power)

    db.session.commit()
    print("Hero powers data added successfully.")

    print("Seed data added successfully.")