from flask_babel import gettext


def error_handler(app):

    @app.errorhandler(AttributeError)
    def attribute_error(error):
        return gettext('Server attribute error'), 500

    @app.errorhandler(Exception)
    def attribute_error(error):
        return gettext('Oops, something is wrong with the server.'), 500
