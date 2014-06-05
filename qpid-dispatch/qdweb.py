#!/usr/bin/env python

##
## Licensed to the Apache Software Foundation (ASF) under one
## or more contributor license agreements.  See the NOTICE file
## distributed with this work for additional information
## regarding copyright ownership.  The ASF licenses this file
## to you under the Apache License, Version 2.0 (the
## "License"); you may not use this file except in compliance
## with the License.  You may obtain a copy of the License at
##
##   http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing,
## software distributed under the License is distributed on an
## "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
## KIND, either express or implied.  See the License for the
## specific language governing permissions and limitations
## under the License.
##

import cgi
import cgitb
from proton import Messenger, Message, Timeout
from time import strftime, gmtime

updates_enabled = True
logfile = '/var/log/qdweb'

cgitb.enable()

def qdw_start(ctype):
    print "Content-Type: %s" % ctype
    print

def qdw_title(title):
    print '<html>'
    print '<head>'
    print '  <title>%s</title>' % title
    print '  <link rel="stylesheet" type="text/css" href="/css/qdweb.css" />'
    print '</head>'
    print '<body>'

def qdw_close():
    print '<center>'
    print 'Powered by <a href="http://qpid.apache.org/components/dispatch-router/index.html">Apache Qpid Dispatch</a> <img src="/feather.png" />'
    print '</center>'
    print '</body>'
    print '</html>'

def qdw_table(rows, heads=None, caption=None):
    if caption:
        print "<center><b>%s</b></center>" % caption
    print '<center><table cellpadding="4">'
    if heads:
        print '  <tr class="header">'
        for h in heads:
            print "    <td>%s</td>" % h
        print "  </tr>"
    ordinal = 0
    for row in rows:
        if (ordinal / 2) * 2 == ordinal:
            print '  <tr>'
        else:
            print '  <tr class="alt">'
        for r in row:
            print "    <td>%s</td>" % str(r)
        print "  </tr>"
        ordinal += 1
    print "</table></center>"

def qdw_yn(val, valid=True):
    if not valid:
        return "--"
    if val:
        return "Yes"
    return "No"

def qdw_val(val, valid=True):
    if not valid:
        return "--"
    return val

def qdw_maybe(val):
    if val:
        return val
    return "--"

def qdw_first_line(text):
    text = text.replace('<br ', '\n').replace('<p ', '\n')
    return text.split('\n')[0]

def qdw_log_query(text):
    fd = open(logfile, "a")
    fd.write(text)
    fd.write('\n')
    fd.close()

def qdw_do_action(db, form):
    action = form['action'].value

def qdw_menu():
    print '<center>'
    print '<table>'
    print '  <tr><td><font size="+2">'
    print '    <a href="qdweb.py">Main Page</a>&nbsp;'
    print '    <a href="qdweb.py?view=CONN">Connections</a>&nbsp;'
    print '    <a href="qdweb.py?view=LINK">Links</a>&nbsp;'
    print '    <a href="qdweb.py?view=ADDRESS">Addresses</a>&nbsp;'
    print '    <a href="qdweb.py?view=MEMORY">Memory</a>&nbsp;'
    print '  </td></tr>'
    print '</table></center><p /><hr width="85%"><p />'


def addr_class(addr):
    if not addr:
        return "-"
    if addr[0] == 'M' : return "mobile"
    if addr[0] == 'R' : return "router"
    if addr[0] == 'A' : return "area"
    if addr[0] == 'L' : return "local"
    return "unknown: %s" % addr[0]

def addr_text(addr):
    if not addr:
        return "-"
    return addr[1:]


class GeneralPage:
    def __init__(self, router, form):
        self.router = router
        self.form   = form

    def display(self):
        qdw_title("Qpid Dispatch Router in Docker - Main Page")
        qdw_menu()
        data = self.router.GetObject('org.apache.qpid.dispatch.router')[0]
        rows = []
        rows.append(["Mode", data.mode])
        rows.append(["Area", data.area])
        rows.append(["Router ID", data.router_id])
        rows.append(["Address Count", data.addr_count])
        rows.append(["Link Count", data.link_count])
        rows.append(["Node Count", data.node_count])
        qdw_table(rows, caption="Router Information")
        print '<hr width="85%"><p />'


