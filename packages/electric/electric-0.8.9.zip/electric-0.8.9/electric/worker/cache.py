import logging

from electric.models import DeviceInfo, ChannelStatus
from electric.worker.casefancontrol import CaseFanControl

logger = logging.getLogger('electric.worker.router')


class Cache(object):
    def __init__(self):
        self.device_info = None
        self.channels = None
        self.case_fan_controller = None
        self.reset()

    def reset(self):
        self.device_info = DeviceInfo()
        self.channels = [
            ChannelStatus(), ChannelStatus()
        ]
        self.case_fan_controller = CaseFanControl()
        logger.info("cache values have been reset")

    def get_device_info(self):
        return self.device_info

    def set_device_info(self, info):
        self.device_info = info

    def get_channel_status(self, channel):
        channel = int(channel)
        assert (channel == 0 or channel == 1)
        return self.channels[channel]

    def set_channel_status(self, channel, status):
        channel = int(channel)
        assert (channel == 0 or channel == 1)
        self.channels[channel] = status

    def get_case_fan_controller(self):
        return self.case_fan_controller


values = Cache()

