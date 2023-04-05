from account.models import User
from bot.models import Activity
from .keyboards import language_menu
import json
from .utils import get_language


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Error: {e}'
            print(error_message)
            print(f)
            raise e

    return inner


def setLanguage(update, callback, user, activity, flag=False, *args, **kwargs):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    data = eval(str(update.message))
    try:
        language = user.language
        lan = get_language(language)
    except:
        try:
            default_lang_user = data['from']['language_code'] if \
                data['from']['language_code'] in ['uz', 'ru'] else 'uz'
        except:
            default_lang_user = 'uz'
        lan = get_language(default_lang_user)

    if flag:
        reply_text = lan['select_language']
    else:
        reply_text = lan['select_lang']

    detail = json.loads(activity.detail)
    messages = detail['messages'] if 'messages' in detail else []
    messages.append(message_id)
    detail['messages'] = messages
    activity.detail = json.dumps(detail)
    activity.type = 'set_lang'
    activity.save()

    reply_markup = language_menu(lan, flag)
    res = update.message.reply_text(text=reply_text, reply_markup=reply_markup)


def autorization(f):
    def inner(update, callback, *args, **kwargs):
        chat_type = None
        if update.message:
            chat_type = update.message.chat['type']
        elif update.callback_query:
            chat_type = update.callback_query.message.chat['type']

        if chat_type not in ['group', 'supergroup']:
            try:
                if hasattr(update.message, 'chat_id'):
                    chat_id = update.message.chat_id
                    message_id = update.message.message_id
                else:
                    chat_id = update.callback_query.message.chat.id
                activity, _ = Activity.objects.get_or_create(chat_id=chat_id)
                # if update.message:
                #     if update.message.text:
                #         if '/start' in update.message.text:
                #             if len(update.message.text.split()) > 1:
                #                 if not Referal.objects.filter(chat_id=chat_id):
                #                     Referal.objects.create(chat_id=chat_id, params=update.message.text.split()[1])
                if activity.detail is None:
                    activity.detail = '{}'
                    activity.save()
                user = User.objects.filter(chat_id=chat_id).first()
                if not user:
                    user = User.objects.create_user(chat_id, password=str(chat_id))
                    user.chat_id = chat_id
                    user.save()
                is_break = False
                if user.language is None:
                    is_break = True
                    setLanguage(update, callback, user, activity, *args, **kwargs)

                lan = get_language(user.language)

                if not is_break:
                    return f(update, callback, user, activity, lan, *args, **kwargs)
            except Exception as e:
                error_message = f'Error: {e}'
                print(error_message)
                print(f)
                raise
        else:
            try:
                if hasattr(update.message, 'chat_id'):
                    chat_id = int(update.message.chat_id)
                    message_id = update.message.message_id
                else:
                    chat_id = int(update.callback_query.message.chat.id)
                # if update.message:
                #     if '/start' in update.message.text:
                #         if len(update.message.text.split()) > 1:
                #             if not Referal.objects.filter(chat_id=chat_id):
                #                 Referal.objects.create(chat_id=chat_id, params=update.message.text.split()[1])
                activity, _ = Activity.objects.get_or_create(chat_id=1, type=chat_id)
                if activity.detail is None:
                    activity.detail = '{}'
                    activity.save()
                user = User.objects.filter(username=chat_id).first()
                if not user:
                    user = User.objects.create(username=chat_id, group_id=chat_id, first_name=update.message.chat['username'])
                lan = get_language('uz')
                return f(update, callback, user, activity, lan, *args, **kwargs)
            except Exception as e:
                error_message = f'Error: {e}'
                print(error_message)
                print(f)
                raise
    return inner


@log_errors
def contact(update, callback):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    activity, _ = Activity.objects.get_or_create(chat_id=chat_id)
    detail = json.loads(activity.detail)

    try:
        language = detail["language"]
        messages = detail['messages']
    except:
        messages = None
    username = update.message.from_user.username
    if not username:
        username = update.message.from_user.first_name

    user, _ = User.objects.get_or_create(
        username=username
    )

    if user.password is None:
        user.set_password(chat_id)

    # lan = 'uz'
    if language:
        lan = language.lower()

    user.chat_id = chat_id
    user.language = lan
    user.save()
    activity.type = 'contact'
    activity.detail = json.dumps({"messages": chat_id})
    activity.save()

    return user
    # res = update.message.reply_text(text=reply_text, reply_markup=reply_markup)


def clear_home(update, callback, activity):
    try:
        detail = json.loads(activity.detail)
        if "home_message" in detail:
            if hasattr(update.message, 'chat_id'):
                callback.bot.deleteMessage(chat_id=update.message.chat_id, message_id=int(detail['home_message']))
            del detail['home_message']
            activity.detail = json.dumps(detail)
            activity.save()
    except Exception as e:
        error_message = f'Error: {e}'
        print(error_message)
        print('clear_home_function')
