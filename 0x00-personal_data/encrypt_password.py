#!/usr/bin/env python3
'''
hash_password function that expects one string argument
name password and returns a salted, hashed password, which is a byte string.
'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''
    hash_password function that expects one string argument name
    password and returns a salted
    '''
    hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
    checks if hashed password and password match
    '''
    return bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password)
