# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Implementation of ``usbinfo`` for Linux-based systems."""

import pyudev

from .posix import get_mounts


def usbinfo(decode_model=False, **kwargs):
    """Helper for usbinfo on Linux.

    Args:
        decode_model: Due to versions <=1.0.2 incorrectly using ID_MODEL, this
            allows for the newer API to return the proper product name.
        **kwargs: Additional keyword arguments specific to platform
            implementation.
    """
    info_list = []

    _mounts = get_mounts()

    context = pyudev.Context()
    devices = context.list_devices().match_property('ID_BUS', 'usb')

    device_it = devices.__iter__()

    while True:
        try:
            # We need to manually get the next item in the iterator because
            # pyudev.device may throw an exception
            device = next(device_it)
        except pyudev.device.DeviceNotFoundError:
            continue
        except StopIteration:
            break

        if decode_model:
            id_product = _decode(device.get('ID_MODEL_ENC', u''))
            id_vendor = _decode(device.get('ID_VENDOR_ENC', u''))
        else:
            id_product = device.get('ID_MODEL', u'')
            id_vendor = device.get('ID_VENDOR', u'')
        devinfo = {
            'bInterfaceNumber': device.get('ID_USB_INTERFACE_NUM', u''),
            'devname': device.get('DEVNAME', u''),
            'iManufacturer': id_vendor,
            'iProduct': id_product,
            'iSerialNumber': device.get('ID_SERIAL_SHORT', u''),
            'idProduct': device.get('ID_MODEL_ID', u''),
            'idVendor': device.get('ID_VENDOR_ID', u''),
        }

        mount = _mounts.get(device.get('DEVNAME'))
        if mount:
            devinfo['mount'] = mount

        info_list.append(devinfo)

    return info_list

def _decode(unicode_str):
    """Decode malformed unicode strings from pyudev.

    ID_MODEL_ENC and ID_VENDOR_ENC could return values as:

      u'Natural\xae\\x20Ergonomic\\x20Keyboard\\x204000'

    which would raise a UnicodeEncodeError. To work around this, the string
    is first fixed by replacing any extended-ASCII characters with an escaped
    character string.

    Args:
        unicode_str: Unicode string to decode.

    Returns:
        A decoded string.
    """
    fixed_str = ''.join(
        [c if ord(c) < 128 else '\\x%02x' % ord(c) for c in unicode_str])
    return fixed_str.decode('string_escape')
