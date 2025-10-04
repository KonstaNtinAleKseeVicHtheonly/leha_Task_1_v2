from aiogram import Bot, Dispatcher
from decouple import config
import logging


# Конфиги для лоадинга бота
bot = Bot(token=config('TOKEN'))
dp = Dispatcher()

# Лог - параметры
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='log_info.log', filemode='w')
logger = logging.getLogger(__name__)
