'''
Tools to pull data out of the current session to re-use them
'''

import flask

import sepiida.session

def extract_credentials(_request):
    '''
    @param request url request object/dict
    @returns dict of {user,username, password, session-secret)
    dict value is None values missing from flask context'''
    user     = None
    username = None
    password = None
    session  = None

    if flask.has_request_context():
        user     = sepiida.session.current_user_uri()
        username = _request.authorization.get('username') if _request.authorization else None
        password = _request.authorization.get('password') if _request.authorization else None
        session  =  _request.cookies.get('session', None)

    return {
        'password'  : password,
        'session'   : session,
        'user'      : user,
        'username'  : username,
    }
