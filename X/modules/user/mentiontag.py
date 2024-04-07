from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message
from X.helpers.tools import get_arg
from X import *
from config import CMD_HANDLER

from .help import *

spam_chats = []


@Client.on_message(filters.command("mention", cmd) & filters.me)
async def mentionall(client: Client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    direp = message.reply_to_message
    args = get_arg(message)
    if not direp and not args:
        return await message.edit("**ᴅʀᴏᴘ ᴍᴇ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ!**")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}), "
        if usrnum == 5:
            if args:
                txt = f"{args}\n\n{usrtxt}"
                await client.send_message(chat_id, txt)
            elif direp:
                await direp.reply(usrtxt)
            await sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@Client.on_message(filters.command("cancel", cmd) & filters.me)
async def cancel_spam(client: Client, message: Message):
    if not message.chat.id in spam_chats:
        return await message.edit("**ʟᴏᴏᴋs ʟɪᴋᴇ ᴛʜᴇʀᴇ's ɴᴏ ᴛᴀɢᴀʟʟ ʜᴇʀᴇ.**")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.edit("**Stop Mention.**") 
