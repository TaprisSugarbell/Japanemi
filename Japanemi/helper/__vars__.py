from decouple import config
from .mongo_connect import Mongo, URI, confirm_ofdb, confirm


def auth_users_sync():
    _u = Mongo(URI, "Japanemi", "users")
    _c = confirm_ofdb(_u, {})
    if _c:
        return [i["user_id"] for i in _c]
    else:
        return []


async def auth_users_async():
    _u = Mongo(URI, "Japanemi", "users")
    _c = await confirm(_u, {})
    if _c:
        return [i["user_id"] for i in _c]
    else:
        return []
