#!/usr/bin/python
__author__ = 'sungwoo'

# http://docs.gstreamer.com/display/GstSDK/Basic+tutorial+2%3A+GStreamer+concepts

import sys
import gst
import gtk


# create the elements
source = gst.element_factory_make("videotestsrc", "source")
sink = gst.element_factory_make("autovideosink", "sink")

# create empty pipleline
pipeline = gst.Pipeline("test-pipeline")

if not pipeline or not source or not sink:
    print "Not all elements could be created."
    sys.exit(2)

# build the pipeline
pipeline.add_many(source, sink)
if source.link(sink) != True:
    print "Elements could not be linked."
    sys.exit(2)

# modify the source's properties
source.set_property("pattern", 0)

# start playing
ret = pipeline.set_state(gst.STATE_PLAYING)
if ret == gst.STATE_CHANGE_FAILURE:
    print "Unable to set the pipeline to the playing state."
    sys.exit(2)

# wait until error or EOS
bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE, gst.MESSAGE_ERROR | gst.MESSAGE_EOS)

# parse message
if msg:
    err = None
    debug_info = None
    def error():
        msg.parse_error(err, debug_info)
        print "Error received from element %s: %s" % (msg.name, err.message)
        print "Debugging information: %s" % (debug_info if debug_info else "none")

    def eos():
        print "End-Of-Stream reached."

    handlers = {
        gst.MESSAGE_ERROR: error,
        gst.MESSAGE_EOS: eos
    }

    handler = handler[msg.type];
    if handler:
        handler()
    else:
        print "Unexpected message received."

pipeline.set_state(gst.STATE_NULL)
