#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# threaded.py - threaded use of pyinotify
# Copyright (C) 2006  Sébastien Martini <sebastien.martini@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

# usage: ./threaded.py '/path-to-watch'


from pyinotify import ThreadedINotify, EventsCodes, ProcessEvent

class PExample(ProcessEvent):
    """
    PExample class: introduces how to subclass ProcessEvent.
    """

    def process_default(self, event_k, event):
        """
        new default processing method
        """
        print 'PExample::process_default'
        super(PExample, self).process_default(event_k, event)

    # The followings events are individually handled

    def process_IN_MODIFY(self, event_k):
        """
        process 'IN_MODIFY' events
        """
        print 'PExample::process_IN_MODIFY'
        super(PExample, self).process_default(event_k, 'IN_MODIFY')

    def process_IN_OPEN(self, event_k):
        """
        process 'IN_OPEN' events
        """
        print 'PExample::process_IN_OPEN'
        super(PExample, self).process_default(event_k, 'IN_OPEN')



if __name__ == '__main__':
    #
    # - Personalized monitoring: watch for selected events and
    #   do processing with PExample()
    # - The watched path is '/tmp' (by default) or the first
    #   command line argument if given.
    # - A separate thread is instanciated and the monitoring thread
    #   serve forever, type c^c to stop it.
    # - You can read a non-threaded version of this example in
    #   simple_example.py
    #
    import sys

    path = '/tmp' # default watched path
    if sys.argv[1:]:
        path = sys.argv[1]

    # only watch those events
    mask = EventsCodes.IN_MODIFY | EventsCodes.IN_DELETE | \
           EventsCodes.IN_OPEN | EventsCodes.IN_ATTRIB | \
           EventsCodes.IN_CREATE

    # class instance and init
    ino = ThreadedINotify()

    # start thread
    ino.start()

    # watch path for events handled by mask and give an instance of
    # PExample as processing function.
    ino.add_watch(path, mask, PExample())

    print 'start monitoring %s with mask %d' % (path, mask)

    # keep artificially the main thread alive forever
    while True:
        try:
            import time
            time.sleep(5)
        except KeyboardInterrupt:
            # ...until c^c signal
            print 'stop monitoring...'
            ino.stop()
            break
        except Exception, err:
            # otherwise keep on looping
            print err
