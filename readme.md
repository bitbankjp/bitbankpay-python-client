# bitbankpay_python

## Execute Example

	$ python
	>>> import bitbankpay_lib as bbplib

	>>> bbplib.create_invoice('APK Key',100,'JPY','item_name','order_id')
	{u'status': u'new', u'invoiceTime': 1408610630, u'currentTime': 1408610630, u'url': u'https://api.bitbankpay.jp/payment/settlement/test/bcp53f5b1468b8ba9.06993685', u'price': u'1', u'btcPrice': u'1', u'currency': u'BTC', u'result': u'OK', u'expirationTime': 1408611530, u'id': u'bcp53f5b1468b8ba9.06993685'}


## Setting
Default is set in bitbankpay_setting.py.

## Logfile(default)
bitbankpay.log
