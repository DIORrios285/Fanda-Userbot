from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import CMD_HELP, bot, CMD_HANDLER as cmd
from userbot.utils import edit_or_reply, edit_delete, fanda_cmd


@fanda_cmd(pattern="(?:dgrup|dg)\\s?(.*)?")
async def _(event):
    if event.fwd_from:
        return
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id:
        await edit_delete(event, "```Mohon Balas Ke Pesan Pengguna atau ketik .dgrup (ID/Username) Yang mau Anda deteksi```")
        return
    if input_str:
        try:
            uid = int(input_str)
        except ValueError:
            try:
                u = await event.client.get_entity(input_str)
            except ValueError:
                await edit_delete(event, "`Mohon Berikan ID/Username untuk menemukan Riwayat`"
                                  )
            uid = u.id
    else:
        uid = reply_message.sender_id
    chat = "@tgscanrobot"
    xx = await edit_or_reply(event, "`Sedang Mendeteksi...`")
    async with bot.conversation(chat) as conv:
        try:
            await conv.send_message(f"{uid}")
        except YouBlockedUserError:
            await steal.reply(
                "```Mohon Unblock @tgscanrobot Dan Coba Lagi```"
            )
        response = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        await xx.edit(response.text)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    return " ".join(names)


CMD_HELP.update({
    "deteksi":
        f"`{cmd}dgrup` ; `{cmd}dg`\
    \nPenjelasan: Melihat Riwayat Grup Yang Pernah / Sedang dimasuki."
})
