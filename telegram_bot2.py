#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
from scrape_urls import get_lemmas_from_url, get_lemmas_from_list
from excel import write_keys_to_xlsx

list_domains = ""

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    print(message.from_user.id)
    print(message.text)
    start_menu = types.ReplyKeyboardMarkup(True)
    start_menu.row('🖊️ Составить SEO-ТЗ')
    bot.send_message(message.chat.id, 'Стартовое меню', reply_markup=start_menu)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.chat.id
    if message.text == '🖊️ Составить SEO-ТЗ':
        print(f"В разделе СОСТАВИТЬ SEO-ТЗ:")
        back_button = types.ReplyKeyboardMarkup(True, True)
        back_button.row('Назад')
        print(f"Message_chat_id: {message.chat.id} --- TEXT: {message.text}")
        bot.send_message(message.chat.id,
                         f"Пришлите мне список ключевых слов. Каждый ключ или сочетание ключей должны быть написаны с "
                         f"новой строки.",
                         reply_markup=back_button, parse_mode="HTML")
        bot.register_next_step_handler(message, get_keys_from_user)

    if message.text == 'Указать URL целевого домена':
        print(message.chat.id)
        print(message.text)
        back_button = types.ReplyKeyboardMarkup(True, True)
        back_button.row('Пропустить')
        back_button.row('Назад')
        bot.send_message(message.chat.id, f"Пришлите мне URL адрес целевого домена для которого требуется составить "
                                          f"ТЗ.\n "
                                          f"Если URL адрес отсутствует, нажмите 'Пропустить'\n",
                         reply_markup=back_button, parse_mode="HTML")
        bot.register_next_step_handler(message, get_lemma_from_my_domain)

    elif message.text == 'Указать URL конкурентов':
        print("KONKYRENTY")

    elif message.text == '❌ Удалить сайт':
        back_button = types.ReplyKeyboardMarkup(True, True)
        back_button.row('Назад')
        print(message.chat.id)
        print(message.text)
        domain_list = sql_select_domain(user_id)
        if len(domain_list) >= 1:
            bot.send_message(message.chat.id, text=
            f"Для <b>удаления</b> сайта требуется указать его <b>ID</b> из указанного ниже списка.\n"
            f"👇Ваш список отслеживаемых доменов:👇\n"
            f"{domain_list}\n"
            f"Укажите ID выбранного домена для удаления", parse_mode="HTML",
                             reply_markup=back_button)
            bot.register_next_step_handler(message, delete_site_bd)
        else:
            bot.send_message(message.chat.id, f"Ваш список отслеживаемых доменов пуст 😟\n"
                                              f"Для продолжения напишите /start и добавьте новый домен.")

    elif message.text == '🖊️ Перезаписать HASH robots':
        back_button = types.ReplyKeyboardMarkup(True, True)
        back_button.row('Назад')
        print(message.chat.id)
        print(message.text)
        domain_list = sql_select_domain(user_id)
        if len(domain_list) >= 1:
            bot.send_message(message.chat.id, f"Ваш список отслеживаемых доменов:\n{domain_list}"
                                              f"\nУкажите ID выбранного домена для перезаписи robots",
                             reply_markup=back_button)
            bot.register_next_step_handler(message, rewrite_robots_hash)
        else:
            bot.send_message(message.chat.id, f"Ваш список отслеживаемых доменов пуст 😟\n"
                                              f"Для продолжения напишите /start и добавьте новый домен.")

    if message.text == '👀 Мой профиль':
        back_button = types.ReplyKeyboardMarkup(True, True)
        back_button.row('Указать урл наш')
        back_button.row('Назад')

        bot.send_message(message.chat.id,
                         f"👮 Количество отслеживаемых доменов, шт.: {col}\n"
                         f"🕒 Средний UPTIME по всем доменам: {uptime}\n"
                         f"🌐 Ближайший освобождающийся домен: {domain_name}\n"
                         f"📅 Дата освобождения: {date_expired_domain}\n"
                         f"📅 Дней до освобождения: {difference_days}\n"
                         f"⌛ Интервал проверки доменов, минут: 10\n"
                         f"☎️Ваш номер телефона для SMS-уведомлений: {actual_telephone_user}\n",
                         reply_markup=back_button)
        # bot.register_next_step_handler(message, add_site_bd)
    elif message.text == 'Обратная связь':
        print(message.chat.id)
        print(message.text)
        back_button = types.ReplyKeyboardMarkup(True, True)
        back_button.row('Назад')
        bot.send_message(message.chat.id, f"Если у вас возник вопрос "
                                          f"или вы заметили ошибку в работе бота, отправьте нам сообщение. "
                                          f"Мы рассмотрим ваше обращение в течение 24 часов.\n"
                                          f"Формат обращения👇\n"
                                          f"<b>1️⃣ Ваше имя:</b>\n"
                                          f"<b>2️⃣ Описание ошибки или жалоба:</b>",
                         reply_markup=back_button, parse_mode="HTML")
        # bot.register_next_step_handler(message, add_site_bd)
    elif message.text == 'Добавить номер телефона (только РФ)':
        print(message.chat.id)
        print(message.text)
        back_button = types.ReplyKeyboardMarkup(True, True)
        back_button.row('Назад')
        bot.send_message(message.chat.id, f"Пришлите мне номер телефона в формате <b>7XXXXXXXXXX</b>\n"
                                          f"📱 Пример номера: <b>79647489485</b>\n"
                                          f"Требуемая длина номера: 11 символов\n"
                                          f"Номер должен начинаться с <b>7</b>\n"
                                          f"✉️ На указанный номер будут поступать SMS-уведомления о доступности сайтов.",
                         reply_markup=back_button, parse_mode="HTML")
        bot.register_next_step_handler(message, get_lemma_from_my_domain)
    elif message.text == 'Назад':
        print(message.text)
        get_text_messages(message)


