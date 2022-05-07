import asyncio
from types import NoneType
from discord import Member

async def getAlias(user: Member):
    alias = None
    if type(user.nick) != NoneType:
        alias = user.nick
    else:
        alias = user.name
        
    await asyncio.sleep(1)
    return alias

