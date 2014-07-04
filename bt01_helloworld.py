#!/usr/bin/python
__author__ = 'sungwoo'

# http://docs.gstreamer.com/pages/viewpage.action?pageId=327735

import gst
import gtk

pipeline = gst.parse_launch("playbin2 uri=http://docs.gstreamer.com/media/sintel_trailer-480p.webm")
pipeline.set_state(gst.STATE_PLAYING)
bus = pipeline.get_bus()
bus.timed_pop_filtered(gst.CLOCK_TIME_NONE, gst.MESSAGE_ERROR | gst.MESSAGE_EOS)
pipeline.set_state(gst.STATE_NULL)