#!/usr/bin/env python3
import logging
import os
import json
from gi.repository import Gtk, Gst, GLib

from lib.config import Config
import lib.connection as Connection

from .info_windows import QueueWindow

# time interval to re-fetch queue timings
TIMER_RESOLUTION = 1.0

class QueuesWindowController():

    def __init__(self, queue_win: QueueWindow):
        self.log = logging.getLogger('QueuesWindowController')

        # get related widgets
        self.win = queue_win
        self.store = queue_win.queue_store
        self.scroll = queue_win.queue_scroll

        # remember row iterators
        self.iterators = None

        # listen for queue_report from voctocore
        Connection.on('queue_report', self.on_queue_report)

    def on_queue_report(self, *report):
        # read string report into dictonary
        report = json.loads("".join(report))
        # check if this is the initial report
        if not self.iterators:
            # append report as rows to treeview store and remember row iterators
            self.iterators = dict()
            for queue, time in report.items():
                self.iterators[queue] = self.store.append((queue, time / Gst.SECOND))
        else:
            # just update values of second column
            for queue, time in report.items():
                self.store.set_value(self.iterators[queue], 1, time / Gst.SECOND)

    def show(self,visible=True):
        # check if widget is getting visible
        if visible:
            # request queue timing report from voctocore
            Connection.send('report_queues')
            # schedule repetition
            GLib.timeout_add(TIMER_RESOLUTION * 1000, self.do_timeout)
            # do the boring stuff
            self.win.show()
        else:
            self.win.hide()

    def do_timeout(self):
        # re-request queue report
        Connection.send('report_queues')
        # repeat if widget is visible
        return self.win.is_visible()
