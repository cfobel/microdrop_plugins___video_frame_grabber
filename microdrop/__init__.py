"""
Copyright 2011 Ryan Fobel

This file is part of dmf_control_board.

dmf_control_board is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

dmf_control_board is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with dmf_control_board.  If not, see <http://www.gnu.org/licenses/>.
"""

import utility
try:
    from ...dmf_control_board import *
    from ...dmf_control_board.microdrop.feedback import *
except:
    # Raise the exception(s) if we're running the program (these exceptions
    # are expected when generating documentation with doxygen, so in that case
    # we can safely ignore them).
    if utility.PROGRAM_LAUNCHED:
        raise
from flatland import Element, Dict, String, Integer, Boolean, Float, Form
from flatland.validation import ValueAtLeast, ValueAtMost

from plugin_helpers import AppDataController, StepOptionsController,\
        get_plugin_version
from plugin_manager import IPlugin, Plugin, \
    implements, PluginGlobals, get_service_instance


PluginGlobals.push_env('microdrop.managed')

class VideoFrameGrabber(Plugin, AppDataController, StepOptionsController):
    implements(IPlugin)
    version = get_plugin_version(path(__file__).parent.parent)
    plugins_name = 'wheelerlab.video_frame_grabber'

    AppFields = Form.of() 
    StepFields = Form.of()

    def __init__(self):
        self.name = self.plugins_name

    def on_step_options_changed(self, plugin, step_number):
        print '[VideoFrameGrabber] on_step_options_changed():'\
                '%s step #%d' % (plugin, step_number)

PluginGlobals.pop_env()
