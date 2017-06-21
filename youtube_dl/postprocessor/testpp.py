# coding: utf-8
from __future__ import unicode_literals
from pprint import pprint
import os

from .ffmpeg import FFmpegPostProcessor

class TestPP(FFmpegPostProcessor):
    def __init__(self, downloader=None):
        FFmpegPostProcessor.__init__(self, downloader)
        self._last = {}

    def run(self, info):
        # Only concerned with the Panopto extractor
        if info['extractor'] != 'Panopto' or info.get('playlist_id') is None:
            return [], info

        # Only want to combine videos from the same playlist
        # Also do nothing on the first video in each playlist
        if self._last.get('playlist_id') != info['playlist_id'] or self._last['webpage_url'] != info['webpage_url']:
            self._last = info
            return [], info

        out = os.path.dirname(os.path.realpath(info['filepath'])) + '/' + info['playlist_title'] + '.mp4'

        self._downloader.to_screen('[' + 'ffmpeg' + '] Combining Panopto videos...')
        self.run_ffmpeg_multiple_files([self._last['filepath'], info['filepath']], out, ['-t', '10', '-filter_complex', '[0] fps=30 [dv]; [1] fps=30 [screen]; [dv][screen] scale2ref=iw/6:ow/mdar [dv][screen]; [screen][dv] overlay=main_w-overlay_w:main_h-overlay_h', '-preset', 'ultrafast', '-crf', '30'])
        

        self._last = {}
        #return [self._last['filepath'], info['filepath']], info
        return [], info
