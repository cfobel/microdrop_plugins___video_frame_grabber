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

from flatland import Element, Dict, String, Integer, Boolean, Float, Form
from flatland.validation import ValueAtLeast, ValueAtMost
from path import path

from utility.pygtkhelpers_widgets import Directory
from plugin_helpers import AppDataController, StepOptionsController,\
        get_plugin_version
from plugin_manager import IPlugin, Plugin, \
    implements, PluginGlobals, get_service_instance_by_name
from opencv.safe_cv import cv


PluginGlobals.push_env('microdrop.managed')

class VideoFrameGrabber(Plugin, AppDataController, StepOptionsController):
    implements(IPlugin)
    version = get_plugin_version(path(__file__).parent.parent)
    plugins_name = 'wheelerlab.video_frame_grabber'

    AppFields = Form.of(
        Directory.named('frame_output_dir').using(default='', optional=True),
    ) 

    StepFields = Form.of(
        Boolean.named('grab_frame').using(default=False, optional=True),
    )

    def __init__(self):
        self.name = self.plugins_name

    def on_step_swapped(self, original_step_number, new_step_number):
        if not self.get_step_value('grab_frame'):
            print '[VideoFrameGrabber] on_step_swapped():'\
                    'frame grab disabled for step %d' % (new_step_number)
            return

        if self.get_app_value('frame_output_dir'):
            output_dir = path(self.get_app_value('frame_output_dir'))
        else:
            output_dir = path('.')
        filename = '%d-%d.jpg' % (original_step_number, new_step_number)
        filename = output_dir.joinpath(filename)

        print '[VideoFrameGrabber] on_step_swapped():'\
                'save image of %d -> %d to %s' % (original_step_number,
                        new_step_number, filename)

        # Grab frame from dmf_device_controller plugin
        service = get_service_instance_by_name(
                'microdrop.gui.dmf_device_controller', env='microdrop')
        frame = service.grab_frame()

        if frame:
            # Save frame to file
            cv.SaveImage(filename, frame)


PluginGlobals.pop_env()
