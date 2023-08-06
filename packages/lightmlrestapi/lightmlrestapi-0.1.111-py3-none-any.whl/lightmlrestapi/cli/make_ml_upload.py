"""
@file
@brief Creates and runs an Falcon application.
"""
import os
import sys
from pyquickhelper.cli.cli_helper import call_cli_function


def upload_model(login="", pwd="", name="", pyfile="", data="", url='127.0.0.1:8081',   # pylint: disable=W0102
                 timeout=15, fLOG=print):  # pylint: disable=W0622
    """
    Uplaods a machine learned models to a REST API defined by
    @see cl MLStoragePost.

    :param login: user login
    :param pwd: user pasword
    :param name: name of the model, should be unique and not already used
    :param pyfile: python file which computes the prediction,
        the file must follows the specification defined in
        :ref:`l-template-ml`
    :param data: files to upload
    :param url: url of the REST API
    :param timeout: timeout
    :param fLOG: logging function
    """
    try:
        from ..netrest import submit_rest_request, json_upload_model
    except (ImportError, ValueError):
        folder = os.path.normpath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", ".."))
        sys.path.append(folder)
        from lightmlrestapi.netrest import submit_rest_request, json_upload_model

    if isinstance(data, str):
        data = data.split(',')
    if fLOG:
        fLOG('[upload_model] Prepare the JSON request.')
    req = json_upload_model(name=name, pyfile=pyfile, data=data)
    if fLOG:
        fLOG('[upload_model] Submit request - size:', len(req['zip']))
    submit_rest_request(req, login=login, pwd=pwd, url=url, fLOG=fLOG)
    if fLOG:
        fLOG('[upload_model] Done.')


def _upload_model(fLOG=print, args=None):
    """
    Encrypts passwords to setup a REST API
    with *lightmlrestapi*.

    @param      fLOG        logging function
    @param      args        to overwrite ``sys.args``

    .. cmdref::
        :title: Uploads a machine model
        :cmd: upload_model=lightmlrestapi.cli.make_ml_upload:_upload_model
        :lid: cmd_upload_model_cmd

        Uploads a machine learned model to a REST API
        created with *lightmlrestapi*. The code of this command line is equivalent
        to:

        ::

            from lightmlrestapi.netrest import submit_rest_request, json_upload_model
            req = json_upload_model(name=name, pyfile=pyfile, data=data)
            submit_rest_request(req, login=login, pwd=pwd, url=url)
    """
    epkg_dictionary = dict(falcon='https://falconframework.org/',
                           Apache='https://httpd.apache.org/',
                           mod_wsgi='https://modwsgi.readthedocs.io/en/develop/',
                           uwsgi='https://uwsgi-docs.readthedocs.io/en/latest/',
                           wsgi='https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface',
                           waitress='https://docs.pylonsproject.org/projects/waitress/en/latest/')
    call_cli_function(upload_model, args=args, fLOG=fLOG, skip_parameters=('fLOG',),
                      epkg_dictionary=epkg_dictionary)


if __name__ == "__main__":
    _upload_model()
