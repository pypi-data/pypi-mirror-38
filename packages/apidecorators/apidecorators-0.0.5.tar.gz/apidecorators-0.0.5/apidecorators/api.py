import os
from aiohttp import web
import jwt
import motor.motor_asyncio
from bson import ObjectId, json_util
from flatten_dict import flatten
from .hooks import _on_insert, _on_update, _on_push, _on_pull

SECRET = os.getenv("SECRET")
DB_URI = os.getenv("DB_URI")
DB = os.getenv("DB")
client = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
db = client[DB] # test

def point_reducer(k1, k2):
    if k1 is None:
        return k2
    else:
        return k1 + "." + k2

def set_cors_headers (request, response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

async def cors_factory (app, handler):
    async def cors_handler (request):
        # preflight requests
        if request.method == 'OPTIONS':
            return set_cors_headers(request, web.Response())
        else:
            response = await handler(request)
            return set_cors_headers(request, response)
    return cors_handler


def jwt_auth(f):
    async def helper(request):
        try:
            payload = jwt.decode(request.headers['Authorization'], SECRET, algorithms=['HS256'])
            return await f(request, payload)
        except Exception as e:
            return web.json_response({'error': str(e)})
    return helper

def validate(validator, update=False):
    def decorator(f):
        async def helper(col, document, request, payload):
            if validator.validate(document, update=update):
                return await f(col, document, request, payload)
            else:
                return web.json_response({'error': 'not valid document'})                 
        return helper
    return decorator

def validate_push(validator):
    def decorator(f):
        async def helper(col, document, request, payload):
            attr = request.match_info.get('push')
            if validator.validate(document):
                return await f(col, document, request, payload)
            else:
                return web.json_response({'error': 'not valid document'}) 
        return helper
    return decorator

def has_role(role):
    def decorator(f):
        async def helper(request, payload):
            document = await request.json()
            if role in payload['roles']:
                return await f(document, request, payload)
            else:
                return web.json_response({'error': 'not authorized'})
        return helper
    return decorator

def collection(col):
    def decorator(f):
        async def helper(request, payload):
            return await f(col, request, payload)
        return helper    
    return decorator

def read_access(user_permissions):
    def decorator(f):
        async def helper(col, request, payload):            
            _id = request.match_info.get('_id')
            old_doc = await db[col].find_one({'_id': ObjectId(_id)})
            
            for user, args in user_permissions.items():  
                if user == '*' or payload['user'] == old_doc[user]:
                    return await f(col, args, request, payload)
            return web.json_response({'error': 'not authorized'})
        return helper
    return decorator

def write_access(user_permissions):
    def decorator(f):
        async def helper(col, request, payload):
            document = await request.json()
            _id = request.match_info.get('_id')
            old_doc = await db[col].find_one({'_id': ObjectId(_id)})

            for user, args in user_permissions.items():     
                if user == '*' or payload['user'] == old_doc[user]:
                    if args[0] == '*':
                        return await f(col, document, request, payload)
                    ret = {}
                    for k in document.keys():
                        if k in args:
                            ret[k] = document[k]
                    return await f(col, ret, request, payload)
            return web.json_response({'error': 'not authorized'})
        return helper
    return decorator


def is_owner(f):
    async def helper(col, request, payload):
        document = await request.json()
        _id = request.match_info.get('_id')
        old_doc = await db[col].find_one({'_id': ObjectId(_id)})
        if payload['user'] == old_doc["__owner"]:
            return await f(col, document, request, payload)
        else:
            return web.json_response({'error': 'not authorized'})
    return helper

def get(f):
    async def helper(col, kw, request, payload):            
        _id = request.match_info.get('_id')
        if kw == '*':
            document = await db[col].find_one({'_id': ObjectId(_id)})
        else:
            projection = {k: 1 for k in kw}
            document = await db[col].find_one({'_id': ObjectId(_id)}, projection)
        document = await f(document)
        return web.json_response(document, dumps=json_util.dumps)
    return helper

def get_many(f):
    async def helper(col, request, payload):
        query, skip, limit = await f(request.query, payload)
        cursor = db[col].find(query).skip(skip).limit(limit)
        documents = await cursor.to_list(length=100)
        return web.json_response(documents, dumps=json_util.dumps)
    return helper

def insert(f):
    async def helper(col, document, request, payload):
        document = await f(document, request, payload)
        document['__owner'] = payload['user']   
        result = await db[col].insert_one(document)
        callback = _on_insert.get(col)
        if callback:
            callback(document)
        return web.json_response(document, dumps=json_util.dumps) 
    return helper

def update(f):
    async def helper(col, document, request, payload):
        document = await f(document, request, payload)
        document = flatten(document, reducer=point_reducer)
        _id = request.match_info.get('_id')
        await db[col].update_one({'_id': ObjectId(_id)}, {'$set': document})        
        callback = _on_update.get(col)
        if callback:
            callback(document)
        return web.json_response(document)
    return helper

def push(attr):
    def decorator(f):
        async def helper(col, document, request, payload):
            document = await f(document, request, payload)
            _id = request.match_info.get('_id')
            document['_id'] = ObjectId()
            await db[col].update_one({'_id': ObjectId(_id)}, {'$push': {attr: document}})        
            callback = _on_push.get(col)
            if callback:
                callback(document)
            return web.json_response(document, dumps=json_util.dumps)
        return helper
    return decorator

def pull(f):
    async def helper(col, document, request, payload):
        await f({}, request, payload)
        _id = request.match_info.get('_id')
        attr = request.match_info.get('pull')
        sub_id = request.match_info.get('sub_id')
        document = {'_id': ObjectId(sub_id)}
        await db[col].update_one({'_id': ObjectId(_id)}, {'$pull': {attr: document}})        
        callback = _on_pull.get(col)
        if callback:
            callback(document)
        return web.json_response({})
    return helper

def json_response(f):
    async def helper(request):
        document = await f(request)
        return web.json_response(document)
    return helper

def delete(f):
    async def helper(col, document, request, payload):
        _id = request.match_info.get('_id')
        await db[col].delete_one({'_id': ObjectId(_id)})
        return web.json_response({})
    return helper
