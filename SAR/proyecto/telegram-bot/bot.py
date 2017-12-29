import socket
import os
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater

address = (os.getenv('SERVER_URL', 'localhost'),
                          int(os.getenv('SERVER_PORT', 2048)))

updater = Updater(token='API-KEY')
dispatcher = updater.dispatcher

def q(query, s=False, n =False):
    query += " -s" if s else ""
    query += " -n" if n else ""

    s = socket.socket()
    s.connect(address)
    s.send(bytes(query, 'utf8'))

    answer = s.recv(50)
    l = len(answer)
    while l > 0:
        aux = s.recv(2000)
        l = len(aux)
        answer += aux
    s.close()

    return answer.decode('utf8') + '\n' + query

def inline(bot, upd ate):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    titles = ['Normal query', 'Query w/o stopwords', 'Query w/ stemming',
              'Query w/ stemming & w/o stopwords']
    responses = [q(query), q(query, n=True), q(query, s=True),
                 q(query, s=True, n=True)]
    for i in range(4):
        results.append(InlineQueryResultArticle(id=i, title=titles[i],
            input_message_content=InputTextMessageContent(responses[i])))
    bot.answer_inline_query(update.inline_query.id, results)

from telegram.ext import InlineQueryHandler
dispatcher.add_handler(InlineQueryHandler(inline))

updater.start_polling()
updater.idle()

