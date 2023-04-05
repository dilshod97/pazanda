from .log import log_errors, autorization, setLanguage
from telegram import ReplyKeyboardRemove, InputMediaPhoto
from account.models import User
from product.models import Food, Category, FoodImages
from bot.models import Activity
from .keyboards import select_category, food_menu
from .commands import start
from django.conf import settings
import importlib, json
from telegram import ParseMode

from .utils import (
        get_chat_id_by_update, get_user_by_chat_id,
        get_language, get_activity,
        add_activity_type)

@autorization
def handler(update, callback, user, activity, lan):
    chat_type = None
    if update.message:
        chat_type = update.message.chat['type']
    elif update.callback_query:
        chat_type = update.callback_query.message.chat['type']
    if chat_type == 'private':
        chat_id = update.message.chat_id
        text = update.message.text

        if activity.type == 'add-comment':
            activity.type = 'home'
            activity.save()
            create_comment(update, callback, user, activity, lan)

        elif text == lan['search_food']:
            food_search(update, callback, user, activity, lan)

        elif text == lan['category_foods']:
            select_categor(update, callback, user, activity, lan)

        elif text == lan['edit_language']:
            setLanguage(update, callback, user, activity, flag=True)

        elif text == lan['back']:
            start(update, callback)

        else:
            search(update, callback, user, activity, lan)
    # else:
    #     search_store(update, callback, user, activity, lan)


def food_search(update, callback, user, activity, lan):
    chat_id = update.message.chat_id
    text = update.message.text
    message_id = update.message.message_id
    detail = json.loads(activity.detail)
    messages = detail['messages']
    reply_text = lan['min_requirement']
    res = update.message.reply_text(text=reply_text)
    messages.append(res.message_id)
    messages.append(message_id)
    activity.type = 'drug_search'
    detail['messages'] = messages
    activity.detail = json.dumps(detail)
    activity.save()


@log_errors
def set_language(update, callback):
    chat_id = get_chat_id_by_update(update)
    message_id = update.message.message_id
    text = update.message.text
    text = text.split(' ')[1]
    activity, _ = Activity.objects.get_or_create(chat_id=chat_id)
    user = get_user_by_chat_id(update)
    languages = (('uz', 'UZ'), ('ru', 'RU'), ('en', 'EN'))
    lan = 'uz'

    for key, value in enumerate(languages):
        (lowercase, uppercase) = value
        if (uppercase == text):
            lan = lowercase
    if user:
        user.language = lan
        user.save()
        detail = json.loads(activity.detail)
        messages = detail['messages'] if 'messages' in detail else []
        messages.append(message_id)
        detail['messages'] = messages
        activity.detail = json.dumps(detail)
        activity.type = 'set_lang'
        activity.save()
    start(update, callback)


def create_comment(update, callback, user, activity, lan):
    text = update.message.text
    if not text == lan['back']:
        message_id = update.message.message_id
        reply_text = lan['comment_finish']

        reply_markup = ReplyKeyboardRemove()
        res = update.message.reply_text(text=reply_text, reply_markup=reply_markup)

        add_activity_type(activity, 'home')
        start(update, callback)


def select_categor(update, callback, user, activity, lan):
    chat_id = user.chat_id
    reply_text = lan['select_category']
    food_category = Category.objects.filter(id__in=Food.objects.all().values_list('category_id', flat=True)).distinct()
    reply_markup = select_category(lan['lang'], food_category)
    res = callback.bot.send_message(chat_id=chat_id,
                                    parse_mode=ParseMode.HTML,
                                    text=reply_text,
                                    reply_markup=reply_markup)
    activity.type = 'select_category'
    activity.save()


def search(update, callback, user, activity, lan):
    chat_id = user.chat_id
    text = update.message.text

    foods = Food.objects.filter(search_variants__icontains=text)
    if foods:
        food_id = foods.first().id
        food = Food.objects.get(id=int(food_id))
        images = FoodImages.objects.filter(notification=food)
        reply_text = food.description_uz
        if images:
            media_group = []
            for index, image in enumerate(images):
                media_group.append(InputMediaPhoto(open(settings.BASE_DIRS + image.image.url, 'rb'),
                                                   caption=reply_text if index == 0 else '', parse_mode=ParseMode.HTML))
            res = callback.bot.send_media_group(chat_id=int(chat_id), media=media_group)

        activity.type = 'result_food'
        activity.save()
    else:
        reply_text = lan['not_found_food']
        res = callback.bot.send_message(chat_id=chat_id,
                                        parse_mode=ParseMode.HTML,
                                        text=reply_text)

