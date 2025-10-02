from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
import polib
from mongo import Mongo
from pymongo.errors import OperationFailure
import nav
from tg_users_service import TelegramUserManager
from doma_names_service import DomaNamesService
from doma_name_activities_service import DomaNameActivitiesService
from doma_listings_service import DomaListingsService
from doma_offers_service import DomaOffersService
from caller_graphql import DomaGraphQLClient
from gemini_client import GeminiClient
import msg_loader


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

msg = msg_loader.load_translations()

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

try:
    db.insert('counters', {"_id": "caip10", "seq": 0})
except OperationFailure:
    # The document already exists, which is fine
    pass


@bot.on(events.NewMessage(pattern='/start', incoming=True))
@bot.on(events.CallbackQuery(data=b'main_menu'))
async def start(event):
    user_info = tum.get_user(event.sender_id)
    if not user_info:
        text = f'{msg.get('en').get("change_language_1")}:'
        buttons = nav.get_language_buttons(msg.get('en'))
        await event.respond(text, buttons=buttons)
    else:
        lang = tum.get_user(event.sender_id).get('language', 'en')
        text = f'{msg.get(lang).get("main_menu_1")}! {msg.get(lang).get("main_menu_2")}?'
        if event.sender_id in config.admin_list:
            await event.respond(text, bottons=nav.get_start_admin_buttons(msg.get(lang)))
        else:
            await event.respond(text, buttons=nav.get_start_user_buttons(msg.get(lang)))


@bot.on(events.CallbackQuery(pattern=b'about'))
async def about(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    text = f'{msg.get(lang).get("about_1")}\n\n{msg.get(lang).get("about_2")}'
    buttons = nav.get_main_menu_button(msg.get(lang))
    await event.respond(text, buttons=buttons)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'settings'))
async def settings(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    text = f'{msg.get(lang).get("change_language_1")}:'
    buttons = nav.get_language_buttons(msg.get(lang))
    buttons.append(nav.get_main_menu_button(msg.get(lang)))
    await event.respond(text, buttons=buttons)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'manage_subscription:.*'))
async def manage_subscription(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    page = int(event.data.decode().split(':')[1])
    sub_list = tum.list_subscriptions(event.sender_id)
    if sub_list:
        msg_text, buttons = nav.list_domains(msg.get(lang), sub_list,
                                   page=page,
                                   prefix='info_sub',
                                   list_prefix='manage_subscription')
        text = f'{msg.get(lang).get("manage_subscription_1")}. {msg.get(lang).get("manage_subscription_2")}.'
    else:
        text = f'{msg.get(lang).get("manage_subscription_x1")}. {msg.get(lang).get("manage_subscription_x2")}.'
        buttons = nav.get_main_menu_button(msg.get(lang))
    await event.respond(text, buttons=buttons)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'info_sub:.*'))
async def info_subscription(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    domain = event.data.decode().split(':')[1]
    text = f'{msg.get(lang).get("info_subscription_1")} `{domain}`. {msg.get(lang).get("info_subscription_2")}?'
    buttons = [nav.get_remove_subscription_button(msg.get(lang), domain),
               nav.get_main_menu_button(msg.get(lang))]
    await event.respond(text, buttons=buttons)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'remove_sub:.*'))
async def remove_subscription(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    domain = event.data.decode().split(':')[1]
    result = tum.remove_subscription(event.sender_id, domain)
    if result.modified_count > 0:
        await event.respond(f'{msg.get(lang).get("remove_subscription_1")}.', buttons=nav.get_main_menu_button(msg.get(lang)))
    else:
        await event.respond(f'{msg.get(lang).get("remove_subscription_2")}.', buttons=nav.get_main_menu_button(msg.get(lang)))
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'change_language'))
async def change_language(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    text = f'{msg.get(lang).get("change_language_1")}:'
    buttons = nav.get_language_buttons(msg.get(lang))
    await event.respond(text, buttons=buttons)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'language:.*'))