def get_keys_from_user(message):
    try:
        print("Зашли в функцию: GET KEYS FROM USER")

        back_button = types.ReplyKeyboardMarkup(True, True)
        back_button.row('Указать URL целевого домена')
        back_button.row('Назад')
        user_id = message.from_user.id
        keys_from_user = message.text
        keys_from_user = str(keys_from_user).split('\n')
        bot.send_message(message.chat.id, f"Пожалуйста, ожидайте. Идет подготовка лемм.")
        lemm_list_keys_from_user = get_lemmas_from_list(keys_from_user)
        write_keys_to_xlsx(lemm_list_keys_from_user)
        print(keys_from_user)
        print(f"USER ID: {user_id} ----- KEYS: {keys_from_user}")
        bot.send_message(message.from_user.id, f"Леммы готовы. Продолжить - кнопки ниже.", reply_markup=back_button,
                         parse_mode="HTML")


    except Exception as e:
        print("ERROR: " + str(e))


def test_function(test):
    print("TERST" + str(test))


def delete_site_bd(message):
    try:
        if message.text == 'Назад':
            get_text_messages(message)
        else:
            domain_id = message.text
            user_id = message.from_user.id
            print(f"Пользователь {user_id} отправил заявку на удаление домена {domain_id} из БД")
            len_list_domain = check_domain_id_and_tg_id(domain_id, user_id)
            if int(len(len_list_domain)) >= 1:
                delete = delete_domain(domain_id, user_id)
                if delete == "Success":
                    bot.send_message(message.from_user.id, f"Домен ID {domain_id} удален из БД. Продолжить /start")
            else:
                bot.send_message(message.from_user.id, f"Указан некорректный id. Напишите /start и повторите команду")
    except ValueError:
        bot.send_message(message.from_user.id, f"Указан некорректный id. Напишите /start и повторите команду")


def rewrite_robots_hash(message):
    try:
        if message.text == 'Назад':
            get_text_messages(message)
        else:
            domain_id = message.text
            user_id = message.from_user.id
            print(f"Пользователь {user_id} отправил заявку на перезапись robots.txt для домена {domain_id}")
            len_list_domain = check_domain_id_and_tg_id(domain_id, user_id)
            len_list = len(len_list_domain)
            if len_list >= 1:
                print(len_list_domain)
                new_robots = new_robots_txt(len_list_domain, domain_id)
                if new_robots == 'Success':
                    print(f"ROBOTS.TXT для домена: {len_list_domain} успешно перезаписан.")
                    bot.send_message(message.from_user.id,
                                     f"ROBOTS.TXT для домена: {len_list_domain} успешно перезаписан.")
            else:
                bot.send_message(message.from_user.id, f"Указан некорректный id. Напишите /start и повторите команду")
    except ValueError:
        bot.send_message(message.from_user.id, f"Указан некорректный id. Напишите /start и повторите команду")


def get_lemma_from_my_domain(message):
    try:
        url_my_domain = message.text
        back_button = types.ReplyKeyboardMarkup(True, True)

        if 'http://' in url_my_domain or 'https://' in url_my_domain:
            back_button.row('Указать URL конкурентов')
            back_button.row('Назад')
            bot.send_message(message.from_user.id, f"Пожалуйста, ожидайте. Формируем таблицу лемм.")
            lemmas = get_lemmas_from_url(url_my_domain)
            print(lemmas)
            print(f"URL MY DOMAIN: {url_my_domain}")
            print(f"USER_ID: {str(message.from_user.id)} ----- {message.text}")

            bot.send_message(message.from_user.id, f"Леммы для целевого домена готовы.\n"
                                                   f"Нажмите на кнопку ниже.", reply_markup=back_button,
                             parse_mode="HTML")
        else:
            back_button.row('Назад')
            bot.send_message(message.from_user.id, f"Указан некорректный адрес. Упущен протокол. Начать сначала /start",
                             reply_markup=back_button,
                             parse_mode="HTML")
            # bot.register_next_step_handler(message, test_function)
            # bot.send_message(message.chat.id,
            #                  f"Леммы готовы. Продолжить.",
            #                  reply_markup=back_button, parse_mode="HTML")




    except ValueError:
        bot.send_message(message.from_user.id, f"Указан некорректный id. Напишите /start и повторите команду")


# Запускаем постоянный опрос бота в Телеграме
bot.polling(none_stop=True, interval=0)
#
