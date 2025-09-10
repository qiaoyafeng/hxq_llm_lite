from constants import SUCCESS_CODE


def build_resp(code, data, message=None):
    resp = {
        "code": code,
        "message": message,
        "success": code == SUCCESS_CODE,
        "data": data,
    }
    return resp


def safe_int(value, default=0):
    try:
        return int(value)
    except Exception as e:
        _ = e
        return default
