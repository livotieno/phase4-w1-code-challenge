from faker import Faker
from app import app
from models import HeroPower, Hero, Power, db
import random

fake = Faker()

with app.app_context():

    Power.query.delete()
    Hero.query.delete()
    HeroPower.query.delete()

    print("🦸‍♀ Seeding powers...")
    powers = []
    for i in range(20):
        power = Power(
            name=fake.text(max_nb_chars=20),
            description=fake.sentence(nb_words=10)
        )
        powers.append(power)
    db.session.add_all(powers)
    db.session.commit()

    print("🦸‍♀ Seeding heroes...")
    heroes = []
    for i in range(20):
        hero = Hero(
            name=fake.first_name(),
            super_name=fake.unique.name(),
        )
        heroes.append(hero)
    db.session.add_all(heroes)
    db.session.commit()

    print("🦸‍♀ Adding powers to heroes...")
    strengths = ["Strong", "Weak", "Average"]
    hero_powers = []
    for i in range(20):
        hero_power = HeroPower(
            strength=random.choice(strengths),
            hero_id=random.choice(heroes).id,
            power_id=random.choice(powers).id
        )
        hero_powers.append(hero_power)

    db.session.add_all(hero_powers)
    db.session.commit()

    print("🦸‍♀ Done seeding!")