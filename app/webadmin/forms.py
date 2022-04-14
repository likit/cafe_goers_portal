from wtforms.validators import DataRequired

from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, widgets
from wtforms_alchemy import (model_form_factory, ModelFormField, QuerySelectMultipleField)
from app.models import *

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class PlaceSearchForm(FlaskForm):
    name = StringField('Place name')


class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ['created_at', 'updated_at', 'wkb_geometry']


class CafeForm(ModelForm):
    class Meta:
        model = Cafe
        exclude = ['created_at', 'updated_at']

    address = ModelFormField(AddressForm)
    zones = QuerySelectMultipleField(u'Zone', get_label='zone',
                                     query_factory=lambda: Zone.query.all(),
                                     widget=widgets.ListWidget(prefix_label=False),
                                     option_widget=widgets.CheckboxInput())
    styles = QuerySelectMultipleField(u'Style', get_label='style',
                                      query_factory=lambda: Style.query.all(),
                                      widget=widgets.ListWidget(prefix_label=False),
                                      option_widget=widgets.CheckboxInput())
    activities = QuerySelectMultipleField(u'Activities', get_label='activity',
                                          query_factory=lambda: Activity.query.all(),
                                          widget=widgets.ListWidget(prefix_label=False),
                                          option_widget=widgets.CheckboxInput())


class InstagramPostForm(ModelForm):
    class Meta:
        model = InstagramEmbedded
        only = ['embedded_url', 'official_post']
