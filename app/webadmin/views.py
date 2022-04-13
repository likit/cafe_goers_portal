from flask import render_template, request, url_for, redirect

from .forms import *
from . import webadmin


@webadmin.route('/')
def index():
    return render_template('webadmin/index.html')


@webadmin.route('/cafes/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
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