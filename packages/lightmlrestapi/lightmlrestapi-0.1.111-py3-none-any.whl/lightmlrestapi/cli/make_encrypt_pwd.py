"""
@file
@brief Creates and runs an Falcon application.
"""
import os
import sys
import pandas
from pyquickhelper.cli.cli_helper import call_cli_function


def encrypt_pwd(input="", output="", algo="sha224", fLOG=print):  # pylint: disable=W0622
    """
    Encrypts passwords to setup a REST API
    with *lightmlrestapi*.

    :param input: file containing two columns <login>,<clear password>
        (comma separated values), no header, encoding is *utf-8*
    :param output: file containing two columns <login>,<encrypted password>,
        csv, encoding is *utf-8*
    :param algo: algorithm used to hash the passwords
    :param fLOG: logging function
    """
    try:
        from ..args.encrypt_helper import encrypt_passwords
    except (ImportError, ValueError):
        folder = os.path.normpath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", ".."))
        sys.path.append(folder)
        from lightmlrestapi.args.encrypt_helper import encrypt_passwords

    if not os.path.exists(input):
        raise FileNotFoundError("File '{0}' not found".format(input))

    if fLOG:
        fLOG("[encrypt_pwd] encrypt '{0}'".format(input))
    df = pandas.read_csv(input, sep=',', encoding='utf-8', header=None)
    df2 = encrypt_passwords(df, algo=algo)
    if fLOG:
        fLOG("[encrypt_pwd] to      '{0}'".format(output))
    df2.to_csv(output, sep=',', encoding='utf-8', header=False, index=False)
    if fLOG:
        fLOG("[encrypt_pwd] done.")


def _encrypt_pwd(fLOG=print, args=None):
    """
    Encrypts passwords to setup a REST API
    with *lightmlrestapi*.

    @param      fLOG        logging function
    @param      args        to overwrite ``sys.args``

    .. cmdref::
        :title: Encrypts password
        :cmd: encrypt_pwd=lightmlrestapi.cli.make_encrypt_pwd:_encrypt_pwd
        :lid: cmd_encrypt_pwd_cmd

        Encrypts passwords for a REST API created by *lightmlrestapi*.
    """
    epkg_dictionary = dict(falcon='https://falconframework.org/',
                           Apache='https://httpd.apache.org/',
                           mod_wsgi='https://modwsgi.readthedocs.io/en/develop/',
                           uwsgi='https://uwsgi-docs.readthedocs.io/en/latest/',
                           wsgi='https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface',
                           waitress='https://docs.pylonsproject.org/projects/waitress/en/latest/')
    call_cli_function(encrypt_pwd, args=args, fLOG=fLOG, skip_parameters=('fLOG',),
                      epkg_dictionary=epkg_dictionary)


if __name__ == "__main__":
    _encrypt_pwd()
