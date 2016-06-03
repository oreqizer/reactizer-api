from flask_babel import gettext


def error_handler(app):

    @app.errorhandler(500)
    def internal_server_error():
        gettext('Oops, something is wrong with the server.')
