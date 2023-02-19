import aiohttp

from bot.config import settings
from bot.enums import HTTPMethodEnum


async def request(endpoint: str, method: HTTPMethodEnum, data: dict | None = None):
    url = f"{settings.BACKEND_HOST}{endpoint}"
    async with aiohttp.ClientSession(trust_env=True) as session:
        sesion_method: aiohttp.client.request = getattr(session, method.lower())
        async with sesion_method(url, data=data) as response:
            return await response.json()


async def get_random_user():
    result = await request(endpoint="/api/lunch-networking", method=HTTPMethodEnum.GET)
    body = result["body"]
    return {"img_link": body["img_link"], "fullname": body["fullname"], "theme": body["theme"]}


async def get_user_by_fullname(first_name: str, last_name: str | None):
    endpoint = f"/api/find-user?first_name={first_name}&last_name={last_name}"
    result = await request(endpoint=endpoint, method=HTTPMethodEnum.GET)
    body = result["body"]
    return body
