from datetime import datetime
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class HeroPower(db.Model):
    __tablename__ = 'hero_power'
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.String(50), nullable=False)
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='power_heroes')

    @validates('strength')
    def validate_strength(self, key, value):
        assert value in [
            'Strong', 'Weak', 'Average'], "Strength must be one of: 'Strong', 'Weak', 'Average'"
        return value


class Hero(db.Model):
    __tablename__ = 'hero'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)
    hero_powers = db.relationship(
        'HeroPower', back_populates='hero', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
            "powers": [{"id": power.id, "name": power.name, "description": power.description}
                       for power in self.powers]
        }


class Power(db.Model):
    __tablename__ = 'power'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    power_heroes = db.relationship(
        'HeroPower', back_populates='power', lazy=True)

    @validates('description')
    def validate_description(self, key, value):
        assert value and len(
            value) >= 10, "Description must be present and at least 20 characters long"
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }