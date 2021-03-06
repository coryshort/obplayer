#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Copyright 2012-2015 OpenBroadcaster, Inc.

This file is part of OpenBroadcaster Player.

OpenBroadcaster Player is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenBroadcaster Player is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with OpenBroadcaster Player.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import absolute_import 

import obplayer

import gi
from gi.repository import GObject


def init():
    obplayer.Streamer = None
    obplayer.RTSPStreamer = None
    obplayer.RTPStreamer = None
    obplayer.YoutubeStreamer = None

    if obplayer.Config.setting('streamer_icecast_enable'):
        from .icecast import ObIcecastStreamer
        def delaystart():
            obplayer.Streamer = ObIcecastStreamer()
            if obplayer.Config.setting('streamer_play_on_startup'):
                obplayer.Streamer.start()
        GObject.timeout_add(1000, delaystart)

    obplayer.RTSPStreamer = None
    if obplayer.Config.setting('streamer_rtsp_enable'):
        from .rtsp import ObRTSPStreamer
        obplayer.RTSPStreamer = ObRTSPStreamer()

    if obplayer.Config.setting('streamer_rtp_enable'):
        from .rtp import ObRTPStreamer
        obplayer.ObRTPStreamer = ObRTPStreamer()
        obplayer.ObRTPStreamer.start()

    if obplayer.Config.setting('streamer_youtube_enable'):
        from .youtube import ObYoutubeStreamer
        obplayer.YoutubeStreamer = ObYoutubeStreamer()
        obplayer.YoutubeStreamer.start()

def quit():
    if obplayer.Streamer:
        obplayer.Streamer.quit()
    if obplayer.RTSPStreamer:
        obplayer.RTSPStreamer.quit()
    if obplayer.RTPStreamer:
        obplayer.RTPStreamer.quit()
    if obplayer.YoutubeStreamer:
        obplayer.YoutubeStreamer.quit()


"""
def start_streamer(name, clsname):
    exec("from .{0} import {1}".format(name, clsname))
    streamer = eval(name)()
    streamer.start()
    return streamer
"""

