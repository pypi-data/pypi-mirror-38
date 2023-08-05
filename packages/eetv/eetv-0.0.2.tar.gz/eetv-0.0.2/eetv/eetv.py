#!/usr/bin/env python
# coding: utf-8

import json
import logging
import requests

KEYS = {"on_off": "Power",
        "2": "2",
        "1": "1",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "delete": "Delete / Subtitle",
        "0": "0",
        "text": "Text",
        "prev": "Previous",
        "play_pause": "Play / Pause",
        "next": "Next",
        "guide": "Guide",
        "rec": "Record",
        "back": "Back",
        "menu": "Menu",
        "info": "Info",
        "green": "Green",
        "yellow": "Yellow",
        "blue": "Blue",
        "red": "Red",
        "ok": "OK",
        "vol_up": "Vol+",
        "vol_down": "Vol-",
        "left": "Left",
        "down": "Down",
        "up": "Up",
        "right": "Right",
        "ch_down": "Channel -",
        "ch_up": "Channel +",
        "mute": "Mute"
        }

_LOGGER = logging.getLogger(__name__)

class EETV(object):
    def __init__(self, hostname, app_key='', port=80, timeout=3, refresh_frequency=60):
        from datetime import timedelta
        self.hostname = hostname
        self.port = port
        self.app_key = app_key
        self.timeout = timeout
        self.channels = False
        # Default programme image used with EETV
        self.default_thumb = "http://{}:{}/EPG/Image/category?id=magazine"
        self.default_thumb = self.default_thumb.format(self.hostname, self.port)
        self.last_volume = 100
        self.current_url = '/Live/CurrentContent/getInfo'
        # Need to put a support Android Device UA otherwise you get OSD messages saying
        # you need to upgrade your app
        self.headers = {'user-agent': "EETV/7.2.27-26 (Linux; Android 6.0.1; Nexus 7)"}
        assert isinstance(self.info, dict), \
            'Failed to retrive info from {}'.format(self.hostname)
        self._cache_channel_img = {}
        self.refresh_frequency = timedelta(seconds=refresh_frequency)

    @property
    def standby_state(self):
        j = self.get_core_info()
        # Bit of a cludge as the API doesn't offer an on/off indicator
        # totalSpace is a proxy, when off it's 0, when on it's a non-zero value.
        return j['pvr']['status']['disk']['totalSpace'] > 0

    @property
    def channel(self):
        return self.get_current_channel_name()

    @property
    def channel_img(self):
        return self.get_current_channel_image()

    @channel.setter
    def channel(self, value):
        self.set_channel(value)

    @property
    def programme(self):
        return self.get_current_programme_info().get("programme_name", "Unknown")

    @property
    def programme_image(self):
        return self.get_current_programme_info().get("thumb", self.default_thumb)

    @property
    def media_state(self):
        return self.media_source

    @property
    def media_position(self):
        # TODO: FIX Media Position
        return self.info.get('playedMediaPosition')

    @property
    def media_type(self):
        return self.media_state

    @property
    def mac_address(self):
        core_info = self.get_core_info()
        mac_address = core_info["ooh"]["applicationId"]
        mac_address = ':'.join([mac_address[i:i+2] for i in range(0, len(mac_address), 2)])
        return mac_address

    @property
    def device_name(self):
        device_name = self.get_core_info()
        return device_name["system"]["friendlyName"]

    @property
    def wol_support(self):
        return False

    @property
    def is_on(self):
        return self.standby_state

    @property
    def info(self):
        return self.get_core_info()

    # TODO: Discovery
    @staticmethod
    def discover():
        pass

    def get_core_info(self):
        url = 'http://{}:{}/UPnP/Device/getInfo?appKey={}'.format(
                self.hostname, self.port, self.app_key)
        resp = requests.get(url, timeout=self.timeout, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_volume(self):
        vol = self.get_url("/RemoteControl/Volume/get")
        return int(vol['volume'])

    def set_volume(self, vol):
        if vol > 100:
            vol = 100
        elif vol < 0:
            vol = 0
        self.get_url("/RemoteControl/Volume/set", {"volume": vol}, False)

    def press_button(self, key):
        if key == "vol_up":
            vol = self.get_volume()
            self.set_volume(vol+7)
        elif key == "vol_down":
            vol = self.get_volume()
            self.set_volume(vol - 7)
        elif key == "mute":
            self.mute()
        else:
            self.get_url("/RemoteControl/KeyHandling/sendKey",
                         {"key": key, "avoidLongPress": "1"}, False)
        return True

    def get_url(self, url, args=None, json_formatted=True):
        url = 'http://{}:{}{}?appKey={}'.format(self.hostname, self.port, url, self.app_key)
        if args is not None:
            for key, value in args.items():
                url = url + "&" + key + "=" + str(value)
        resp = requests.get(url, timeout=self.timeout, headers=self.headers)
        resp.raise_for_status()
        if json_formatted is True:
            return resp.json()
        else:
            return True

    def state(self):
        return self.standby_state

    def get_channel_list(self):
        if self.channels is False:
            self.channels = self.get_channels()
            return self.channels
        else:
            return self.channels

    def turn_on(self):
        # TODO: Turning off when on
        # When turning on there will be approx 30 seconds before the recorder has started up
        # Until then we have no idea if the STB is turned on
        if not self.standby_state:
            self.press_button("on_off")

    def turn_off(self):
        if self.standby_state:
            self.press_button("on_off")

    def get_current_channel(self):
        j = self.get_url(self.current_url)
        if j.get('channel', "UNKNOWN") == "UNKNOWN":
            channel_info = {
                "name": "Unknown",
                "lcn": "Unknown",
                "id": "Unknown",
                "logo": "Unknown",
            }
        else:
            channel_info = {
                'name': j['channel']['name'],
                'lcn': j['channel']['zap'],
                'id': j['channel']['id'],
                'logo': self.get_channel_image(j['channel']['zap'])
            }
        return channel_info

    def get_current_channel_name(self):
        channel = self.get_current_channel()
        return channel['name']

    def get_current_channel_image(self):
        channel = self.get_current_channel()
        return channel['logo']

    def get_channel_image(self, lcn):
        for channel in self.get_channel_list():
            if str(channel['zap']) == str(lcn):
                return channel['logo']
        return "Not Found"

    def get_channels(self):
        args = {"tvOnly": 0, "avoidHD": 0, "allowHidden": 0, "fields": "name,id,zap,isDVB,hidden,rank,isHD,logo,rec"}
        channels = self.get_url("/Live/Channels/getList", args)
        return channels

    def get_channel_names(self, json_output=False):
        channels = [x['name'] for x in self.get_channels()]
        return json.dumps(channels) if json_output else channels

    def set_channel(self, channel):
        self.get_url("/Live/Channels/zap", {"zap": channel}, False)
        return self.get_current_channel()

    def press_key(self, key):
        assert key in KEYS, 'No such key: {}'.format(key)
        return self.press_button(key)

    def volume_up(self):
        return self.press_key(key="vol_up")

    def volume_down(self):
        return self.press_key(key="vol_down")

    def mute(self):
        current = self.get_volume()
        if current == 0:
            self.set_volume(self.last_volume)
        else:
            self.last_volume = current
            self.set_volume(0)
        return True

    def channel_up(self):
        return self.press_key(key="ch_down")

    def channel_down(self):
        return self.press_key(key="ch_up")

    def play_pause(self):
        return self.press_key(key="play_pause")

    @property
    def media_source(self):
        if self.standby_state is False:
            return "Power Off"
        else:
            current_info = self.get_url(self.current_url)
            source = current_info["type"]
            if source == "rec":
                return "Recording"
            elif source == "live":
                return "Freeview TV"
            elif source is None:
                return "Menu, Radio, On Demand, EETV"
            else:
                return source

    def get_current_programme_info(self):
        if self.standby_state is False:
            return {"State": "Off"}
        else:
            j = self.get_url(self.current_url)

            programme_info = {
                "thumb": j.get('info', {}).get('event', {}).get('icon', self.default_thumb),
                "channel_name":  j.get('info', {}).get('event', {}).get('channelName', 'Unknown'),
                "episode_x_of_y": j.get('info', {}).get('event', {}).get('episodeInfo', 'Unknown'),
                "episode_title": j.get('info', {}).get('event', {}).get('text', 'Unknown'),
                "programme_title": j.get('info', {}).get('event', {}).get('name', 'Unknown'),
                "description": j.get('info', {}).get('event', {}).get('description', 'Unknown'),
            }
            return programme_info
