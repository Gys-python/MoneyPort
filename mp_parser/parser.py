from telethon import TelegramClient, events
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel
from settings.settings import *
from database.models import QuestionMessage, AnswerMessage, db, LastParsed
from logger import logger
import aioschedule as schedule
import asyncio
import re


client = TelegramClient(PHONE, API_ID, API_HASH, system_version=SYSTEM_VERSION)


def contains_question_outside_link(text):
    logger.info("Function ~ contains_question_outside_link")
    text_without_links = re.sub(r'\[(.*?)\]\(tg://user\?id=\d+\)', '', text)
    return "?" in text_without_links


async def get_last_parsed_id():
    logger.info("Function ~ get_last_parsed_id")
    last_parsed, created = LastParsed.get_or_create(id=1)
    return last_parsed.last_parsed_id


async def update_last_parsed_id(message_id):
    logger.info("Function ~ update_last_parsed_id")
    try:
        last_parsed, created = LastParsed.get_or_create(id=1)
        last_parsed.last_parsed_id = message_id
        last_parsed.save()
        logger.info(f"Last parsed ID updated to: {message_id}")
    except Exception as e:
        logger.error(f"Error updating last parsed ID: {e}")


async def parse_history(client):
    logger.info("Function ~ parse_history")
    last_parsed_id = await get_last_parsed_id()
    channel_entity = await client.get_entity(PeerChannel(int(CHANNEL_ID)))
    async for message in client.iter_messages(channel_entity, offset_id=last_parsed_id):
        await handle_message(message)
        await update_last_parsed_id(message.id)


async def handle_message(event):
    logger.info('Function ~ handle_message')
    try:
        is_question_text = contains_question_outside_link(event.text) if event.text else False
        reply_to_msg_id = event.reply_to.reply_to_msg_id if event.reply_to else None

        user = await event.get_sender()
        username, first_name, last_name = (user.username if user.username else "",
                                           user.first_name if user.first_name else "",
                                           user.last_name if user.last_name else "") if user else ("", "", "")

        question = None
        if is_question_text:
            question = QuestionMessage.create(
                message_id=event.id, date=event.date, user_id=event.sender_id,
                username=username, first_name=first_name, last_name=last_name, text=event.text
            )
            logger.info(f"Question saved: {event.id}")
            pending_answers = AnswerMessage.update({AnswerMessage.question_id: question.id}).where(
                AnswerMessage.reply_to_msg_id == event.id)
            pending_answers.execute()
        if reply_to_msg_id:
            question = QuestionMessage.get_or_none(message_id=reply_to_msg_id)

            AnswerMessage.create(
                message_id=event.id, date=event.date, user_id=event.sender_id, username=username, first_name=first_name,
                last_name=last_name, text=event.text, question_id=question.id if question else None,  # Установите question_id, если вопрос найден
                reply_to_msg_id=reply_to_msg_id
            )
            logger.info(f"Answer saved: {event.id} (reply to {reply_to_msg_id})")

        elif not is_question_text:
            logger.info(f"Message skipped: {event.id} - not a question or answer.")
    except Exception as e:
        logger.error(f"Error handling message: {e}")


async def message_handler(event):
    logger.info('Function ~ message_handler')
    logger.info(event)
    await handle_message(event)


async def periodic_task(interval, coro):
    logger.info("Function ~ periodic_task")
    while True:
        await asyncio.create_task(coro())
        await asyncio.sleep(interval)


async def update_question_links():
    logger.info("Function ~ update_question_links")
    unanswered_messages = AnswerMessage.select().where(AnswerMessage.question_id.is_null())
    for answer in unanswered_messages:
        question = QuestionMessage.get_or_none(message_id=answer.reply_to_msg_id)
        if question:
            answer.question_id = question.id
            answer.save()
            logger.info(f"Updated AnswerMessage {answer.id}: set question_id to {question.id}")


async def scheduler():
    logger.info("Function ~ scheduler")
    schedule.every(1).minutes.do(update_question_links)

    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)


async def run():
    logger.info("Function ~ run")
    await client.start()
    logger.info("Client started. Parsing history...")
    await parse_history(client)
    logger.info("History parsed. Running scheduler...")
    client.add_event_handler(message_handler, events.NewMessage(chats=[int(CHANNEL_ID)]))
    await asyncio.create_task(periodic_task(600, update_question_links))
    logger.info("Scheduler started. Running client...")
    await client.run_until_disconnected()
    logger.info("Client disconnected.")


