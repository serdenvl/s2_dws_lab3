import os.path


class Config(object):
    SECRET_KEY = 'secret'

    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = '6Lds8HQgAAAAAD9jAxy3YnIaKMK7BNy1ZNGayjm9'
    RECAPTCHA_PRIVATE_KEY = '6Lds8HQgAAAAAIiQH-dnlOIlaEMhaZnx_2JadK7L'
    RECAPTCHA_OPTIONS = {'theme': 'white'}

    UPLOADS_FOLDER = os.path.join('static', 'uploads')
    UPLOADS_URL = '/static/uploads'

    DEFAULT_IMAGE_NAME = 'rainbow.jpg'
