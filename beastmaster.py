import asyncio


groups = {}

class Beastmaster():
    def __init__(self, time):
        self.time = time
        self.title = f"Beastmaster Durzag [{self.time} UTC]"
        self.requirement = 'Sunspear or better'
        self.team = []
        self.queue = []
        self.roles = {
            'Base Tank': [],
            'Pet Tank 1/3': [],
            'Pet Tank 2': [],
            'North Charger': [],
            'Backup South Charger': [],
            'DPS': [],
            }
        self.role_maxes = {
            'Base Tank': 1,
            'Pet Tank 1/3': 1,
            'Pet Tank 2': 1,
            'North Charger': 1,
            'Backup South Charger': 1,
            'DPS': 5,
        }
        groups[self.title] = self
        pass

    def __del__(self):
        print('Object destructed.')
        pass
    
    async def add_member(self, alias, role, inter):
        if len(self.roles[role]) < self.role_maxes[role]:
            current = self.get_role(alias)
            if current == None:
                self.roles[role].append(alias)
                self.team.append(alias)
                await inter.message.channel.send(
                    content=f'Added **{alias}** to the group as __{role}__.',
                    delete_after=3
                    )
            else:
                self.roles[current].remove(alias)
                self.roles[role].append(alias)
                await inter.message.channel.send(
                    content=f'Swapped **{alias}** from __{current}__ to __{role}__.',
                    delete_after=3
                    )
                await asyncio.sleep(1)
        else:
            await inter.message.channel.send(
                content=f'__{role}__ is already filled.',
                delete_after=3
                )
            
    async def remove_member(self, alias, inter):
        if alias in self.team:
            role = self.get_role(alias)
            self.roles[role].remove(alias)
            self.team.remove(alias)
            await inter.message.channel.send(
                content=f'Removed **{alias}** from the group as __{role}__.',
                delete_after=3
                )
            pass
        else:
            await inter.message.channel.send(
                content=f'Failed to back out {alias}, not in group.',
                delete_after=3
                )
        await asyncio.sleep(1)
        
    async def join_queue(self, member):
        await asyncio.sleep(1)
        
    def check_queue(self, role):
        pass
        
    def get_role(self, alias):
        roles = self.roles
        for x in roles:
            if alias in self.roles[x]:
                return x
        