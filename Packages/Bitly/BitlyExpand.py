import urllib
import urllib2
import threading
import sublime
import json
import logging as logger

class BitlyExpand(threading.Thread):
  def __init__(self, sel, string, timeout, user, key):
    self.sel = sel
    self.original = string
    self.timeout = timeout
    self.result = None
    self.user = user or "bitlysublime"
    self.key = key or "R_ade2ddc55669904d7a5f1f1459645a3c"
    threading.Thread.__init__(self)

  def run(self):
    try:
      # print self.original
      encUrl = urllib.urlencode({"shortUrl": self.original})
      # print encUrl
      reqUrl = 'http://api.bitly.com/v3/expand?login=' + self.user + '&apiKey=' + self.key + '&' + encUrl
      # print "reqUrl: " + reqUrl
      request = urllib2.Request(reqUrl, headers={"User-Agent": "Sublime Bitly"})
      http_file = urllib2.urlopen(request, timeout=self.timeout)
      bitlyRes = http_file.read()
      bitlyObj = json.loads(bitlyRes)
      # print bitlyObj
      self.result = bitlyObj['data']['expand'][0]['long_url']
      # print self.result
      # print self.result[0]['long_url']
      return
    except (urllib2.HTTPError) as (e):
      err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
    except (urllib2.URLError) as (e):
      err = '%s: URL error %s contacting API' % (__name__, str(e.reason))

    sublime.error_message(err)
    self.result = False
