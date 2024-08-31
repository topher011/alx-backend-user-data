#!/usr/bin/env python3
'''
class to manage the API authentication.
'''
from flask import request
from typing import List, TypeVar
import os


class Auth:
    '''
    Manages authentication for api
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        auth mthd
        '''
        if path is None:
            return True
        if not path.endswith("/"):
            path += "/"
        if excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        '''
        To be implemented
        '''
        if not request:
            return None
        if "Authorization" not in request.headers:
            return None
        else:
            return request.headers.get("Authorization")
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        To be implemented
        '''
        return None

    def session_cookie(self, request=None):
        '''
        returns a cookie value from a request
        '''
        if request is None:
            return None
        cookie_name = os.getenv("SESSION_NAME")
        return request.cookies.get(cookie_name, None)
