import telebot
import chatbot_module
import json, random

ai = chatbot_module.Chatbot()
ai.train_data(json.loads(open("phrases.json", "rb").read().decode()), json.loads(open("database.json", "rb").read().decode()))

bot = telebot.TeleBot("adicione seu token aqui")

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Seja muito bem-vindo humano! Não sei o que te traz aqui, mas espero que a gente se divirta muito juntinhos! Tudo bem com você?")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    response_msg = ai.get_answer_with_return(message.text)
    print(" - Mensagem: {} // {}".format(message.text, response_msg))

    bot.reply_to(message, response_msg)


bot.infinity_polling()
