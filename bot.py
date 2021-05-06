import logging
from typing import Dict
import datetime
import requests


from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['Age', 'Postal Code'],
    ['Something else...'],
    ['Done'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

'''
MAIN FUNCTION
def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = list()

    for key, value in user_data.items():
        facts.append(f'{key} - {value}')

    return "\n".join(facts).join(['\n', '\n'])
 '''
 
 ## EDITED ##
def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = list()

    #for key, value in user_data.items():
    #    facts.append(f'{key} - {value}')

    return user_data
####


def cowin(user_data: Dict[str, str]) -> str:
    final_list = []
    base = datetime.datetime.today()
    date_list = [base + datetime.timedelta(days=x) for x in range(7)]
    date_str = [x.strftime("%d-%m-%Y") for x in date_list]
    age = int(user_data['Age']) 
    #numdays = user_data['Days ahead']
    POST_CODE = int(user_data['Postal Code'])
    print_flag = 'Y'
    for INP_DATE in date_str:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(POST_CODE, INP_DATE)
        response = requests.get(URL)
        if response.ok:
            resp_json = response.json()
            #print(json.dumps(resp_json, indent = 1))
            flag = False
            if resp_json["centers"]:
                #print("As of: {}".format(INP_DATE))
                if(print_flag=='y' or print_flag=='Y'):
                    for center in resp_json["centers"]:
                        for session in center["sessions"]:
                            if session["min_age_limit"] <= age:
                                #print("\t", center["name"])
                                #print("\t", center["block_name"])
                                #print("\t Price: ", center["fee_type"])
                                #print("\t Available Capacity: ", session["available_capacity"])
                                put = {center["name"]:session["available_capacity"]}
                                final_list.append(put)
                                if(session["vaccine"] != ''):
                                    a = 1
                                    #print("\t Vaccine: ", session["vaccine"])
                                #print("\n\n")       
            else:
                nope = str("No available slots on: ")
                inp_date = str(INP_DATE)
                nope_app = nope + inp_date
                final_list.append(nope_app)
    #final_list = list(set(final_list))
    return final_list
    
    
    

def start(update: Update, _: CallbackContext) -> int:
    
    update.message.reply_text(
        "Hi! My name is COWIN Bot, I will show all the vaccination centers corresponding to the postal code you mention. "
        "Let's start, shall we?",
        reply_markup=markup,
    )

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Enter your {text.lower()}')

    return TYPING_REPLY


def custom_choice(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        'Alright, please send me the category first, for example "Age"'
    )

    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text(
        "Neat!  Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)} You can change the data that you have entered."
        " To do this click the button called *Something else...*",
        reply_markup=markup,
    )

    return CHOOSING


def done(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    base = datetime.datetime.today()
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"Here are all vaccination centers and vaccine count corresponding to the postal code you mentioned: {cowin(user_data)}"
        "Ignore the repeated values, since person who coded me isn't a pro!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Age|Postal Code)$'), regular_choice
                ),
                MessageHandler(Filters.regex('^Something else...$'), custom_choice),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()