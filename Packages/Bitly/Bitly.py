import sublime
import sublime_plugin
import re
import json
import urlparse
import logging as logger

from BitlyShorten import BitlyShorten 
from BitlyExpand import BitlyExpand

# The inspiration for this is the following Textmate plugin:
# http://bit.ly/18MdHDI
#
# replace with regex from here: http://bit.ly/18siBsM
# here is the full explanation of this regex: http://bit.ly/HdQl3F
# Using now:
# \b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^%s\s]|/)))
# Original Gruber:
# \b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))
# 1. \b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]|/)))
# 2. \b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[-!\"#$%&\'()*+,./:;<=>?@\\[\\\\]^_`{|}~]\s]|/)))
# 3. \b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\s]|/)))
# 4. Jeff Atwoods \(?\bhttp://[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]
#     This also has a parens cleanup routine at the end of it


# This shortens URLs using the bit.ly service
class BitlyShortenCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.settings = sublime.load_settings("Bitly.sublime-settings")
    logger.debug("inside BitlyShortenCommand.run()")
    self.urls = self.view.find_all(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\s]|/)))\b')
    logger.debug(self.urls)
    threads = []
    for url in self.urls:
      logger.debug(url)
      string = self.view.substr(url)
      string = self.strip_parens(string)
      thread = BitlyShorten(url, string, 15, self.settings.get("api_login"), self.settings.get("api_key"))
      threads.append(thread)
      thread.start()
    edit = self.view.begin_edit('bitly')
    self.handle_threads(edit, threads)

  def handle_threads(self, edit, threads, offset=0, i=0, dir=1):
    next_threads = []
    for thread in threads:
      if thread.is_alive():
        next_threads.append(thread)
        continue
      if thread.result == False:
        continue
      offset = self.replace(edit, thread, offset)

    threads = next_threads

    if len(threads):
      # This animates a little activity indicator in the status area
      before = i % 8
      after = (7) - before
      if not after:
        dir = -1
      if not before:
        dir = 1
      i += dir
      self.view.set_status('bitly', 'Bitly [%s=%s]' % (' ' * before, ' ' * after))

      sublime.set_timeout(lambda: self.handle_threads(edit, threads, offset, i, dir), 100)
      return

    self.view.end_edit(edit)

    self.view.erase_status('bitly')
    matches = len(self.urls)
    sublime.status_message('Bitly successfully run on %s selection%s' % (matches, '' if matches == 1 else 's'))

  def replace(self, edit, thread, offset):
    sel = thread.sel
    original = thread.original
    result = thread.result

    # Here we adjust each selection for any text we have already inserted
    if offset:
      # print 'offset: %s' % offset
      sel = sublime.Region(sel.begin() + offset, sel.end() + offset)

    self.view.replace(edit, sel, result)

    # We add the end of the new text to the selection
    return offset + len(result) - len(original)

  def strip_parens(self, strUrl):
    asStr = str(strUrl)
    if asStr[-1] == ")":
      return asStr[0:len(asStr)-1]
    else:
      return asStr

# This expands a bitly URL
class BitlyExpandCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.settings = sublime.load_settings("Bitly.sublime-settings")
    logger.debug("inside BitlyExpandCommand.run()")

    self.view = self.window.active_view()
    self.selections = self.view.sel()
    # print self.sel
    threads = []

    for selection in self.selections:
      # print selection
      string = self.view.substr(selection)
      # print string
      thread = BitlyExpand(selection, string, 15, self.settings.get("api_login"), self.settings.get("api_key"))
      threads.append(thread)
      thread.start()
    edit = self.view.begin_edit('bitly')
    self.handle_threads(edit, threads)

  def handle_threads(self, edit, threads, offset=0, i=0, dir=1):
    next_threads = []
    for thread in threads:
      if thread.is_alive():
        next_threads.append(thread)
        continue
      if thread.result == False:
        continue
      offset = self.replace(edit, thread, offset)
    threads = next_threads

    if len(threads):
      # This animates a little activity indicator in the status area
      before = i % 8
      after = (7) - before
      if not after:
        dir = -1
      if not before:
        dir = 1
      i += dir
      self.view.set_status('bitly', 'Bitly [%s=%s]' % (' ' * before, ' ' * after))

      sublime.set_timeout(lambda: self.handle_threads(edit, threads, offset, i, dir), 100)
      return

    self.view.end_edit(edit)

    self.view.erase_status('bitly')
    matches = len(self.selections)
    sublime.status_message('Bitly successfully run on %s selection%s' % (matches, '' if matches == 1 else 's'))

  def replace(self, edit, thread, offset):
    # print thread.sel
    sel = thread.sel
    original = thread.original
    # print "original: " + original
    logger.debug("original: " + original)
    result = thread.result
    # print "result: " + result
    logger.debug("result: " + result)

    # Here we adjust each selection for any text we have already inserted
    if offset:
      # print 'offset: %s' % offset
      logger.debug('offset: %s' % offset)
      sel = sublime.Region(sel.begin() + offset, sel.end() + offset)

    self.view.replace(edit, sel, result)

    # We add the end of the new text to the selection
    return offset + len(result) - len(original)