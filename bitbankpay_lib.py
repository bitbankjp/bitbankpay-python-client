# coding: utf-8
import json
import base64
import urllib2
import urllib

import bitbankpay_setting

def to_camel_case(snake_str, is_lower=True, to_uppers=['url']):
    """
    conbert to camel case string from snake case string.

    DocTest
    >>> to_camel_case('test_aaa_bbb')
    'testAaaBbb'
    >>> to_camel_case('test_aaa_url')
    'testAaaURL'
    >>> to_camel_case('test_aaa_url', False)
    'TestAaaURL'

    :param snake_str:
    :param is_lower:
    :param to_uppers:
    :return:
    """
    ret = ''
    components = snake_str.split('_')
    for component in components:
        if component in to_uppers:
            ret += component.upper()
        else:
            if is_lower:
                ret += component
            else:
                ret += component.title()
        is_lower = False

    return ret


def api_request(url, api_key, post_params=None, setting=None):
    """
    For request to BitbankPay API

    :param url: string
    :param api_key: string
    :param post_params: None or Dict
    :param setting: setting module
    :return response
    """
    print post_params

    if setting is None:
        setting = bitbankpay_setting

    logger = setting.get_logger()

    #check params
    if not url.strip():
        return {'error': 'url were blank.'}
    if not api_key.strip():
        return {'error': 'apiKey were blank.'}

    #request to api
    cookie_handler = urllib2.HTTPCookieProcessor()
    redirect_handler = urllib2.HTTPRedirectHandler()
    opener = urllib2.build_opener(redirect_handler, cookie_handler)

    api_key_base64 = base64.b64encode(api_key)

    opener.addheaders = [
        ('Content-Type', 'application/json'),
        ('Authorization', 'Basic ' + api_key_base64),
    ]

    response_string = ''
    try:
        print url
        if post_params is None:
            response_string = opener.open(url).read()
        else:
            response_string = opener.open(url, urllib.urlencode(post_params)).read()
    except Exception as e:
        #err_msg = str(e) + "\n" + traceback.format_exc()
        err_msg = str(e)
        logger.error(err_msg)
        return {'error': err_msg}

    try:
        response = json.loads(response_string)
    except ValueError:
        response = {'error': response_string}
        logger.error(response_string)

    return response


def accept_bitcoin(api_key,id):

    setting = bitbankpay_setting
    logger = setting.get_logger()

    post_params = {'uuid[]': id}

    #request to api
    cookie_handler = urllib2.HTTPCookieProcessor()
    redirect_handler = urllib2.HTTPRedirectHandler()
    opener = urllib2.build_opener(redirect_handler, cookie_handler)

    api_key_base64 = base64.b64encode(api_key)

    opener.addheaders = [
        ('Content-Type', 'application/json'),
        ('Authorization', 'Basic ' + api_key_base64),
    ]

    response_string = ''
    try:
        response_string = opener.open(setting.settings['apiURL'] + 'accept_bitcoin', urllib.urlencode(post_params)).read()
    except Exception as e:
        err_msg = str(e)
        logger.error(err_msg)
        return {'error': err_msg}

    try:
        response = json.loads(response_string)
    except ValueError:
        response = {'error': response_string}
        logger.error(response_string)

    return response

def accept_jpy_yen(api_key,id):

    setting = bitbankpay_setting
    logger = setting.get_logger()

    post_params = {'uuid[]': id}

    #request to api
    cookie_handler = urllib2.HTTPCookieProcessor()
    redirect_handler = urllib2.HTTPRedirectHandler()
    opener = urllib2.build_opener(redirect_handler, cookie_handler)

    api_key_base64 = base64.b64encode(api_key)

    opener.addheaders = [
        ('Content-Type', 'application/json'),
        ('Authorization', 'Basic ' + api_key_base64),
    ]

    response_string = ''
    try:
        response_string = opener.open(setting.settings['apiURL'] + 'accept_jpyyen', urllib.urlencode(post_params)).read()
    except Exception as e:
        err_msg = str(e)
        logger.error(err_msg)
        return {'error': err_msg}

    try:
        response = json.loads(response_string)
    except ValueError:
        response = {'error': response_string}
        logger.error(response_string)

    return response
    
def create_invoice(api_key,price,currency,item_name,
       order_id = None,
       setting = None
):
    """
    Create Invoice.

    DocTest
    >>> import bitbankpay_setting as test_setting
    >>> test_setting.settings['apiURL'] = 'https://api.bitbankpay.jp/api/v1/'
    >>> test_setting.settings['apiKey'] = 'API Key'
    >>> test_setting.settings['isLogging'] = False
    >>> res = create_invoice('API Key',100,'JPY','item_name','order_id')
    >>> res['result'] == 'OK'
    True
    >>> res['status'] == 'new'
    True
    >>> res['currency'] == 'BTC'
    True
    >>> res['btcPrice'] == '123.45'
    True

    :param api_key: In None case, it is set from bitchekpay_setting.
    :param price:
    :param currency: 'BTC' or 'JPY'. In None case, it is set from bitchekpay_setting.
    :param item_name: item name.
    :param order_id:
    :param setting: setting module
    :return: response dict
    """
    if setting is None:
        setting = bitbankpay_setting
    logger = setting.get_logger()

    import inspect
    args, _, _, locals = inspect.getargvalues(inspect.currentframe())
    not_post_params_set = set(['api_key', 'setting'])
    post_params = {}
    for arg_name in args:
        post_param_name = arg_name
        if locals[arg_name] is None:
            if setting.settings.has_key(post_param_name):
                if arg_name not in not_post_params_set:
                    post_params[post_param_name] = setting.settings[post_param_name]
        else:
            post_params[post_param_name] =locals[arg_name]

    logger.debug('post_params = ' + str(post_params))

    if api_key is None:
        api_key = setting.settings['apiKey']

    response = api_request(
        setting.settings['apiURL'] + 'invoice', api_key,
        post_params=post_params,
        setting=setting
    )

    return response

if __name__ == "__main__":
    import doctest
    doctest.testmod()

