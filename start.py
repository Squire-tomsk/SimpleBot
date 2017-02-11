import controller
# import cherrypy
# from server import WebhookServer
from config import SETTINGS

# be sure to pass a telegram bot token
# as an environmental variable or within
# the configuration file

if __name__ == '__main__':
    controller.init()
    if SETTINGS['reception_method']['type'] == 'polling':
        controller.bot.polling(timeout=SETTINGS['reception_method']['params']['timeout'])
        # elif SETTINGS['reception_method']['type'] == 'webhook':
        #     controller.bot.remove_webhook()
        #     controller.bot.set_webhook(url=SETTINGS['reception_method']['params']['url_base'] + SETTINGS['reception_method']['params']['url_path'],
        #             certificate=open(SETTINGS['reception_method']['params']['ssl_cert'], 'r'))
        #     cherrypy.config.update({
        #         'server.socket_host': SETTINGS['reception_method']['params']['listen'],
        #         'server.socket_port': SETTINGS['reception_method']['params']['port'],
        #         'server.ssl_module': 'builtin',
        #         'server.ssl_certificate': SETTINGS['reception_method']['params']['ssl_cert'],
        #         'server.ssl_private_key': SETTINGS['reception_method']['params']['ssl_priv']
        #     })
        #     cherrypy.quickstart(WebhookServer(controller.bot), SETTINGS['reception_method']['params']['url_path'], {'/': {}})
