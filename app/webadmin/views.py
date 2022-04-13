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
            db.session.add(cafe)
            db.session.commit()
            return redirect(url_for('webadmin.index'))
        else:
            print(form.errors)
    return render_template('webadmin/cafe_edit.html', form=form)


@webadmin.route('/cafes')
def list_cafes():
    cafes = Cafe.query.all()
    return render_template('webadmin/cafes.html', cafes=cafes)