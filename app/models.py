from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    _tablename_ = 'heroes'
    serialize_rules = ('-hero_powers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', back_populates='hero')


class Power(db.Model, SerializerMixin):
    _tablename_ = 'powers'
    serialize_rules = ('-hero_powers.power',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', back_populates='power')

    @validates('description')
    def validate_description(self, key, description):
        if not description:
            raise ValueError('Please provide description')
        if len(description) < 20:
            raise ValueError(
                'description should be at least 20 characters long')

        return description


class HeroPower(db.Model, SerializerMixin):
    _tablename_ = 'hero_powers'
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey(
        'powers.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero = db.relationship('Hero', back_populates="hero_powers", lazy=True)
    power = db.relationship('Power', back_populates="hero_powers", lazy=True)

    @validates('strength')
    def validate_strength(self, key, strength):
        strengths = ["Strong", "Weak", "Average"]
        if strength not in strengths:
            raise ValueError('Strength should be (Strong, Weak or Average)')
        return strength