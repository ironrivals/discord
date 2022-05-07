import asyncio
from discord import Member

async def getAlias(user: Member):
    alias = None
    if type(user.nick) != type(None):
        alias = user.nick
    else:
        alias = user.name
        
    await asyncio.sleep(1)
    return alias

