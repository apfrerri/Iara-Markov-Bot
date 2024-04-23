import re, os, time, json, random
from instagrapi import Client
from random import randint
import chatbot_module

class Bot:
    def __init__(self, username, password, data, data_markov):
        self.cl = Client()
        self.cl.login(username, password)
        print(" [!] Login feito com sucesso!")

        self.ai = chatbot_module.Chatbot()
        self.ai.train_data(data, data_markov)

    def pass_time(self, num=0):
        if not num:
            num = random.randint(30, 60)

        time.sleep(random.randint(round(num / 2), num + round(num / 2)))

    def direct_message(self, pattern="."):
        for num in range(0, 10):
            try:
                thread = self.cl.direct_threads(selected_filter = "unread")[0]
                print(" - Mensagem recebida: {}".format(thread.messages[0].text))

                if not thread.messages[0].text:
                    self.pass_time(150)
                    break

                if random.random() <= 0.03:
                    self.cl.direct_send_photo(pattern + "/" + random.choice(os.listdir(pattern)), thread_ids=[thread.id])
                    print(" [+] Imagem")
                    self.pass_time(25)
                else:
                    msg = self.ai.get_answer_with_return(thread.messages[0].text)

                    if msg:
                        self.cl.direct_send(msg, thread_ids=[thread.id])
                        print(" - Mensagem enviada! -> {} // {}".format(thread.messages[0].text, msg))
                        self.pass_time(25)
            except IndexError:
                pass

            self.pass_time(30)
        self.cl.logout()

iara = Bot("arroba do instagram", "senha do instagram", json.loads(open("phrases.json", "rb").read().decode()), json.loads(open("database.json", "rb").read().decode()))
iara.direct_message("Imagens")
