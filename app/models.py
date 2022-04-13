from app import db
from sqlalchemy.sql import func


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    street = db.Column('street', db.String)
    province = db.Column('province', db.String)
    district = db.Column('district', db.String)


class Cafe(db.Model):
    __tablename__ = 'cafes'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String, nullable=False)
    address_id = db.Column('address_id', db.ForeignKey('addresses.id'))
    created_at = db.Column('created_at', db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column('updated_at', db.DateTime(timezone=True),
                           onupdate=func.now())
    address = db.relation(Address, backref=db.backref('cafe', uselist=False,
                                                      lazy='dynamic',
                                                      cascade='all, delete-orphan'))


class InstagramEmbedded(db.Model):
    __tablename__ = 'instagram_embeddeds'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    embedded_url = db.Column('embedded_url', db.Text, nullable=False)
    cafe_id = db.Column('cafe_id', db.ForeignKey('cafes.id'))
    cafe = db.relation(Cafe, backref=db.backref('instagrams',
                                                lazy='dynamic',
                                                cascade='all, delete-orphan'))
    created_at = db.Column('created_at', db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column('updated_at', db.DateTime(timezone=True),
                           onupdate=func.now())
