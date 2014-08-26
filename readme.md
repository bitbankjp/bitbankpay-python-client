# bitcheckpay_python

## Execute Example

	$ python
	>>> import bitcheckpay_lib as bcplib

	>>> bcplib.create_invoice(10.00, 'Order description')
	{u'status': u'new', u'invoiceTime': 1408610630, u'currentTime': 1408610630, u'url': u'https://bitcheckpay.jp/payment/settlement/test/bcp53f5b1468b8ba9.06993685', u'price': u'1', u'btcPrice': u'1', u'currency': u'BTC', u'result': u'OK', u'expirationTime': 1408611530, u'id': u'bcp53f5b1468b8ba9.06993685'}

	>>> bcplib.get_invoice('bcp53f5b1468b8ba9.06993685')
	{u'status': u'new', u'invoiceTime': 1408610630, u'currentTime': 1408610662, u'url': u'https://bitcheckpay.jp/payment/settlement/test/bcp53f5b1468b8ba9.06993685', u'price': u'1', u'btcPrice': u'1', u'currency': u'BTC', u'result': u'OK', u'expirationTime': 1408611530, u'id': u'bcp53f5b1468b8ba9.06993685'}


## Doctest

OK case

	$ python bitcheckpay_lib.py


NG case

	$ python bitcheckpay_lib.py
	**********************************************************************
	File "bitcheckpay_lib.py", line 181, in __main__.get_invoice
	Failed example:
	    res['result'] == 'OK'
	Expected:
	    True
	Got:
	    False
	**********************************************************************
	1 items had failures:
	   1 of  10 in __main__.get_invoice
	***Test Failed*** 1 failures.


## Setting
Default is set in bitcheckpay_setting.py.

## Logfile(default)
bitcheckpay.log
