#!/usr/bin/env python3
'''
class BasicAuth that inherits from Auth
'''
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    '''
    BasicAuth, a variation of Auth
    '''

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        '''
        returns the Base64 part of the Authorization
        header for a Basic Authentication
        '''
        if authorization_header and isinstance(authorization_header, str):
            syntax_a = authorization_header.startswith("Basic ")
            if not syntax_a:
                return None
            auth_data = authorization_header.split(" ")[-1]
            return auth_data
            # decoded_data = base64.b64decode(auth_data)
            # return auth_data
        else:
            return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''
        returns the decoded value of a Base64
        string base64_authorization_header
        '''
        if base64_authorization_header and isinstance(
                base64_authorization_header, str):
            try:
                decoded_data = base64.b64decode(base64_authorization_header)
                return decoded_data.decode('utf-8')
            except Exception:
                return None
        else:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''
        returns the user email and password from the Base64 decoded value.
        '''
        if decoded_base64_authorization_header and isinstance(
                decoded_base64_authorization_header, str):
            if ":" not in decoded_base64_authorization_header:
                return (None, None)
            return tuple(decoded_base64_authorization_header.split(":"))
        else:
            return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''
        returns the User instance based on his email and password.
        '''
        if user_email and user_pwd and isinstance(
                user_email, str) and isinstance(user_pwd, str):
            response = User().search({'email': user_email})
            for obj in response:
                if obj.is_valid_password(user_pwd):
                    return obj
            return None
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        retrieves the User instance for a request
        '''
        auth = Auth()
        response_header = auth.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
            response_header)
        decoded_base64_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        user_credentials = self.extract_user_credentials(
            decoded_base64_auth_header)

        user = self.user_object_from_credentials(
            user_credentials[0], user_credentials[1])
        return user
