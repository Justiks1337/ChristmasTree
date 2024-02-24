from configparser import ConfigParser as _ConfigParser
import os


class Config:
    """Get values from config"""

    __config_file = _ConfigParser()
    __config_file.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding='utf-8-sig')

    bot_token = __config_file.get('Telegram', 'bot_token')

    db_name = __config_file.get('Database', 'db_name')
    transactions_to_backup = int(__config_file.get('Database', 'transactions_to_backup'))
    yadisk_jwt = __config_file.get('Database', 'yadisk_jwt')