import logging

_logger = logging.getLogger(__name__)


def check_header( a_jwt , a_headers):
    w_token = get_token_from_header(a_headers)
    if w_token is None:
        return False
    return a_jwt.verify(w_token)


def get_token_decoded(a_jwt, a_headers):
    w_token = get_token_from_header(a_headers)
    if w_token is None:
        return False
    return a_jwt.get_token_decoded(w_token)

def get_token_from_header(a_headers):
    if "authorization" in a_headers:
        w_authorization = a_headers["authorization"]
        if w_authorization is not None and "Bearer" in w_authorization:
            w_token = w_authorization[len("Bearer "):]
            return w_token
        else:
            return None
    elif "Cookie" in a_headers:
        w_cookies = a_headers["Cookie"]
        w_token = ""
        if ";" in w_cookies:
            w_arr = w_cookies.split(";")
            for w_cookie in w_arr:
                if "_ycappuccino" in w_cookie:
                    w_token = w_cookie.split("=")[1]
        else:
            w_token = w_cookies.split("=")[1]
        _logger.info("token {}".format(w_token))
        return w_token
