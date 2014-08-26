# coding: utf-8
import json
import base64
import urllib2
import urllib

import bitcheckpay_setting

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
    For request to BitcheckPay API

    :param url: string
    :param api_key: string
    :param post_params: None or Dict
    :param setting: setting module
    :return response
    """
    print post_params

    if setting is None:
        setting = bitcheckpay_setting

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


def create_invoice(price, item_name,
       currency = None,
       redirect_url = None,
       order_id = None,
       api_key = None,
       setting = None,
):
    """
    Create Invoice.

    DocTest
    >>> import bitcheckpay_setting as test_setting
    >>> test_setting.settings['apiURL'] = 'https://bitcheckpay.jp/api/v1/'
    >>> test_setting.settings['apiKey'] = 'API Key'
    >>> test_setting.settings['isLogging'] = False
    >>> res = create_invoice(123.45, 'Test ITEM', currency='BTC', redirect_url='http://test/', order_id=123, setting=test_setting)
    >>> res['result'] == 'OK'
    True
    >>> res['status'] == 'new'
    True
    >>> res['currency'] == 'BTC'
    True
    >>> res['btcPrice'] == '123.45'
    True

    :param price:
    :param item_name: item name.
    :param currency: 'BTC' or 'JPY'. In None case, it is set from bitchekpay_setting.
    :param redirect_url: In None case, it is set from bitchekpay_setting.
    :param order_id:
    :param api_key: In None case, it is set from bitchekpay_setting.
    :param setting: setting module
    :return: response dict
    """
    if setting is None:
        setting = bitcheckpay_setting
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
        setting.settings['apiURL'] + 'invoice/', api_key,
        post_params=post_params,
        setting=setting
    )

    return response


def get_invoice(invoice_id,
       api_key = None,
       setting = None,
):
    """
    Get Invoice.

    DocTest
    >>> import bitcheckpay_setting as test_setting
    >>> test_setting.settings['apiURL'] = 'https://bitcheckpay.jp/api/v1/'
    >>> test_setting.settings['apiKey'] = 'API Key'
    >>> test_setting.settings['isLogging'] = False
    >>> res_at_create = create_invoice(123.45, 'Test ITEM', currency='BTC', redirect_url='http://test/', order_id=123, setting=test_setting)
    >>> res = get_invoice(res_at_create['id'], setting=test_setting)
    >>> res['result'] == 'OK'
    True
    >>> res['status'] == 'new'
    True
    >>> res['currency'] == 'BTC'
    True
    >>> res['btcPrice'] == '123.45'
    True

    :param invoice_id:
    :param api_key:
    :param setting:
    :return: response dict
    """
    if setting is None:
        setting = bitcheckpay_setting
    if api_key is None:
        api_key = setting.settings['apiKey']

    logger = setting.get_logger()

    url = setting.settings['apiURL'] + 'invoice/' + invoice_id

    logger.debug('url = ' + url)

    response = api_request(url, api_key, setting=setting)

    return response


if __name__ == "__main__":
    import doctest
    doctest.testmod()

