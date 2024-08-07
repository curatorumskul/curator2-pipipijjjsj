import telebot
import random

TOKEN = '7408781473:AAFk7LLxvb4ICmoUMa7UeI6e2iCTNoevFv0'
bot = telebot.TeleBot(token=TOKEN, parse_mode=None)
gl_status = None  # current game


def create_markup():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    buttons = [
        telebot.types.InlineKeyboardButton(text='rock, paper and sciccors', callback_data='rock_paper_sciccors'),
        telebot.types.InlineKeyboardButton(text='echo', callback_data='echo_bot'),
        telebot.types.InlineKeyboardButton(text='conversation', callback_data='conversation'),
        telebot.types.InlineKeyboardButton(text='suggest nickname', callback_data='suggest_nickname')
    ]

    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['start'])
def start_games(message):
    global gl_status
    gl_status = None  # reset current game
    bot.send_message(message.chat.id, text='Choose the game:', reply_markup=create_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global gl_status
    cd = call.data  # set current game
    gl_status = cd
    try:
        if cd == 'rock_paper_sciccors':
            bot.send_message(call.message.chat.id, text='*__Let\'s play rock, paper and sciccors\\.__*',
                             parse_mode='MarkDownV2')
        elif cd == 'echo_bot':
            bot.send_message(call.message.chat.id,
                             text='*Whatever you say \\- I\'ll say it\\. Say stop to stop lol\\.*',
                             parse_mode='MarkDownV2')
        elif cd == 'conversation':
            bot.send_message(call.message.chat.id, text='*_Let\'s have a conversation\\. Say stop to stop lol\\._*',
                             parse_mode='MarkDownV2')
        elif cd == 'suggest_nickname':
            bot.send_message(call.message.chat.id, text='Go ahead and suggest a name\\.', parse_mode='MarkDownV2')
    except Exception as e:
        print(repr(e))


@bot.message_handler(func=lambda message: True)
def current_message_handler(message):
    global gl_status
    if gl_status == 'rock_paper_sciccors':
        play_rps(message)
    elif gl_status == 'echo_bot':
        echo_bot(message)
    elif gl_status == 'conversation':
        conversation(message)
    elif gl_status == 'suggest_nickname':
        suggestion(message)
    else:
        bot.send_message(message.chat.id, text='Please, choose the game.')


def play_rps(message):
    user_choice = message.text.lower()
    if user_choice not in (['rock', 'paper', 'sciccors']):
        bot.send_message(message.chat.id, text='Please, choose rock, paper, or sciccors.')
        return

    bot_choice = random.choice(['rock', 'paper', 'sciccors'])
    result = determine_winner(bot_choice, user_choice)
    bot.send_message(message.chat.id, text=f'You chose: {user_choice}. I chose: {bot_choice}. {result}')


def determine_winner(bot_choice, user_choice):
    if bot_choice == user_choice:
        return 'Draw'
    elif (bot_choice == 'rock' and user_choice == 'sciccors') or \
            (bot_choice == 'sciccors' and user_choice == 'paper') or \
            (bot_choice == 'paper' and user_choice == 'rock'):
        return 'I win!'
    else:
        return 'You win! Congratulations!'


def echo_bot(message):
    global gl_status
    if message.text.lower() == 'stop':
        gl_status = None
        bot.send_message(message.chat.id, text='The game was stopped.')
        return

    bot.send_message(message.chat.id, text=message.text)


def conversation(message):
    global gl_status
    user_name = message.from_user.first_name
    if message.text.lower() == 'stop':
        gl_status = None
        bot.send_message(message.chat.id, text='The conversation is over.')
        return

    bot.send_message(message.chat.id, text=f'Hello *{user_name}*\\. Let\'s have a conversation\\. Bla bla bla bla\\.',
                     parse_mode='MarkDownV2')


def suggestion(message):
    global gl_status
    name = message.text.lower()
    if name == 'stop':
        gl_status = None
        return
    elif is_valid_name(name):
        bot.send_message(message.chat.id, text=f'Good nickname: {name}')
    else:
        bot.send_message(message.chat.id, text=f'Bad nickname: {name}')


def is_valid_name(name):
    return (len(name) <= 20 and name.endswith('bot') and name[0].isdigit() == False)


bot.infinity_polling()