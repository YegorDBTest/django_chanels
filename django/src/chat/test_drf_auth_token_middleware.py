import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization': 'Token c02869d077505a2e42dcf16cd91276a8c930dc90',
        }
        async with session.ws_connect('ws://nginx/ws/chat/test/', headers=headers) as ws:
            await ws.send_str('{"message": "test"}')
            await ws.close()


if __name__ == '__main__':
    asyncio.run(main())
