import controller

# be sure to pass a telegram bot token
# as an environmental variable or within
# the configuration file

if __name__ == '__main__':
    controller.init()
    controller.bot.polling(timeout=1)
