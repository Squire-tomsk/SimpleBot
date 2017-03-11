## Enviroment variables

| Variable | Description |
| ------ | ------ |
|BOT_TOKEN|Telegram bot token|
|BOT_PATH|Full path to bot folder|
|MONGO_HOST|Host name of MongoDB|
|MONGO_PORT|TCP port used by MongoDB|
|MONGO_DBNAME|Database name|

## Bot data

Bot scan folder `$BOT_PATH/res/pictures` for a pictures and put them into database automatically, every time after restart.
Pictures should have `*.png` or `*.jpg` extensions. If two pictures have same name, bot will choose picture with `*.png` extension.

Messages are used in the bot should be stored in `$BOT_PATH/res/messages` in `*.txt` format. If message name is same as picture name, they will connect automatically.
Documents in `*.doc` format should be stored in `$BOT_PATH/res/documents`. This way they will put to telegram servers and local database.



Text for buttons are stored in standard localisation file `$BOT_PATH/res/l10n.json`.
Correspondence between picture name and button text should be set in `$BOT_PATH/config.py` section `pictures` in format `'*message_name_from_l10n.json*' : 'picture_filename_without_extension'`.

If you want to add button to inline keyboard you should add button text in format `picture_request_*`:`button_text` to `l10n.json` where `*` will define position of button (they are sorted in accordance with this value).
Also you should add correspondence between button text and picture in `SETTINGS` dictionary, file `config.py` in format `picture_request_*` : `picture_filename_without_extension`. Files for picture and message text should exist in `res/pictures` and `res/documents` in any case.
At last step you should add to `SETTINGS['show_picture']` value `picture_request_*` : `True` if you want to show bot picture and message, and `picture_request_*` : `False` in other case.

