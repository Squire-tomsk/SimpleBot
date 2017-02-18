## Enviroment variables

| Variable | Description |
| ------ | ------ |
|BOT_TOKEN|Telegram bot token|
|BOT_PATH|Full path to bot folder|
|MONGO_HOST|Host name of MongoDB|
|MONGO_PORT|TCP port used by MongoDB|
|MONGO_DBNAME|Database name|

## Bot data

Bot scan folder `$BOT_PATH/res/pictures` for a pictres and put them into database automatically, every time after restart.
Pictures should have `*.png` or `*.jpg` extensions. If two pictures have same name, bot will choose picture with `*.png` extension.

Text for buttons stored in standart localisation file `$BOT_PATH/res/l10n.json`. Messages `message_request` and `message_response` responsible for button text and bot answer respectively.
Button text for pictures stored in messages like `picture_request_*`. Correspondence between picture name and button text should be set in `$BOT_PATH/config.py` section `pictures` in format `'*message_name_from_l10n.json*' : 'picture_name_without_extension'`.

