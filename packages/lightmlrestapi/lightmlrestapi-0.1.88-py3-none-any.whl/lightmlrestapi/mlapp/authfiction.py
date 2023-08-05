"""
@file
@brief Authentification part.
"""
import io
import os
import pandas
import jwt
import falcon


class AuthMiddleware:
    """
    Authentification. The name and secret comes from
    a file. The file must store encrypted password.
    """

    def __init__(self, source, secret):
        """
        @param      source      filename or dataframe
        @param      secret      used to encrypt password and check equality
        """
        if secret is None:
            raise ValueError("secret cannot be None")
        if isinstance(source, str):
            if ',' in source:
                df = pandas.read_csv(io.StringIO(source))
            elif os.path.exists(source):
                df = pandas.read_csv(source)
            else:
                raise FileNotFoundError("Unable to find '{0}'.".format(source))
        else:
            df = source
        if not isinstance(df, dict):
            for col in ['login', 'pwd']:
                if col not in df.columns:
                    raise ValueError(
                        "source must have a column '{0}'".format(col))
            memo = df
            df = {}
            for i in range(memo.shape[0]):
                login = memo.loc[i, 'login']
                pwd = memo.loc[i, 'pwd']
                if login in df:
                    raise KeyError("Duplicated login '{0}'.".format(login))
                df[login] = pwd
        self.allowed = df
        self.secret = secret

    def process_request(self, req, resp):
        """
        Processes an authentification request.

        @param  req     request
        @param  resp    unused
        """
        if req.protocol.lower() != 'https':
            raise falcon.HTTPBadRequest(title='HTTPS Required',
                                        description=('All requests must be performed via the HTTPS protocol. '
                                                     'Please switch to HTTPS and try again.'))

        token = req.get_header('token')
        account_id = req.get_header('uid')

        challenges = ['Token type="Fernet"']

        if token is None:
            description = (
                'Please provide an auth token as part of the request.')
            raise falcon.HTTPUnauthorized('Authentification token required',
                                          description, challenges,
                                          href='http://docs.example.com/auth')

        if not self._token_is_valid(token, account_id):
            description = (
                'The provided auth token is not valid. Please request a new token and try again.')
            raise falcon.HTTPUnauthorized('Authentication required',
                                          description, challenges,
                                          href='http://docs.example.com/auth')

    def _token_is_valid(self, token, account_id):
        """
        Decides if it is valid or not.
        """
        if account_id not in self.allowed:
            return False
        enc_pwd = jwt.encode({'token': token}, self.secret, algorithm='HS256')
        return self.allowed[account_id] != enc_pwd
