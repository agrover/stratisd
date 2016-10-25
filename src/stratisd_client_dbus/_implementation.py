# Copyright 2016 Red Hat, Inc.
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

"""
Classes to implement dbus interface.
"""

import abc

from into_dbus_python import xformer

class Interface(abc.ABC):
    """
    Parent class for an interface hierarchy.
    """

    _METHODS = abc.abstractproperty(doc="map from method name to data")
    _XFORMERS = abc.abstractproperty(doc="map from signature to xformer")
    _INTERFACE_NAME = abc.abstractproperty(doc="interface name")
    _PROPERTIES_INTERFACE_NAME = 'org.freedesktop.DBus.Properties'

    @classmethod
    def callMethod(cls, proxy_object, method_name, *args):
        """
        Call a dbus method on a proxy object.

        :param proxy_object: the proxy object to invoke the method on
        :param method_name: a method name
        :param args: the arguments to pass to the dbus method

        :returns: the result of the call
        :rtype: object * int * str

        This method intentionally permits lower-level exceptions to be
        propagated.
        """
        input_signature = cls._METHODS[method_name]

        if input_signature not in cls._XFORMERS:
            cls._XFORMERS[input_signature] = xformer(input_signature)
        xformed_args = cls._XFORMERS[input_signature](args)

        dbus_method = getattr(proxy_object, method_name)
        return dbus_method(*xformed_args, dbus_interface=cls._INTERFACE_NAME)

    @classmethod
    def getProperty(cls, proxy_object, name):
        """
        Get a property with name 'name'.

        :param proxy_object: the proxy object
        :param str name: the name of the property

        :returns: the value of the property
        :rtype: object
        """
        return proxy_object.Get(
           cls._INTERFACE_NAME,
           name,
           dbus_interface=cls._PROPERTIES_INTERFACE_NAME
        )
