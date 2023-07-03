import asyncio
from aiohttp import web

async def endpoint_handler(request):
    return web.Response(text="Success")

app = web.Application()
app.router.add_get('/endpoint', endpoint_handler)

if __name__ == '__main__':
    web.run_app(app)
