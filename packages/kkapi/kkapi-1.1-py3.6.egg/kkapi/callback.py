# -*- coding: utf-8 -*-
class Callback(object):

    def __init__(self, callback):
        self.callback = callback

    def PinVerified(self, pin):
        self.callback("在兩分鐘內'" + pin + "'在手機的LINE上填入此PIN碼")

    def QrUrl(self, url, showQr=True):
        self.callback('在兩分鐘內在手機上的LINE上登入此連結\n' + url)
        if showQr:
            try:
                import pyqrcode
                url = pyqrcode.create(url)
                self.callback(url.terminal('green', 'white', 1))
            except:
                pass

    def default(self, str):
        self.callback(str)