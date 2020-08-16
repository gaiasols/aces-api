from datetime import datetime
from fastapi import HTTPException


def raise_not_found(message: str = "Not found"):
    '''Raise 404'''
    raise HTTPException(
        status_code=404,
        detail=message
    )


def raise_bad_request(message: str="Bad request"):
    '''Raise 400'''
    raise HTTPException(
        status_code=400,
        detail=message
    )


def raise_server_error(message: str="Server error"):
    '''Raise 500'''
    raise HTTPException(
        status_code=500,
        detail=message
    )


def is_date(date_string: str):
    '''Check if str matche date format'''
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

