import aiohttp

from bot.config import settings
from bot.enums import HTTPMethodEnum


async def request(endpoint: str, method: HTTPMethodEnum, data: dict | None):
    url = f"{settings.BACKEND_HOST}{endpoint}"
    async with aiohttp.ClientSession() as session:
        sesion_method: aiohttp.client.request = getattr(session, method.lower())
        async with sesion_method(url, data=data) as response:
            return await response.json()


async def get_random_user():
    result = await request(endpoint="/api/lunch-networking")
    return {
        "img_link": "https://storage.yandexcloud.net/onboarding/2d03ffa416e349468c35b07aa03c137d.png",
        "fullname": "Оксана Хохлышева",
    }
