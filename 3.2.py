from cerberus import Validator
from aiohttp import web

async def endpoint_handler(request):
    schema = {
        'name': {'type': 'string', 'required': True},
        'age': {'type': 'integer', 'min': 18, 'max': 99}
    }

    data = await request.json()
    validator = Validator(schema)
    if not validator.validate(data):
        return web.json_response({'error': 'Invalid data'}, status=400)


    return web.json_response({'message': 'Success'})

app = web.Application()
app.router.add_post('/endpoint', endpoint_handler)


