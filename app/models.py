from geoalchemy2 import Geometry
from shapely.geometry import Point
from geoalchemy2.shape import from_shape

from app import db
from sqlalchemy.sql import func

place_styles = db.Table('place_styles',
    db.Column('cafe_id', db.Integer, db.ForeignKey('cafes.id'), primary_key=True),
    db.Column('style_id', db.Integer, db.ForeignKey('styles.id'), primary_key=True)
)

place_zones = db.Table('place_zones',
                        db.Column('cafe_id', db.Integer, db.ForeignKey('cafes.id'), primary_key=True),
                        db.Column('zone_id', db.Integer, db.ForeignKey('zones.id'), primary_key=True)
                        )

place_activities = db.Table('place_activities',
                       db.Column('cafe_id', db.Integer, db.ForeignKey('cafes.id'), primary_key=True),
                       db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True)
                       )


class Style(db.Model):
    __tablename__ = 'styles'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    style = db.Column('style', db.String)


class Zone(db.Model):
    __tablename__ = 'zones'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    zone = db.Column('zone', db.String)


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    activity = db.Column('activity', db.String)


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    street = db.Column('street', db.String, info={'label': 'Street'})
    province = db.Column('province', db.String, info={'label': 'District'})
    district = db.Column('district', db.String, info={'label': 'Province'})
    subdistrict = db.Column('subdistrict', db.String, info={'label': 'Sub-district'})
    postal_code = db.Column('postal_code', db.String, info={'label': 'Postal Code'})
    created_at = db.Column('created_at', db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column('updated_at', db.DateTime(timezone=True),
                           onupdate=func.now())
    lat = db.Column('lat', db.Float, info={'label': 'Latitude'})
    lon = db.Column('lon', db.Float, info={'label': 'Longitude'})
    wkb_geometry = db.Column(Geometry('POINT', srid=4326))

    def add_geometry(self):
        self.wkb_geometry = from_shape(Point(self.lon, self.lat), srid=4326)

    def __str__(self):
        return ' '.join([self.street, self.district, self.province])

    @property
    def location(self):
        return f'{self.lat:.4f}, {self.lon:.4f}'


class Cafe(db.Model):
    __tablename__ = 'cafes'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String, nullable=False, info={'label': 'Name'})
    address_id = db.Column('address_id', db.ForeignKey('addresses.id'))
    created_at = db.Column('created_at', db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column('updated_at', db.DateTime(timezone=True),
                           onupdate=func.now())
    address = db.relation(Address, backref=db.backref('cafe', uselist=False,
                                                      cascade='all, delete-orphan'))
    zones = db.relation(Zone, secondary=place_zones, lazy='subquery', backref=db.backref('cafes', lazy=True))
    styles = db.relation(Style, secondary=place_styles, lazy='subquery', backref=db.backref('cafes', lazy=True))
    activities = db.relation(Activity, secondary=place_activities, lazy='subquery', backref=db.backref('cafes', lazy=True))
    price_level = db.Column('price_level', db.Integer,
                            info={'label': 'Price Level',
                                  'choices': [(i, c) for i, c in enumerate(['$-$$', '$$-$$$', '$$$-$$$$'])],
                                  }
                            )
    service_charge_rate = db.Column('service_charge_rate', db.Float(), default=0.0,
                                    info={'label': 'Service Charge Rate'})
    vat_included = db.Column('vat_included', db.Boolean, default=True, info={'label': 'Vat included', 'description': 'ราคารวมภาษีมูลค่าเพิ่มแล้ว'})
    parking_avail = db.Column('parking_avail', db.String, info={'label': 'Parking Availability',
                                                                'choices': [(c, c) for c in ['<10', '10-20', '>20']]})
    parking_note = db.Column('parking_note', db.Text(), info={'label': 'Parking Note'})
    parking_fee = db.Column('parking_fee', db.Boolean, info={'label': 'Parking Fee'})
    free_wifi = db.Column('free_wifi', db.Boolean, info={'label': 'Free WiFi'})
    seating_avail = db.Column('seating_avail', db.String, info={'label': 'Seating Availability',
                                                                'choices': [(c, c) for c in ['<10', '10-20', '>20']]})
    pet_friendly = db.Column('pet_friendly', db.Boolean, info={'label': 'Pet Friendly'})


class InstagramEmbedded(db.Model):
    __tablename__ = 'instagram_embeddeds'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    embedded_url = db.Column('embedded_url', db.Text, nullable=False)
    cafe_id = db.Column('cafe_id', db.ForeignKey('cafes.id'))
    cafe = db.relation(Cafe, backref=db.backref('ig_posts',
                                                lazy='dynamic',
                                                cascade='all, delete-orphan'))
    created_at = db.Column('created_at', db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column('updated_at', db.DateTime(timezone=True),
                           onupdate=func.now())

    def __str__(self):
        return self.embedded_url
