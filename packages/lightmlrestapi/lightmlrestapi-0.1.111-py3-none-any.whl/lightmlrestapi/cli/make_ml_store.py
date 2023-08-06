"""
@file
@brief Creates and runs an Falcon application.
"""
import os
import sys
import logging
import falcon
from pyquickhelper.cli.cli_helper import call_cli_function


def start_mlreststor(location='.', host='127.0.0.1', port=8081, name='ml', nostart=False,
                     wsgi='waitress', secret='', users='', algo='sha224',
                     fLOG=print):
    """
    Creates an :epkg:`falcon` application and
    runs it through a :epkg:`wsgi` server.
    The appplication stores machine learned models and runs predictions assuming
    all the necessary packages were installed.

    :param name: only one option is implemented 'ml'
    :param location: location of the storage
    :param host: host
    :param port: port
    :param nostart: do not start the wsgi server (for debug purpose)
    :param wsgi: :epkg:`wsgi` framework which runs the falcon application
    :param secret: secret used to encrypt the logging, default is empty which
        disables the encryption
    :param users: list of authorized users stored
        in a text file with two columns:
        login and encrypted password
    :param algo: algorithm used to encrypt the passwords
    :param fLOG: logging function

    Only :epkg:`waitress` is implemented right now.
    Other alternative such as :epkg:`mod_wsgi` with :epkg:`Apache`.
    :epkg:`uwsgi` are not implemented. Parameter *users* can be empty
    to disable authentification.
    """
    try:
        from ..mlapp.mlstorage_rest import MLStoragePost
        from ..mlapp.authfiction import AuthMiddleware
    except (ImportError, ValueError):
        folder = os.path.normpath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", ".."))
        sys.path.append(folder)
        from lightmlrestapi.mlapp.mlstorage_rest import MLStoragePost
        from lightmlrestapi.mlapp.authfiction import AuthMiddleware

    # Secrets.
    if not secret:
        secret = None
    if not users:
        users = None
    if name not in {'ml'}:
        raise ValueError("Name '{0}' is not recognized.".format(name))

    # Authenfication.
    if users:
        if fLOG:
            fLOG("[start_mlreststor] enable authentification")
        middleware = [AuthMiddleware(users, algo=algo)]
        app = falcon.API(middleware=middleware)
        url_scheme = 'https'
    else:
        app = falcon.API()
        url_scheme = 'http'

    # REST API
    location = os.path.abspath(location)
    if not os.path.exists(location):
        raise FileNotFoundError("Unable to find '{0}'".format(location))
    rest = MLStoragePost(secret=secret, folder=location,
                         folder_storage=location, version=None)

    app.add_route("/", rest)

    # Server.
    if wsgi == 'waitress':
        from waitress import serve
        if not nostart:
            fLOG("[start_mlreststor] serve(app, host='{}', port='{}', url_scheme='{}')".format(
                host, port, url_scheme))
            logger = logging.getLogger('waitress')
            logger.setLevel(logging.INFO)
            serve(app, host=host, port=port, url_scheme=url_scheme)
        else:
            fLOG("[start_mlreststor] do not run serve(app, host='{}', port='{}')".format(
                host, port))
    else:
        raise NotImplementedError(
            "Server '{}' is not implemented.".format(wsgi))

    return app


def _start_mlreststor(fLOG=print, args=None):
    """
    Creates an falcon application and starts it through a wsgi application.

    @param      fLOG        logging function
    @param      args        to overwrite ``sys.args``

    .. cmdref::
        :title: Creates an falcon application to store machine learned models
        :cmd: start_mlreststor=lightmlrestapi.cli.make_ml_store:_start_mlreststor
        :lid: cmd_start_mlreststor_cmd

        Creates an :epkg:`falcon` application and starts it through a :epkg:`wsgi` server.
        The appplication stores machine learned models and runs predictions assuming
        all the necessary packages were installed.
    """
    epkg_dictionary = dict(falcon='https://falconframework.org/',
                           Apache='https://httpd.apache.org/',
                           mod_wsgi='https://modwsgi.readthedocs.io/en/develop/',
                           uwsgi='https://uwsgi-docs.readthedocs.io/en/latest/',
                           wsgi='https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface',
                           waitress='https://docs.pylonsproject.org/projects/waitress/en/latest/')
    call_cli_function(start_mlreststor, args=args, fLOG=fLOG, skip_parameters=('fLOG',),
                      epkg_dictionary=epkg_dictionary)


if __name__ == "__main__":
    _start_mlreststor()
