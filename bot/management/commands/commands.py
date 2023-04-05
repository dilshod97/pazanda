from .log import autorization, clear_home
from .keyboards import home_menu
import json
from account.models import User


@autorization
def start(update, callback, user, activity, lan):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    clear_home(update, callback, activity)
    activity.type = 'home'
    reply_markup = home_menu(lan)
    reply_text = lan['start_msg']

    res = update.message.reply_text(text=reply_text, reply_markup=reply_markup)
    detail = json.loads(activity.detail)
    messages = []
    messages.append(message_id)
    detail['home_message'] = res.message_id
    detail['messages'] = messages
    activity.detail = json.dumps(detail)
    activity.save()


