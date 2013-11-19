#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# simple.py - non threaded use of pyinotify
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

# usage: ./simple.py '/path-to-watch'

from pyinotify import SimpleINotify, EventsCodes, ProcessEvent


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
    # - No additional thread is instancied and dedicated to the
    #   monitoring, instead of that this thread is in charge of
    #   all the job and block until the monitoring stop, type
    #   c^c to stop it.
    import sys

    path = '/tmp' # default watched path
    if sys.argv[1:]:
        path = sys.argv[1]

    # only watch those events
    mask = EventsCodes.IN_MODIFY | EventsCodes.IN_DELETE | \
           EventsCodes.IN_OPEN | EventsCodes.IN_ATTRIB | \
           EventsCodes.IN_CREATE

    # class instance and init
    ino = SimpleINotify()

    print 'start monitoring %s with mask %d' % (path, mask)

    added_flag = False
    # read and process events
    while True:
        try:
            if not added_flag:
                # on first iteration, add a watch on path:
                # watch path for events handled by mask and give an
                # instance of PExample as processing function.
                ino.add_watch(path, mask, PExample())
                added_flag = True
            ino.process_events()
            if ino.event_check():
                print "yo"
                ino.read_events()
        except KeyboardInterrupt:
            # ...until c^c signal
            print 'stop monitoring...'
            # close inotify's instance
            ino.close()
            break
        except Exception, err:
            # otherwise keep on watching
            print err

