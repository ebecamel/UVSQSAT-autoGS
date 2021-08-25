#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Decoder from IQ file for UVSQ-SAT
# Author: Enzo BECAMEL F4IAI
# Description: Decoder for UVSQ-SAT
# GNU Radio version: 3.8.3.1

from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import satellites
import satellites.components.datasinks
import satellites.core
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


class nogui_decoder_UVSQSAT_IQ(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Decoder from IQ file for UVSQ-SAT")

        ##################################################
        # Variables
        ##################################################
        self._start_time_value_config = configparser.ConfigParser()
        self._start_time_value_config.read('/path/to/start_time.ini')
        try: start_time_value = self._start_time_value_config.get('main', 'key')
        except: start_time_value = "time"
        self.start_time_value = start_time_value
        self.samp_rate = samp_rate = 39000

        ##################################################
        # Blocks
        ##################################################
        self.satellites_telemetry_parser_0 = satellites.components.datasinks.telemetry_parser('ax25', file = 'grc_out.txt', options="")
        self.satellites_submit_0 = satellites.submit('https://db.satnogs.org/api/telemetry/', 47438, 'your_call', 0.000000, 0.000000, start_time_value)
        self.satellites_satellite_decoder_0 = satellites.core.gr_satellites_flowgraph(norad = 47438, samp_rate = samp_rate, grc_block = True, iq = True, options = "")
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/tmp/rx.cf32', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.satellites_submit_0, 'in'))
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.satellites_telemetry_parser_0, 'in'))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.satellites_satellite_decoder_0, 0))


    def get_start_time_value(self):
        return self.start_time_value

    def set_start_time_value(self, start_time_value):
        self.start_time_value = start_time_value

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)





def main(top_block_cls=nogui_decoder_UVSQSAT_IQ, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