class ConnPage:
    def __init__(self, router, form):
        self.router = router
        self.form   = form

    def display(self):
        qdw_title("Qpid Dispatch Router in Docker - Connections Page")
        qdw_menu()

        hdr = []
        hdr.append(Header("state"))
        hdr.append(Header("host"))
        hdr.append(Header("container"))
        hdr.append(Header("sasl-mechanisms"))
        hdr.append(Header("role"))
        hdr.append(Header("dir"))

        data = self.router.GetObject('org.apache.qpid.dispatch.connection')
        rows = []

        for conn in data:
            row = []
            row.append(conn.state)
            row.append(conn.host)
            row.append(conn.container)
            row.append(conn.sasl)
            row.append(conn.role)
            row.append(conn.dir)
            rows.append(row)

        qdw_table(rows, heads=hdr, caption="Connections")
        print '<hr width="85%"><p />'


class LinkPage:
    def __init__(self, router, form):
        self.router = router
        self.form   = form

    def display(self):
        qdw_title("Qpid Dispatch Router in Docker - Links Page")
        qdw_menu()

        hdr = []
        hdr.append(Header("type"))
        hdr.append(Header("dir"))
        hdr.append(Header("rindex"))
        hdr.append(Header("class"))
        hdr.append(Header("addr"))

        data = self.router.GetObject('org.apache.qpid.dispatch.router.link')
        rows = []

        for link in data:
            row = []
            row.append(link.link_type)
            row.append(link.link_dir)
            if link.link_type == "inter-router":
                row.append(link.index)
            else:
                row.append('-')
            row.append(addr_class(link.owning_addr))
            row.append(addr_text(link.owning_addr))
            rows.append(row)

        qdw_table(rows, heads=hdr, caption="Router Links")
        print '<hr width="85%"><p />'


class AddressPage:
    def __init__(self, router, form):
        self.router = router
        self.form   = form

    def display(self):
        qdw_title("Qpid Dispatch Router in Docker - Address Page")
        qdw_menu()

        hdr = []
        hdr.append(Header("class"))
        hdr.append(Header("address"))
        hdr.append(Header("in-proc", Header.Y))
        hdr.append(Header("local", Header.COMMAS))
        hdr.append(Header("remote", Header.COMMAS))
        hdr.append(Header("in", Header.COMMAS))
        hdr.append(Header("out", Header.COMMAS))
        hdr.append(Header("thru", Header.COMMAS))
        hdr.append(Header("to-proc", Header.COMMAS))
        hdr.append(Header("from-proc", Header.COMMAS))

        data = router.GetObject('org.apache.qpid.dispatch.router.address')
        rows = []

        for addr in data:
            row = []
            row.append(addr_class(addr.addr))
            row.append(addr_text(addr.addr))
            row.append(addr.in_process)
            row.append(addr.subscriber_count)
            row.append(addr.remote_count)
            row.append(addr.deliveries_ingress)
            row.append(addr.deliveries_egress)
            row.append(addr.deliveries_transit)
            row.append(addr.deliveries_to_container)
            row.append(addr.deliveries_from_container)
            rows.append(row)
        title = "Router Addresses"
        sorter = Sorter(hdr, rows, 'address', 0, True)
        dispRows = sorter.getSorted()

        qdw_table(dispRows, heads=hdr, caption="Router Addresses")
        print '<hr width="85%"><p />'


class MemoryPage:
    def __init__(self, router, form):
        self.router = router
        self.form   = form

    def display(self):
        qdw_title("Qpid Dispatch Router in Docker - Memory Page")
        qdw_menu()

        hdr = []
        hdr.append(Header("type"))
        hdr.append(Header("size", Header.COMMAS))
        hdr.append(Header("batch"))
        hdr.append(Header("thread-max", Header.COMMAS))
        hdr.append(Header("total", Header.COMMAS))
        hdr.append(Header("in-threads", Header.COMMAS))
        hdr.append(Header("rebal-in", Header.COMMAS))
        hdr.append(Header("rebal-out", Header.COMMAS))

        data = router.GetObject('org.apache.qpid.dispatch.allocator')
        rows = []

        for t in data:
            row = []
            row.append(t.name)
            row.append(t.type_size)
            row.append(t.transfer_batch_size)
            row.append(t.local_free_list_max)
            row.append(t.total_alloc_from_heap)
            row.append(t.held_by_threads)
            row.append(t.batches_rebalanced_to_threads)
            row.append(t.batches_rebalanced_to_global)
            rows.append(row)
        title = "Types"
        sorter = Sorter(hdr, rows, 'type', 0, True)
        dispRows = sorter.getSorted()

        qdw_table(dispRows, heads=hdr, caption="Router Memory Statistics")
        print '<hr width="85%"><p />'