async def language(event):
    language_selected = event.data.decode().split(':')[1]
    user_info = tum.get_user(event.sender_id)
    if not user_info:
        tum.save_user(event.sender_id, language=language_selected)
    else:
        tum.update_user(event.sender_id, {'language': language_selected})
    lang = tum.get_user(event.sender_id).get('language', 'en')
    await event.respond(f'{msg.get(lang).get("change_language_2")}.', buttons=nav.get_main_menu_button(msg.get(lang)))
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'ai_consult'))
async def ai_consult(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    gc = GeminiClient(config.gemini_api_key, config.ai_model)
    dns = DomaNamesService(dgc, api_key=config.doma_api_key)
    ask_for_filter = f'{msg.get(lang).get('ai_consult_1')}. {msg.get(lang).get('ai_consult_2')}:\n`{msg.get(lang).get('ai_consult_3')}`'
    async with bot.conversation(event.sender_id, timeout=2400) as conv:
        await conv.send_message(ask_for_filter)
        response_filter = await conv.get_response()
        user_prompt = response_filter.text
        await conv.send_message(f'{msg.get(lang).get('ai_is_searching_1')}... {msg.get(lang).get('ai_is_searching_2')}.')
        keywords = gc.gen_augment_keyword(user_prompt)
        domains = []
        for word in keywords:
            try:
                domains.append(dns.get_names_by_name(name_filter=word))
            except:
                pass
        ai_domains = gc.gen_suggest_domain(user_prompt, domains)
        text, buttons = nav.list_domains(msg.get(lang), ai_domains)
        await conv.send_message(text, buttons=buttons)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'search_domain'))
async def search_domain(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    dns = DomaNamesService(dgc, api_key=config.doma_api_key)
    ask_for_filter = f'{msg.get(lang).get('enter_a_filter_string_1')}. {msg.get(lang).get('enter_a_filter_string_2')}.'
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message(ask_for_filter)
        response_filter = await conv.get_response()
        the_filter = response_filter.text
        await conv.send_message(f'{msg.get(lang).get('searching')} `{the_filter}`...')
        domains = dns.get_names_by_name(name_filter=the_filter)
        text, buttons = nav.list_domains(msg.get(lang), domains, the_filter)
        await conv.send_message(text, buttons=buttons)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'find_domains_by_owner'))
async def find_domains_by_owner(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    dns = DomaNamesService(dgc, api_key=config.doma_api_key)
    ask_for_filter = f'{msg.get(lang).get('enter_a_caip10_address_1')}. {msg.get(lang).get('enter_a_caip10_address_2')}.'
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message(ask_for_filter)
        response_filter = await conv.get_response()
        the_filter = response_filter.text
        await conv.send_message(f'{msg.get(lang).get('searching')} `{the_filter}`...')
        domains = dns.get_names_by_owner(owner_address_caip10=the_filter)
        if len(domains) > 10:
            address_exists = db.find('caip10_addresses', {'address' : the_filter})
            address_list = address_exists.to_list()
            if len(address_list) == 0:
                next_id = db.get_next_sequence_value("caip10")
                db.insert('caip10_addresses',
                          {'address': the_filter,
                                '_id': next_id})
                address_id = next_id
            else:
                address_id = str(address_list[0]['_id'])
        else:
            address_id = '0'
        text, buttons = nav.list_domains(msg.get(lang), domains, address_id, list_prefix='page_owner')
        await conv.send_message(text, buttons=buttons)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'page_domain:.*'))
async def page_domain(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    search_word = event.data.decode().split(':')[1]
    page = int(event.data.decode().split(':')[2])
    dns = DomaNamesService(dgc, api_key=config.doma_api_key)
    the_filter = search_word
    await event.respond(f'{msg.get(lang).get('searching')} `{the_filter}`...')
    domains = dns.get_names_by_name(name_filter=the_filter)
    text, buttons = nav.list_domains(msg.get(lang), domains, the_filter, page=page)
    await event.respond(text, buttons=buttons)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'page_owner:.*'))
