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


class MessageActionChatCreate(Object):
    """Attributes:
        ID: ``0xa6638b9a``

    Args:
        title: ``str``
        users: List of ``int`` ``32-bit``
    """

    ID = 0xa6638b9a

    def __init__(self, title: str, users: list):
        self.title = title  # string
        self.users = users  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args) -> "MessageActionChatCreate":
        # No flags
        
        title = String.read(b)
        
        users = Object.read(b, Int)
        
        return MessageActionChatCreate(title, users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.title))
        
        b.write(Vector(self.users, Int))
        
        return b.getvalue()
