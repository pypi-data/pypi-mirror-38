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

import binascii
import mimetypes
import os
import struct

from pyrogram.api import functions, types
from pyrogram.api.errors import FileIdInvalid, FilePartMissing
from pyrogram.client.ext import BaseClient, utils


class SendVideo(BaseClient):
    def send_video(self,
                   chat_id: int or str,
                   video: str,
                   caption: str = "",
                   parse_mode: str = "",
                   duration: int = 0,
                   width: int = 0,
                   height: int = 0,
                   thumb: str = None,
                   supports_streaming: bool = True,
                   disable_notification: bool = None,
                   reply_to_message_id: int = None,
                   reply_markup=None,
                   progress: callable = None,
                   progress_args: tuple = ()):
        """Use this method to send video files.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            video (``str``):
                Video to send.
                Pass a file_id as string to send a video that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a video from the Internet, or
                pass a file path as string to upload a new video that exists on your local machine.

            caption (``str``, *optional*):
                Video caption, 0-1024 characters.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            width (``int``, *optional*):
                Video width.

            height (``int``, *optional*):
                Video height.

            thumb (``str``, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 90 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            supports_streaming (``bool``, *optional*):
                Pass True, if the uploaded video is suitable for streaming.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``callable``, *optional*):
                Pass a callback function to view the upload progress.
                The function must take *(client, current, total, \*args)* as positional arguments (look at the section
                below for a detailed description).

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function. Useful, for example, if you want to pass
                a chat_id and a message_id in order to edit a message with the updated progress.

        Other Parameters:
            client (:obj:`Client <pyrogram.Client>`):
                The Client itself, useful when you want to call other API methods inside the callback function.

            current (``int``):
                The amount of bytes uploaded so far.

            total (``int``):
                The size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`Message <pyrogram.Message>` is returned.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
        """
        file = None
        style = self.html if parse_mode.lower() == "html" else self.markdown

        if os.path.exists(video):
            thumb = None if thumb is None else self.save_file(thumb)
            file = self.save_file(video, progress=progress, progress_args=progress_args)
            media = types.InputMediaUploadedDocument(
                mime_type=mimetypes.types_map[".mp4"],
                file=file,
                thumb=thumb,
                attributes=[
                    types.DocumentAttributeVideo(
                        supports_streaming=supports_streaming or None,
                        duration=duration,
                        w=width,
                        h=height
                    ),
                    types.DocumentAttributeFilename(os.path.basename(video))
                ]
            )
        elif video.startswith("http"):
            media = types.InputMediaDocumentExternal(
                url=video
            )
        else:
            try:
                decoded = utils.decode(video)
                fmt = "<iiqqqqi" if len(decoded) > 24 else "<iiqq"
                unpacked = struct.unpack(fmt, decoded)
            except (AssertionError, binascii.Error, struct.error):
                raise FileIdInvalid from None
            else:
                if unpacked[0] != 4:
                    media_type = BaseClient.MEDIA_TYPE_ID.get(unpacked[0], None)

                    if media_type:
                        raise FileIdInvalid("The file_id belongs to a {}".format(media_type))
                    else:
                        raise FileIdInvalid("Unknown media type: {}".format(unpacked[0]))

                media = types.InputMediaDocument(
                    id=types.InputDocument(
                        id=unpacked[2],
                        access_hash=unpacked[3]
                    )
                )

        while True:
            try:
                r = self.send(
                    functions.messages.SendMedia(
                        peer=self.resolve_peer(chat_id),
                        media=media,
                        silent=disable_notification or None,
                        reply_to_msg_id=reply_to_message_id,
                        random_id=self.rnd_id(),
                        reply_markup=reply_markup.write() if reply_markup else None,
                        **style.parse(caption)
                    )
                )
            except FilePartMissing as e:
                self.save_file(video, file_id=file.id, file_part=e.x)
            else:
                for i in r.updates:
                    if isinstance(i, (types.UpdateNewMessage, types.UpdateNewChannelMessage)):
                        return utils.parse_messages(
                            self, i.message,
                            {i.id: i for i in r.users},
                            {i.id: i for i in r.chats}
                        )
