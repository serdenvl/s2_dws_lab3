# -*- coding: utf-8 -*-
import os

from PIL import Image
from flask import render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename

from app import app
from app.forms import UploadForm, RetouchForm
from app.task1 import handle_image, color_histogram, Task1Function, Task1Orientation


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        data = form.upload.data
        name = secure_filename(data.filename)
        filepath = os.path.join(app.config['UPLOADS_FOLDER'], name)

        data.save(filepath)
        return redirect(url_for('retouch_image', original_name=name))
    return render_template('upload_image.html', title='Upload', form=form)


@app.route(
    rule='/retouch/<string:original_name>',
    methods=['GET', 'POST'],
)
def retouch_image(original_name: str):
    if not os.path.exists(os.path.join(app.config['UPLOADS_FOLDER'], original_name)):
        flash('no image to retouch')
        return redirect(url_for('upload_image'))

    with_sub_before_dot = lambda s, sub: s[:s.rfind('.')] + sub + s[s.rfind('.'):]

    retouched_name = with_sub_before_dot(original_name, '_retouched')
    histogram_name = with_sub_before_dot(original_name, '_histogram')

    src = lambda name: f"{app.config['UPLOADS_URL']}/{name}"
    path = lambda name: os.path.join(app.config['UPLOADS_FOLDER'], name)

    form = RetouchForm()
    if not form.validate_on_submit():
        return render_template('retouch_image.html',
                               title='Retouch',
                               form=form,
                               original_src=src(original_name))

    original = Image.open(path(original_name))

    function_name = form.function.data
    orientation = form.orientation.data
    period = form.period.data
    period_type = form.period_type.data

    retouched = handle_image(original, Task1Function[function_name], Task1Orientation[orientation], period, period_type == '%')
    retouched.save(path(retouched_name))

    histogram = color_histogram(path(histogram_name), original, retouched)
    histogram.save(path(histogram_name))

    return render_template('retouch_image.html',
                           title='Retouch',
                           form=form,
                           original_src=src(original_name),
                           retouched_src=src(retouched_name),
                           histogram_src=src(histogram_name),
                           width = original.width,
                           height= original.height)

@app.route(
    rule='/retouch/default',
    methods=['GET', 'POST'],
)
def default_image():
    return redirect(url_for('retouch_image', original_name=app.config['DEFAULT_IMAGE_NAME']))