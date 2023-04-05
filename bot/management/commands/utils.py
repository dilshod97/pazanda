import importlib
from account.models import User
from bot.models import Activity
import json


def get_language(from_where):
    lan = importlib.import_module("bot.languages." + from_where).words
    return lan


def get_chat_id_by_update(update):
    return update.message.chat_id


def get_chat_id_by_message(message):
    return message.chat_id


def get_user_by_chat_id(update=None, message=None, callback=None):
    if update:
        chat_id = get_chat_id_by_update(update)
    elif message:
        chat_id = message.chat_id
    elif callback:
        chat_id = callback.message.chat_id
    user = User.objects.filter(chat_id=chat_id).first()

    return user


def get_activity(update, callback_query=False):
    if callback_query:

        chat_id = update.callback_query.message.chat_id
    else:
        chat_id = get_chat_id_by_update(update)
    activity = Activity.objects.filter(chat_id=chat_id).first()
    return activity


def update_reply_text(update, keyboard, lan, reply_text):
    reply_markup = keyboard(lan)
    reply_text = lan[reply_text]

    res = update.message.reply_text(text=reply_text, reply_markup=reply_markup)
    return res


def add_activity_type(activity, activity_type, message_id=None, res=None, language=None):
    messages = []
    chats = []
    if activity.detail:
        detail = json.loads(activity.detail)

    if res:
        messages.append(res.message_id)

    if message_id:
        messages.append(message_id)
        detail['messages'] = messages

    activity.type = activity_type
    if language:
        activity.language = language

    if activity.detail:
        activity.detail = json.dumps(detail)

    activity.save()

