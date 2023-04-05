from .log import autorization
from product.models import Food, FoodImages
from .keyboards import select_food
from telegram import ParseMode, InputMediaPhoto
from django.conf import settings

@autorization
def callback_query(update, callback, user, activity, lan):
    query = update.callback_query
    query.answer()

    if 'foodcategory_' in query.data:
        category_id = query.data.split('_')[1]
        result_category(update, callback, user, activity, lan, category_id)
    elif 'food_' in query.data:
        food_id = query.data.split('_')[1]
        result_food(update, callback, user, activity, lan, food_id)
    # elif 'prevresultt_' in query.data:
    #     result_page_near(update, drug, callback, user, activity, lan)
    # elif 'nextresultt_' in query.data:
    #     result_page_near(update,drug, callback, user, activity, lan)
    # elif 'searchnear_' in query.data:
    #     search_near(update,drug, callback, user, activity, lan)
    # elif 'searchcheap_' in query.data:
    #     searchcheap(update,drug, callback, user, activity, lan)


def result_category(update, callback, user, activity, lan, category_id):
    chat_id = user.chat_id
    food = Food.objects.filter(category_id=int(category_id))
    reply_text = lan['select_food']
    reply_markup = select_food(lan['lang'], food)
    res = callback.bot.send_message(chat_id=chat_id,
                                    parse_mode=ParseMode.HTML,
                                    text=reply_text,
                                    reply_markup=reply_markup)
    activity.type = 'select_food'
    activity.save()


def result_food(update, callback, user, activity, lan, food_id):
    chat_id = user.chat_id
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