async def page_owner(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    address_id = event.data.decode().split(':')[1]
    page = int(event.data.decode().split(':')[2])
    dns = DomaNamesService(dgc, api_key=config.doma_api_key)
    the_filter_cursor = db.find('caip10_addresses', {'_id' : int(address_id)})
    the_filter = the_filter_cursor.to_list()[0]['address']
    await event.respond(f'{msg.get(lang).get('searching')} `{the_filter}`...')
    domains = dns.get_names_by_owner(owner_address_caip10=the_filter)
    text, buttons = nav.list_domains(msg.get(lang), domains, address_id, page=page, list_prefix='page_owner')
    await event.respond(text, buttons=buttons)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'info_domain:.*'))
async def page_domain(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    domain = event.data.decode().split(':')[1]
    dns = DomaNamesService(dgc, api_key=config.doma_api_key)
    d = dns.get_name(domain)
    response_text, buttons = nav.info_domain(msg.get(lang), d)
    await event.respond(response_text, buttons=buttons)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'get_recent_listing'))
async def get_recent_listing(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    dls = DomaListingsService(dgc, api_key=config.doma_api_key)
    response_text = f'{msg.get(lang).get("last_week_domains")}:\n\n'
    text, buttons = nav.list_listings(msg.get(lang), dls, text=response_text)
    await event.respond(text, buttons=buttons)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'get_recent_offers:.*'))
async def get_recent_offers(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    name = event.data.decode().split(':')[1]
    dns = DomaNamesService(dgc, api_key=config.doma_api_key)
    name_info = dns.get_name(name)
    tokens = name_info.get('tokens', [])
    if len(tokens) > 0:
        token_id = tokens[0].get('tokenId', '')
        dos = DomaOffersService(dgc, api_key=config.doma_api_key)
        x = dos.get_offers(token_id=token_id)
        counter = 0
        response_text = f'{len(x.get('items', []))} offers so far\n\n'
        for item in x.get('items', []):
            price = int(item.get('price', 0))
            symbol = item.get('currency', {}).get('symbol', '???')
            decimals = int(item.get('currency', {}).get('decimals', '0'))
            counter += 1
            if round(price / (10 ** decimals)) > 10 ** 12:
                pretty_price = round(price / (10 ** decimals))
            else:
                pretty_price = round(price / (10 ** decimals), 4)
            response_text += f'#{counter}: {pretty_price} {symbol}\n'
        await event.respond(response_text, buttons=nav.get_main_menu_button(msg.get(lang)))
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'get_recent_activities:.*'))
async def get_recent_activities(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    name = event.data.decode().split(':')[1]
    dnas = DomaNameActivitiesService(dgc, api_key=config.doma_api_key)
    na = dnas.get_name_activities(name)
    items_list = na.get('items', [])
    response_text = f'{msg.get(lang).get("recent_activities")}:\n\n'
    for item in items_list:
        response_text += (f'{msg.get(lang).get("event")}: '
                          f'`{DomaNameActivitiesService.space_before_capitals(item.get("__typename"))}`\n'
                          f'{msg.get(lang).get("status")}: `{item.get("type")}`\n'
                          f'{msg.get(lang).get("tx_hash")}: `{item.get("txHash")}`\n'
                          f'{msg.get(lang).get("event_time")}: `{item.get("createdAt").replace("T", " ")[:-5]}`\n\n')
    await event.respond(response_text, buttons=nav.get_main_menu_button(msg.get(lang)))
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'subscribe:.*'))
async def subscribe(event):
    lang = tum.get_user(event.sender_id).get('language', 'en')
    name = event.data.decode().split(':')[1]
    sub_list = tum.list_subscriptions(event.sender_id)
    if name not in sub_list:
        tum.add_subscription(event.sender_id, name)
        await event.respond(f'{msg.get(lang).get("sub_added")}.', buttons=nav.get_main_menu_button(msg.get(lang)))
    else:
        await event.respond(f'{msg.get(lang).get("sub_already_existed")}!', buttons=nav.get_main_menu_button(msg.get(lang)))
    raise events.StopPropagation


# Connect to Telegram and run in a loop
try:
    print('bot starting...')
    bot.start(bot_token=config.tg_bot_token)
    print('bot started')
    bot.run_until_disconnected()
finally:
    db.close()
    print('bot stopped')