def YN(val):
  if val:
    return 'Y'
  return 'N'

def Commas(value):
  sval = str(value)
  result = ""
  while True:
    if len(sval) == 0:
      return result
    left = sval[:-3]
    right = sval[-3:]
    result = right + result
    if len(left) > 0:
      result = ',' + result
    sval = left

def TimeLong(value):
  return strftime("%c", gmtime(value / 1000000000))

def TimeShort(value):
  return strftime("%X", gmtime(value / 1000000000))


class Header:
  """ """
  NONE = 1
  KMG = 2
  YN = 3
  Y = 4
  TIME_LONG = 5
  TIME_SHORT = 6
  DURATION = 7
  COMMAS = 8

  def __init__(self, text, format=NONE):
    self.text = text
    self.format = format

  def __repr__(self):
    return self.text

  def __str__(self):
    return self.text

  def formatted(self, value):
    try:
      if value == None:
        return ''
      if self.format == Header.NONE:
        return value
      if self.format == Header.KMG:
        return self.num(value)
      if self.format == Header.YN:
        if value:
          return 'Y'
        return 'N'
      if self.format == Header.Y:
        if value:
          return 'Y'
        return ''
      if self.format == Header.TIME_LONG:
         return TimeLong(value)
      if self.format == Header.TIME_SHORT:
         return TimeShort(value)
      if self.format == Header.DURATION:
        if value < 0: value = 0
        sec = value / 1000000000
        min = sec / 60
        hour = min / 60
        day = hour / 24
        result = ""
        if day > 0:
          result = "%dd " % day
        if hour > 0 or result != "":
          result += "%dh " % (hour % 24)
        if min > 0 or result != "":
          result += "%dm " % (min % 60)
        result += "%ds" % (sec % 60)
        return result
      if self.format == Header.COMMAS:
        return Commas(value)
    except:
      return "?"

  def numCell(self, value, tag):
    fp = float(value) / 1000.
    if fp < 10.0:
      return "%1.2f%c" % (fp, tag)
    if fp < 100.0:
      return "%2.1f%c" % (fp, tag)
    return "%4d%c" % (value / 1000, tag)

  def num(self, value):
    if value < 1000:
      return "%4d" % value
    if value < 1000000:
      return self.numCell(value, 'k')
    value /= 1000
    if value < 1000000:
      return self.numCell(value, 'm')
    value /= 1000
    return self.numCell(value, 'g')


class Display:
  """ Display formatting """
  
  def __init__(self, spacing=2, prefix="    "):
    self.tableSpacing    = spacing
    self.tablePrefix     = prefix
    self.timestampFormat = "%X"

  def formattedTable(self, title, heads, rows):
    fRows = []
    for row in rows:
      fRow = []
      col = 0
      for cell in row:
        fRow.append(heads[col].formatted(cell))
        col += 1
      fRows.append(fRow)
    headtext = []
    for head in heads:
      headtext.append(head.text)
    self.table(title, headtext, fRows)

  def table(self, title, heads, rows):
    """ Print a table with autosized columns """

    # Pad the rows to the number of heads
    for row in rows:
      diff = len(heads) - len(row)
      for idx in range(diff):
        row.append("")

    print title
    if len (rows) == 0:
      return
    colWidth = []
    col      = 0
    line     = self.tablePrefix
    for head in heads:
      width = len (head)
      for row in rows:
        text = row[col]
        if text.__class__ == str:
          text = text.decode('utf-8')
        cellWidth = len(unicode(text))
        if cellWidth > width:
          width = cellWidth
      colWidth.append (width + self.tableSpacing)
      line = line + head
      if col < len (heads) - 1:
        for i in range (colWidth[col] - len (head)):
          line = line + " "
      col = col + 1
    print line
    line = self.tablePrefix
    for width in colWidth:
      for i in range (width):
        line = line + "="
    print line

    for row in rows:
      line = self.tablePrefix
      col  = 0
      for width in colWidth:
        text = row[col]
        if text.__class__ == str:
          text = text.decode('utf-8')
        line = line + unicode(text)
        if col < len (heads) - 1:
          for i in range (width - len(unicode(text))):
            line = line + " "
        col = col + 1
      print line

  def do_setTimeFormat (self, fmt):
    """ Select timestamp format """
    if fmt == "long":
      self.timestampFormat = "%c"
    elif fmt == "short":
      self.timestampFormat = "%X"

  def timestamp (self, nsec):
    """ Format a nanosecond-since-the-epoch timestamp for printing """
    return strftime (self.timestampFormat, gmtime (nsec / 1000000000))

  def duration(self, nsec):
    if nsec < 0: nsec = 0
    sec = nsec / 1000000000
    min = sec / 60
    hour = min / 60
    day = hour / 24
    result = ""
    if day > 0:
      result = "%dd " % day
    if hour > 0 or result != "":
      result += "%dh " % (hour % 24)
    if min > 0 or result != "":
      result += "%dm " % (min % 60)
    result += "%ds" % (sec % 60)
    return result

