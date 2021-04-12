import dingtalkchatbot.chatbot as cb
import config

def send_ding(text, msg):
    ding = cb.DingtalkChatbot(config.webhook, secret=config.secret)
    ding.send_text(msg='{}\r\n{}'.format(text, msg), is_at_all=False)