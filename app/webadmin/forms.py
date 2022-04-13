from app import db
from flask_wtf import FlaskForm
from wtforms_alchemy import (model_form_factory, ModelFormField, )
from app.models import *


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class AddressForm(ModelForm):
    class Meta:
        model = Address


class CafeForm(ModelForm):
    class Meta:
        model = Cafe
        exclude = ['created_at', 'updated_at']

    address = ModelFormField(AddressForm)


class InstagramPostForm(ModelForm):
    class Meta:
        model = InstagramEmbedded
        only = ['embedded_url']