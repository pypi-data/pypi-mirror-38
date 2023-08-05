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


class ExportedAuthorization(Object):
    """Attributes:
        ID: ``0xdf969c2d``

    Args:
        id: ``int`` ``32-bit``
        bytes: ``bytes``

    See Also:
        This object can be returned by :obj:`auth.ExportAuthorization <pyrogram.api.functions.auth.ExportAuthorization>`.
    """

    ID = 0xdf969c2d

    def __init__(self, id: int, bytes: bytes):
        self.id = id  # int
        self.bytes = bytes  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "ExportedAuthorization":
        # No flags
        
        id = Int.read(b)
        
        bytes = Bytes.read(b)
        
        return ExportedAuthorization(id, bytes)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        b.write(Bytes(self.bytes))
        
        return b.getvalue()
