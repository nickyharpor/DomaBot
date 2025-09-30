from telethon import TelegramClient
from dotenv import load_dotenv
from mongo import Mongo
from tg_users_service import TelegramUserManager
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
    for entry in polib.pofile('msg_' + config.language + '.po'):
        msg[entry.msgid] = entry.msgstr

    db = Mongo(config.db_host, config.db_port, config.db_name)
    tum = TelegramUserManager(db, 'telegram_users')

    if config.proxy:
        bot = TelegramClient(session=config.background_name, api_id=config.api_id, api_hash=config.api_hash,
                             proxy=(config.proxy_protocol, config.proxy_host, config.proxy_port))
    else:
        bot = TelegramClient(session=config.background_name, api_id=config.api_id, api_hash=config.api_hash)

    event_collection = 'doma_events'
    poll_interval_seconds = 30

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
                    if last_id is not None:
                        acknowledge_events(api_key=config.doma_api_key,
                                           last_event_id=int(last_id))
                        print("Saved and acknowledged %d events up to id %s.", len(events), last_id)
                    if has_more:
                        continue
                else:
                    print("No new events received.")

                time.sleep(poll_interval_seconds)
            except Exception as e:
                print("Error during polling cycle: %s", e)
                time.sleep(poll_interval_seconds)
    except KeyboardInterrupt:
        print("Poll worker interrupted; shutting down.")
    finally:
        db.close()