#!/usr/bin/env python
# coding: utf-8

import asyncio
import logging
import argparse


from eetv import EETV


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='action', help='Action')
    parser.add_argument(
        '-H', '--hostname',
        required=True,
        help='IP address or hostname of the EETV Set Top Box'
    )
    parser.add_argument(
        '-K', '--app-key',
        required=True,
        help='Application Key for EETV Set Top Box'
    )
    parser.add_argument(
        '-j', '--json',
        action='store_true',
        default=False,
        required=False,
        help='Format output as JSON'
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        default=False,
        required=False,
        help='Debug mode'
    )
    key_parser = subparsers.add_parser('key', help='Press an arbitrary key')
    key_parser.add_argument('key', help='Name or ID of the key to press')
    vol_parser = subparsers.add_parser('vol', help='Volume Control')
    vol_parser.add_argument('volume_action', choices=['up', 'down', 'mute'])
    subparsers.add_parser('info', help='Get info')
    subparsers.add_parser('test', help='Get info')
    subparsers.add_parser('programme', help='Get current programme')
    subparsers.add_parser('channel', help='Get current channel')
    subparsers.add_parser('device_name', help='Shows the EETV Box Name')
    subparsers.add_parser('device_mac', help='Shows the EETV Box MAC Address')
    subparsers.add_parser('media_source', help='Shows the EETV Box Active Source')
    subparsers.add_parser('media_source_details', help='Shows the EETV Box Active Source Details')
    subparsers.add_parser('channellogo', help='Get current channel logo')
    subparsers.add_parser('channels', help='Get list of channels')
    subparsers.add_parser('state', help='Get the current state (on or off)')
    subparsers.add_parser('on', help='Turn the EETV set top box on')
    subparsers.add_parser('off', help='Turn the EETV set top box off')
    channel_parser = subparsers.add_parser(
        'channel', help='Get or set the current channel'
    )
    channel_parser.add_argument('CHANNEL', nargs='?')
    # Debuggign methods
    subparsers.add_parser('notify', help='Wait and notify of new events')
    op_parser = subparsers.add_parser('op', help='[DEBUG] Send request')
    op_parser.add_argument('OPERATION', help='Operation')
    return parser.parse_args()


def main():
    args = parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    output = ''
    l = EETV(args.hostname,args.app_key)

    if args.action == 'info':
        output = l.info
    elif args.action == 'state':
        output = 'on' if l.state() else 'off'
    elif args.action == 'on':
        output = l.turn_on()
    elif args.action == 'device_name':
        output = l.device_name
    elif args.action == 'device_mac':
        output = l.mac_address
    elif args.action == 'media_source':
        output = l.media_source
    elif args.action == 'media_source_details':
        output = l.media_source_details
    elif args.action == 'off':
        output = l.turn_off()
    elif args.action == 'key':
        output = l.press_key(args.key)
    elif args.action == 'test':
        output = l.media_state
    elif args.action == 'vol':
        if args.volume_action == 'up':
            output = l.volume_up()
        elif args.volume_action == 'down':
            output = l.volume_down()
        elif args.volume_action == 'mute':
            output = l.mute()
    elif args.action == 'channel':
        if args.CHANNEL:
            if args.CHANNEL.lower() == 'list':
                output = l.get_channel_names(args.json)
            else:
                output = l.set_channel(args.CHANNEL)
        else:
            output = l.get_current_channel_name()
    elif args.action == "channellogo":
        output = l.get_current_channel_image()
    elif args.action == 'channel':
        output = l.channel
    elif args.action == 'programme':
        output = l.get_current_programme_info()
    elif args.action == 'channels':
        output = l.get_channels()
    if output:
        if args.json:
            from pprint import pprint
            pprint(output)
        else:
            print(output)


if __name__ == '__main__':
    main()
