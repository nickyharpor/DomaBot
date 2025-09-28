from telethon import TelegramClient
import asyncio
from typing import Optional, Sequence, Union, List, Dict, Any
from pymongo import MongoClient, errors as mongo_errors
from caller_poll import poll_events, acknowledge_events
import time
import logging

__all__ = ["run_poll_worker"]

#client = TelegramClient("eventbot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def _ensure_indexes(collection) -> None:
    # Ensure idempotent upserts/inserts by unique event uniqueId
    collection.create_index("uniqueId", unique=True)


def _insert_events(collection, events: List[Dict[str, Any]], logger: logging.Logger) -> None:
    if not events:
        return
    try:
        collection.insert_many(events, ordered=False)
    except mongo_errors.BulkWriteError as bwe:
        write_errors = bwe.details.get("writeErrors", []) if bwe.details else []
        # Ignore duplicate key errors; re-raise others
        non_dup_errors = [e for e in write_errors if e.get("code") != 11000]
        if non_dup_errors:
            logger.error("Bulk insert encountered non-duplicate errors: %s", non_dup_errors)
            raise
        dup_count = len(write_errors) - len(non_dup_errors)
        if dup_count:
            logger.debug("Ignored %d duplicate events during insert.", dup_count)


def run_poll_worker(
    api_key: str,
    mongo_uri: str,
    db_name: str = "doma",
    collection_name: str = "events",
    *,
    event_types: Optional[Sequence[str]] = None,
    limit: Optional[int] = None,
    finalized_only: Optional[bool] = True,
    poll_interval_seconds: float = 2.0,
    timeout: Union[int, float] = 15,
    logger: Optional[logging.Logger] = None,
) -> None:
    """
    Continuously polls events, saves them to MongoDB, and acknowledges processed events.

    Args:
        api_key: API key for the API.
        mongo_uri: MongoDB URI, e.g. mongodb://localhost:27017
        db_name: Database name to store events.
        collection_name: Collection name to store events.
        event_types: Optional list of event type filters.
        limit: Optional max number of events per poll.
        finalized_only: If True, only finalized events are returned.
        poll_interval_seconds: Sleep interval when no events or on error.
        timeout: HTTP request timeout.
        logger: Optional logger; if None, a default logger is created.

    Behavior:
        - Inserts events as-is; ensures a unique index on 'uniqueId' to deduplicate.
        - Acknowledges with 'lastId' only after successful insert.
        - Sleeps between polls when no events, or on errors, then continues.
    """
    if logger is None:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
        logger = logging.getLogger("bg_poll")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    _ensure_indexes(collection)

    logger.info("Starting poll worker. DB=%s Collection=%s", db_name, collection_name)

    try:
        while True:
            try:
                response = poll_events(
                    api_key=api_key,
                    event_types=event_types,
                    limit=limit,
                    finalized_only=finalized_only,
                    timeout=timeout,
                )
                events = response.get("events") or []
                last_id = response.get("lastId")
                has_more = bool(response.get("hasMoreEvents"))

                if events:
                    _insert_events(collection, events, logger)
                    if last_id is not None:
                        acknowledge_events(api_key=api_key, last_event_id=int(last_id), timeout=timeout)
                        logger.info("Saved and acknowledged %d events up to id %s.", len(events), last_id)
                    # If API indicates more events may be available, loop again immediately
                    if has_more:
                        continue
                else:
                    logger.debug("No new events received.")

                time.sleep(poll_interval_seconds)
            except Exception as e:
                logger.exception("Error during polling cycle: %s", e)
                time.sleep(poll_interval_seconds)
    except KeyboardInterrupt:
        logger.info("Poll worker interrupted; shutting down.")
    finally:
        client.close()