class Sortable:
  """ """
  def __init__(self, row, sortIndex):
    self.row = row
    self.sortIndex = sortIndex
    if sortIndex >= len(row):
      raise Exception("sort index exceeds row boundary")

  def __cmp__(self, other):
    return cmp(self.row[self.sortIndex], other.row[self.sortIndex])

  def getRow(self):
    return self.row

class Sorter:
  """ """
  def __init__(self, heads, rows, sortCol, limit=0, inc=True):
    col = 0
    for head in heads:
      if head.text == sortCol:
        break
      col += 1
    if col == len(heads):
      raise Exception("sortCol '%s', not found in headers" % sortCol)

    list = []
    for row in rows:
      list.append(Sortable(row, col))
    list.sort()
    if not inc:
      list.reverse()
    count = 0
    self.sorted = []
    for row in list:
      self.sorted.append(row.getRow())
      count += 1
      if count == limit:
        break

  def getSorted(self):
    return self.sorted


class AmqpEntity(object):
    def __init__(self, values):
        self.values = {}
        for k,v in values.items():
            self.values[k.replace('-', '_')] = v

    def __getattr__(self, attr):
        if attr in self.values:
            return self.values[attr]
        raise Exception("Unknown attribute: %s" % attr)

    def __repr__(self):
        return "%r" % self.values


class BusManager:
    def __init__(self):
        pass

    def SetHost(self, host, router):
        self.M = Messenger()
        self.M.start()
        self.M.timeout = 3
        self.M.route("amqp:/*", "amqp://%s/$1" % host)
        if router:
            self.address = "amqp:/_topo/0/%s/$management" % router
        else:
            self.address = "amqp:/_local/$management"
        self.subscription = self.M.subscribe("amqp:/#")
        self.reply = self.subscription.address

    def Disconnect(self):
        self.M.stop()

    def GetObject(self, cls):
        request = Message()
        response = Message()

        request.address = self.address
        request.reply_to = self.reply
        request.correlation_id = 1
        request.properties = {u'operation':u'GET', u'type':cls}
        request.body = {'attributeNames': []}

        self.M.put(request)
        self.M.send()
        self.M.recv()
        self.M.get(response)

        if response.properties['status-code'] != 200:
            raise Exception("Agent reports: %d %s" % (response.properties['status-code'], response.properties['status-description']))

        entities = []
        results = response.body
        for e in results:
            entities.append(AmqpEntity(e))

        return entities


qdw_start("text/html")
form = cgi.FieldStorage()
router = BusManager()
router.SetHost("0.0.0.0", None)

if 'action' in form:
  if updates_enabled:
    qdw_do_action(router, form)

page = None
if 'view' in form:
  view = form['view'].value
  if view == 'GENERAL':
    page = GeneralPage(router, form)
  elif view == 'CONN':
    page = ConnPage(router, form)
  elif view == 'LINK':
    page = LinkPage(router, form)
  elif view == 'ADDRESS':
    page = AddressPage(router, form)
  elif view == 'MEMORY':
    page = MemoryPage(router, form)
  else:
    page = GeneralPage(router, form)
else:
  page = GeneralPage(router, form)

page.display()
router.Disconnect()
qdw_close()
