import os
import random

from yuiChyan import CQEvent
from yuiChyan.exception import FunctionException
from yuiChyan.service import Service
from yuiChyan.util import DailyNumberLimiter

sv = Service(name='today_eat', help_cmd='吃啥帮助')

_lmt = DailyNumberLimiter(5)
img_path = os.path.join(os.path.dirname(__file__), 'foods')


@sv.on_rex(r'^(今天|[早中午晚][上饭餐午]|夜宵)吃(什么|啥|点啥)$')
async def net_ease_cloud_word(bot, ev: CQEvent):
    uid = ev.user_id
    if not _lmt.check(uid):
        raise FunctionException(ev, '你今天吃的已经够多的了！')
    match = ev['match']
    time = match.group(1).strip()
    food = random.choice(os.listdir(img_path))
    name = food.split('.')
    to_eat = f'{time}去吃{name[0]}吧~\n'
    try:
        image_path = os.path.join(img_path, food)
        to_eat += f'[CQ:image,file=file:///{image_path}]'
    except Exception as e:
        sv.logger.error(f'读取食物图片时发生错误{type(e)}')
    await bot.send(ev, to_eat, at_sender=True)
    _lmt.increase(uid)
