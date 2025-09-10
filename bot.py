from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
import polib
from mongo import Mongo
import nav
from tg_users_service import TelegramUserManager
from doma_listings_service import DomaListingsService
from caller_graphql import DomaGraphQLClient


# Environment detection
load_dotenv()
env = os.getenv("ENV")
if env == 'live':
    import config_live
    config = config_live
elif env == 'dev':
    import config_dev
    config = config_dev
else:
    import config_test
    config = config_test

# Load the message file
msg = {}
for entry in polib.pofile('msg_' + config.language + '.po'):
    msg[entry.msgid] = entry.msgstr

# Connect to database
db = Mongo(config.db_host, config.db_port, config.db_name)
tum = TelegramUserManager(db, 'telegram_users')
dgc = DomaGraphQLClient(api_key=config.doma_api_key)

# Initialize Telegram client
if config.proxy:
    bot = TelegramClient(session=config.session_name, api_id=config.api_id, api_hash=config.api_hash,
                         proxy=(config.proxy_protocol, config.proxy_host, config.proxy_port))
else:
    bot = TelegramClient(session=config.session_name, api_id=config.api_id, api_hash=config.api_hash)


@bot.on(events.NewMessage(pattern='/start', incoming=True))
@bot.on(events.CallbackQuery(data=b'main_menu'))
async def start(event):
    tum.save_user(event.sender_id)
    if event.sender_id in config.admin_list:
        await event.respond("test admin", bottons=nav.get_start_admin_buttons(msg))
    else:
        await event.respond("test", buttons=nav.get_start_user_buttons(msg))


@bot.on(events.CallbackQuery(pattern=b'about'))
async def about(event):
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'manage_event_subscription'))
async def manage_event_subscription(event):
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'get_recent_listing'))
async def get_recent_listing(event):
    dls = DomaListingsService(dgc, api_key=config.doma_api_key)
    await event.respond(str(dls.get_listings()))
    raise events.StopPropagation


# Connect to Telegram and run in a loop
try:
    print('bot starting...')
    bot.start(bot_token=config.tg_bot_token)
    print('bot started')
    bot.run_until_disconnected()
finally:
    print('never runs in async mode!')