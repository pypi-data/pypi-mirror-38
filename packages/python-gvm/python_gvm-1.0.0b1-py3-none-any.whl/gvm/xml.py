# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import defusedxml.lxml as secET

from lxml import etree

class XmlCommandElement:

    def __init__(self, element):
        self._element = element

    def add_element(self, name, text=None, attrs=None):
        node = etree.SubElement(self._element, name, attrib=attrs)
        node.text = text
        return XmlCommandElement(node)

    def set_attribute(self, name, value):
        self._element.set(name, value)

    def set_attributes(self, attrs):
        """Set several attributes at once.

        Arguments:
            attrs (dict): Attributes to be set on the element
        """
        for key, value in attrs.items():
            self._element.set(key, value)

    def append_xml_str(self, xml_text):
        """Append a xml element in string format."""
        node = secET.fromstring(xml_text)
        self._element.append(node)

    def to_string(self):
        return etree.tostring(self._element).decode('utf-8')

    def __str__(self):
        return self.to_string()


class XmlCommand(XmlCommandElement):

    def __init__(self, name):
        super().__init__(etree.Element(name))


def pretty_print(xml):
    """Prints beautiful XML-Code

    This function gets an object of list<lxml.etree._Element>
    or directly a lxml element.
    Print it with good readable format.

    Arguments:
        xml: List<lxml.etree.Element> or directly a lxml element
    """
    if isinstance(xml, list):
        for item in xml:
            if etree.iselement(item):
                print(etree.tostring(item, pretty_print=True).decode('utf-8'))
            else:
                print(item)
    elif etree.iselement(xml):
        print(etree.tostring(xml, pretty_print=True).decode('utf-8'))
