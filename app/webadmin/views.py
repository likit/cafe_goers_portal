import os

import googlemaps
from flask import render_template, request, url_for, redirect, flash

from .forms import *
from . import webadmin


gmaps = googlemaps.Client(os.environ.get('GOOGLE_MAP_API_KEY'))


@webadmin.route('/')
def index():
    return render_template('webadmin/index.html')


@webadmin.route('/places/find', methods=['GET', 'POST'])
def find_place():
    form = PlaceSearchForm()
    places = []
    if request.method == 'POST':
        name = form.name.data
        result = gmaps.find_place(name, input_type='textquery')
        for cand in result['candidates']:
            place = gmaps.place(cand['place_id'], language='TH')
            places.append(
                {
                    'place_id': cand['place_id'],
                    'name': place['result']['name'],
                    'formatted_address': place['result']['formatted_address'],
                    'url': place['result']['url']
                }
            )
    return render_template('webadmin/place_search_form.html', form=form, places=places)


@webadmin.route('/cafes/add', methods=['GET', 'POST'])
def add_cafe():
    place_id = request.args.get('place_id')
    form = CafeForm()
    if place_id:
        place = gmaps.place(place_id, language='TH')
        form.name.data = place['result'].get('name')
        try:
            form.address.lat.data, form.address.lon.data = place['result']['geometry']['location'].values()
        except KeyError:
            pass
        for addr_component in place['result'].get('address_components', []):
            if 'route' in addr_component['types']:
                form.address.street.data = addr_component['long_name']
            elif 'sublocality_level_1' in addr_component['types']:
                form.address.district.data = addr_component['long_name']
            elif 'sublocality_level_2' in addr_component['types']:
                form.address.subdistrict.data = addr_component['long_name']
            elif 'administrative_area_level_1' in addr_component['types']:
                form.address.province.data = addr_component['long_name']
            elif 'postal_code' in addr_component['types']:
                form.address.postal_code.data = addr_component['long_name']

    if request.method == 'POST':
        if form.validate_on_submit():
            cafe = Cafe()
            form.populate_obj(cafe)
            if cafe.address.lat and cafe.address.lon:
                cafe.address.add_geometry()
            db.session.add(cafe)
            db.session.commit()
            return redirect(url_for('webadmin.index'))
        else:
            print(form.errors)
    return render_template('webadmin/cafe_add.html', form=form)


@webadmin.route('/cafes/<int:cafe_id>/edit', methods=['GET', 'POST'])
def edit_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    form = CafeForm(obj=cafe)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(cafe)
            db.session.add(cafe)
            db.session.commit()
            flash('Updated data successfully.', 'success')
        return redirect(url_for('webadmin.list_cafes'))
    return render_template('webadmin/cafe_add.html', form=form)


@webadmin.route('/cafes')
def list_cafes():
    cafes = Cafe.query.all()
    return render_template('webadmin/cafes.html', cafes=cafes)


@webadmin.route('/cafes/<int:cafe_id>/ig-post/add', methods=['GET', 'POST'])
def add_ig_post(cafe_id):
    form = InstagramPostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = InstagramEmbedded()
            form.populate_obj(post)
            post.cafe_id = cafe_id
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('webadmin.list_cafes'))
    return render_template('webadmin/ig_url_add.html', form=form)