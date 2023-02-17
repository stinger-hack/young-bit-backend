import aiohttp

from bot.config import settings
from bot.enums import HTTPMethodEnum


async def request(endpoint: str, method: HTTPMethodEnum, data: dict | None):
    url = f"{settings.BACKEND_HOST}{endpoint}"
    async with aiohttp.ClientSession() as session:
        sesion_method: aiohttp.client.request = getattr(session, method.lower())
        async with sesion_method(url, data=data) as response:
            return await response.json()
