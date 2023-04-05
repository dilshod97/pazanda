from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import math


def home_menu(lan):
    keyboard = [
        [KeyboardButton(lan['search_food'])],
        # [KeyboardButton(lan['add_comment']), KeyboardButton(lan['edit_language'])],
        [KeyboardButton(lan['category_foods'])],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def language_menu(lan, flag):
    keyboard = [
        [KeyboardButton("🇺🇿 UZ"), KeyboardButton("🇷🇺 RU")],
        [KeyboardButton(lan['back']) if flag else '']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def back_keyboard(lan):
    keyboard = [
        [KeyboardButton(lan['back'])]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def select_category(lan, food_category):
    keyboard = []
    if lan == 'uz':
        for i in food_category:
            keyboard += [[InlineKeyboardButton(i.name_uz, callback_data='foodcategory_' + f'{i.id}')]]
    elif lan == 'ru':
        for i in food_category:
            keyboard += [[InlineKeyboardButton(i.name_ru, callback_data='foodcategory_' + f'{i.id}')]]

    reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def select_food(lan, food):
    keyboard = []
    if lan == 'uz':
        if food.count() % 2 == 0:
            for i in range(0, food.count()):
                keyboard += [[InlineKeyboardButton(food[i].name_uz, callback_data='food_' + f'{food[i].id}')],
                             [InlineKeyboardButton(food[i+1].name_uz, callback_data='food_' + f'{food[i+1].id}')]]
        else:
            for i in range(0, food.count()):
                keyboard += [[InlineKeyboardButton(food[i].name_uz, callback_data='food_' + f'{food[i].id}')]]

    elif lan == 'ru':
        if food.count() % 2 == 0:
            for i in range(0, food.count()):
                keyboard += [[InlineKeyboardButton(food[i].name_ru, callback_data='food_' + f'{food[i].id}')],
                             [InlineKeyboardButton(food[i+1].name_ru, callback_data='food_' + f'{food[i+1].id}')]]

    reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def food_menu(foods, user, lan):
    keyboard = []
    if lan == 'uz':
        keyboard += [[KeyboardButton(food.name_uz + '🥘') for food in foods]]
    else:
        keyboard += [[KeyboardButton(food.name_ru + '🥘') for food in foods]]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup