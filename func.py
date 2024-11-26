import re, os
import asyncio
import aiofiles
from loguru import logger
from colorama import Fore, Back, Style, init; init()

# программа получает текстовик
# программа проверяет его размер
# программа делит если необходимо его на части
# программа ищет ip в куске текста и если находит отправляет запрос гпт
# обрабатывает ответ

class bcolors:
    # Текстовые цвета
    BLACK = Fore.BLACK
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Fore.RESET

    # Фоновые цвета
    BG_BLACK = Back.BLACK
    BG_RED = Back.RED
    BG_GREEN = Back.GREEN
    BG_YELLOW = Back.YELLOW
    BG_BLUE = Back.BLUE
    BG_MAGENTA = Back.MAGENTA
    BG_CYAN = Back.CYAN
    BG_WHITE = Back.WHITE
    BG_RESET = Back.RESET

    # Стили текста
    BRIGHT = Style.BRIGHT
    DIM = Style.DIM
    NORMAL = Style.NORMAL
    RESET_STYLE = Style.RESET_ALL

class Helpers:

    ip_pattern = r'(\b(?:\d{1,3}\.){3}\d{1,3}\b)\s+(?i:adm\w+|root)\s+(\w+)\s+(\w+)?'

    dirr = ''

    tmpl_list = []


async def re_check(text: str, file):
    # Регулярное выражение для IP

    matches = re.finditer(Helpers.ip_pattern, text)

    if matches:
        for matc in matches:
            matc = matc.group()
            logger.success(f'FINE: {matc}')
            async with aiofiles.open('res.txt', 'a', encoding='utf8') as txt:
                await txt.write(f'\nFile: {file}\n{matc}\n{"|+|" * 50}\n')


async def file_reader(file_path, chunk_size = 4096):

    async with aiofiles.open(file_path, 'r', encoding='utf8') as f:
        # while True:
        #     chunk = await f.read(chunk_size)
        #     if not chunk: break
        #     yield chunk
        return await f.read()

async def file_handler(file_path):
    tasks = []
    async for chunk in file_reader(file_path):
        while True:
            if len(tasks) >= 30:
                tasks = [task for task in tasks if not task.done()]
                await asyncio.sleep(1)
                continue

            task = asyncio.create_task(asyncio.wait_for(re_check(chunk), 10))
            tasks.append(task)
            break



    await asyncio.gather(*tasks)



async def main():

    tasks = []
    for file in os.listdir(Helpers.dirr):
        if not file.endswith('.txt'): continue
        logger.info(bcolors.BLUE + f"{file} started" + bcolors.RESET)
        while True:
            if len(tasks) >= 1000:
                tasks = [task for task in tasks if not task.done()]
                #await asyncio.sleep(1)
                continue
            file_text = await file_reader(os.path.join(Helpers.dirr, file))
            task = asyncio.create_task(re_check(file_text, file))
            tasks.append(task)
            break

    await asyncio.gather(*tasks)


if __name__ == "__main__":

    Helpers.dirr = input("Dir: ")
    asyncio.run(main())
