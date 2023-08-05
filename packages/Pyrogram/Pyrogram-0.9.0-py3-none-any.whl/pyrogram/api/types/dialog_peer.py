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


class DialogPeer(Object):
    """Attributes:
        ID: ``0xe56dbf05``

    Args:
        peer: Either :obj:`PeerUser <pyrogram.api.types.PeerUser>`, :obj:`PeerChat <pyrogram.api.types.PeerChat>` or :obj:`PeerChannel <pyrogram.api.types.PeerChannel>`

    See Also:
        This object can be returned by :obj:`messages.GetDialogUnreadMarks <pyrogram.api.functions.messages.GetDialogUnreadMarks>`.
    """

    ID = 0xe56dbf05

    def __init__(self, peer):
        self.peer = peer  # Peer

    @staticmethod
    def read(b: BytesIO, *args) -> "DialogPeer":
        # No flags
        
        peer = Object.read(b)
        
        return DialogPeer(peer)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        return b.getvalue()
