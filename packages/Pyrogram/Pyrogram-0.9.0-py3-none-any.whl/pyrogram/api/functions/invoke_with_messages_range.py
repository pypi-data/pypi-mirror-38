# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.api.core import *


class InvokeWithMessagesRange(Object):
    """Attributes:
        ID: ``0x365275f2``

    Args:
        range: :obj:`MessageRange <pyrogram.api.types.MessageRange>`
        query: Any method from :obj:`pyrogram.api.functions`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Any object from :obj:`pyrogram.api.types`
    """

    ID = 0x365275f2

    def __init__(self, range, query):
        self.range = range  # MessageRange
        self.query = query  # !X

    @staticmethod
    def read(b: BytesIO, *args) -> "InvokeWithMessagesRange":
        # No flags
        
        range = Object.read(b)
        
        query = Object.read(b)
        
        return InvokeWithMessagesRange(range, query)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.range.write())
        
        b.write(self.query.write())
        
        return b.getvalue()
