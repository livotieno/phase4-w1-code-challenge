from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model,SerializerMixin):
    __tablename__ = 'heroes'
    serialize_rules = ('-hero_powers.hero')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    super_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define the relationship with Power through HeroPower
    powers = db.relationship('HeroPower', back_populates='hero')
    hero_power = db.relationship('HeroPower', backref='hero')

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define the relationship with Hero through HeroPower
    heroes = db.relationship('HeroPower',  back_populates='power')
    
    @validates('description')
    def validate_description(self, key, description):
        if not description:
            raise ValueError('Please provide description')
        if len(description) < 20:
            raise ValueError(
                'description should be atleast 20 characters long')

        return description

class HeroPower(db.Model,SerializerMixin):
    __tablename__ = 'heropowers'  
    serialize_rules=('-hero.hero_powers', '-power.hero_powers')
    id = db.Column(db.Integer, primary_key=True)  
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define the relationships with Hero and Power
    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')
    
    @validates('strength')
    def validate_strength(self, key, strength):
        strengths = ["Strong", "Weak", "Average"]
        if strength not in strengths:
            raise ValueError('Strength should be (Strong, Weak or Average)')
        return strength