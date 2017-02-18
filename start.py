import controller
# import cherrypy
# from server import WebhookServer
from config import SETTINGS

# be sure to pass a telegram bot token
# as an environmental variable or within
# the configuration file

if __name__ == '__main__':
    controller.init()
    controller.bot.polling(timeout=SETTINGS['reception_method']['params']['timeout'])