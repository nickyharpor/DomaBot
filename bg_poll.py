from telethon import TelegramClient
from dotenv import load_dotenv
from mongo import Mongo
import poll_event_models as pem
from caller_poll import poll_events, acknowledge_events
import time
import polib
import os


if __name__ == '__main__':
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

    msg = {}
    for entry in polib.pofile('translations/msg_en.po'):
        msg[entry.msgid] = entry.msgstr

    db = Mongo(config.db_host, config.db_port, config.db_name)

    if config.proxy:
        bot = TelegramClient(session=config.background_name, api_id=config.api_id, api_hash=config.api_hash,
                             proxy=(config.proxy_protocol, config.proxy_host, config.proxy_port))
    else:
        bot = TelegramClient(session=config.background_name, api_id=config.api_id, api_hash=config.api_hash)

    event_collection = 'doma_events'
    users_collection = 'telegram_users'

    try:
        while True:
            try:
                response = poll_events(
                    api_key=config.doma_api_key
                )
                events = response.get("events") or []
                last_id = response.get("lastId")
                has_more = bool(response.get("hasMoreEvents"))

                if events:
                    db.insert(event_collection, events)
                    for event in events:
                        sub_users = db.find(users_collection, {'subscriptions': { "$in": [event.get("name")] }})
                        if sub_users:
                            event_data = pem.parse_event_data(event.get('type'), event.get('eventData'))
                            if event_data:
                                notification = (f'{msg.get("new_event_alert")} `{event.get("name")}`\n\n'
                                                f'{pem.dataclass_to_string(event_data)}')
                            else:
                                notification = (f'{msg.get("new_event_alert")} `{event.get("name")}`\n\n'
                                                f'{msg.get("event")}: `{event.get("type")}`')
                            for u in sub_users:
                                bot.send_message(u.get('user_id'), notification)
                    if last_id is not None:
                        acknowledge_events(api_key=config.doma_api_key,
                                           last_event_id=int(last_id))
                        print("Saved and acknowledged %d events up to id %s.", len(events), last_id)
                    if has_more:
                        continue
                else:
                    print("No new events received.")

                time.sleep(config.bg_poll_interval_seconds)
            except Exception as e:
                print("Error during polling cycle: %s", e)
                time.sleep(config.bg_poll_interval_seconds)
    except KeyboardInterrupt:
        print("Poll worker interrupted; shutting down.")
    finally:
        db.close()