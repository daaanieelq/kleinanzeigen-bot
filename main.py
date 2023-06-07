import requests
from bs4 import BeautifulSoup
import telebot
import datetime
from threading import Thread
import time
TOKEN = '6067622741:AAE5siPodwHBBSNpF6LQrT7N7_KlHhJBEG0'
bot = telebot.TeleBot(TOKEN)
mainUrls = []
messages = []
chat_id = ''
with open('chat_id.txt','r') as file:
    chat_id = file.readline()
@bot.message_handler(commands = ['add','remove','list'])
def greet(message):
    command, *args = message.text.split()
    if command == '/add':
        print("Command Add")
        mainUrls.append(args[0].replace('"',''))
        #print("u = ",mainUrls)
        bot.send_message(message.chat.id,"Hinzugefügt")
    if command == '/remove':
        mainUrls.remove(args[0])
    if command == '/list':
        msg = ''
        for i in mainUrls:
            msg = msg + i + '\n'
        #print("s = ",msg)
        #print("STARTED")
        #msg = ''' Hello, how are you? '''
        if msg == '':
            bot.send_message(message.chat.id, "Liste ist leer.")
        else:
            bot.send_message(message.chat.id, msg)


def isResultsFound(url):
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://https://www.kleinanzeigen.de',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
    
    response = requests.get(url, headers=headers).content.decode('utf-8')
    soup = BeautifulSoup(response,'html.parser')
    elements = soup.find_all('article',attrs={'class':'aditem'})
    if len(elements) == 0:
        return False
    return True
def checkOne(url):
    result = isResultsFound(url)
    if result:
        message = "ETWAS WURDE GELISTET UNTER:" + "\n" + url+"\n"
        if message not in messages:
            bot.send_message(chat_id,message)
            messages.append(message)

def checkAll(urls):
    for u in urls:
        s_thread = Thread(target=checkOne,args=(u,))
        s_thread.start()

def mainThread():
    while True:
        checkAll(mainUrls)
        if len(mainUrls) != 0:
            time.sleep(180)




def main():
    s_s = Thread(target=bot.polling)
    s_s.start()
    p_thread = Thread(target=mainThread)
    p_thread.start()

if __name__ == '__main__':
    main()
