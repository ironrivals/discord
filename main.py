# load in and store environment variables from .env file
from dotenv import load_dotenv
import os
load_dotenv()
token = os.getenv('TOKEN')
secret = os.getenv('CLIENT_SECRET')
client = os.getenv('CLIENT_ID')
# import discord and reddit APIs
from discord.ext import commands
import discord
import asyncpraw
# import native packages
import utils
import time
# import custom beastmaster class
import beastmaster

# make bot instance with debug guilds set to bypass possible command registration timers
bot = discord.Bot(debug_guilds=[917445010058792973])
# make reddit instance with .env variables
reddit = asyncpraw.Reddit(
    client_id=client, 
    client_secret=secret, 
    user_agent='discord.gg:ironrivals.bot:v0.0.1')


# responds to the user with an embed of the latest Map from 'r/NemiForest'
# OR (if latest 3 Maps are depleted)
# responds to the user that all recent Maps are marked as 'depleted'.
async def get_map(ctx):
    count = 0
    # check the 3 latest posts in New in r/NemiForest
    subreddit = await reddit.subreddit('nemiforest')
    async for submission in subreddit.new(limit=3):
        count += 1
        # if the flair is None it means it is not depleted
        if submission.link_flair_text == None:
            embed = discord.Embed(title=submission.title, description='Posted by **'+str(submission.author)+'** on **r/NemiForest**')
            embed.set_image(url=submission.url)
            embed.set_footer(text='Checked on ' + time.strftime("%b %d, %Y at %H:%M:%S UTC", time.gmtime(time.time())), icon_url='')
            await ctx.respond(embed=embed)
            break
        # if the last 3 posts in New are depleted there is no active map
        if count == 3:
            await ctx.respond('Latest maps on r/NemiForest are all depleted, check back later.')

# event for when bot first logs on
@bot.event
async def on_ready():
    output_channel = bot.get_channel(963565349981286521)
    await output_channel.send(f'{bot.user} is online!')

@bot.slash_command(name='nemi', description="Gets the latest Map from 'r/NemiForest'")
async def nemi_forest_map(ctx):
    await get_map(ctx)
    
@bot.slash_command(name='beastmaster', description='Creates a new Beastmaster raid group')
async def create_bm_group(ctx, gametime: discord.Option(str)):
    raid = beastmaster.Beastmaster(gametime)
    await build_embed(ctx, raid)

async def build_embed(ctx, raid):
    embed = discord.Embed(title=f'{raid.title}', description='\u200b')
    instructions = 'Select a role from below to sign up for the raid! If the raid is full and all roles are taken you can click "Join Queue" to auto-fill in case someone else backs out of the raid.'
    team = ''
    queue = ''
    
    thumbnail = ''
    temp = 0
    
    if len(raid.roles['Base Tank']) > 0:
        host = raid.roles['Base Tank'][0]
    else:
        host = None
    
    embed.set_thumbnail(url=thumbnail)
    embed.add_field(name=f'__Host__: (Base Tank)', value=host, inline=True)
    embed.add_field(name=f'__Time__: (Gametime)', value=f'**[{raid.time} UTC]**', inline=True)
    embed.add_field(name=f'__Requirements__', value=f'{raid.requirement}', inline=True)
    embed.add_field(name=f'__Raid Team__: [{len(raid.team)}/10]', value='placeholder', inline=True)
    embed.add_field(name=f'__Queue__: [{temp}]', value='placeholder', inline=True)
    embed.add_field(name=f'__Instructions__', value=instructions, inline=False)
    embed.add_field(name=f'__Resources__', value='placeholder', inline=False)
    
    await ctx.respond(embed=embed, view=View())   
    
class View(discord.ui.View):
    @discord.ui.button(label='Base Tank')
    async def button_callback(self, button, inter):
        #set_field_at(index=3, name, value, inline) use to reset team format when method is made
        await View.role_callback(self, button, inter)
        
    @discord.ui.button(label='Pet Tank 2')
    async def button1_callback(self, button, inter):
        await View.role_callback(self, button, inter)
        
    @discord.ui.button(label='Pet Tank 1/3')
    async def button2_callback(self, button, inter):
        await View.role_callback(self, button, inter)
        
    @discord.ui.button(label='North Charger')
    async def button3_callback(self, button, inter):
        await View.role_callback(self, button, inter)
        
    @discord.ui.button(label='Backup South Charger', row=1)
    async def button4_callback(self, button, inter):
        await View.role_callback(self, button, inter)
        
    @discord.ui.button(label='DPS', row=1)
    async def button5_callback(self, button, inter):
        await View.role_callback(self, button, inter)
        
    @discord.ui.button(label='Back Out', row=1)
    async def button6_callback(self, button, inter):
        await View.backout_callback(inter)
    
    @discord.ui.button(label='Join Queue', row=1)
    async def button7_callback(self, button, inter):
        await inter.message.channel.send('workin on it, bub')
        
    async def role_callback(self, button, inter):
        title = inter.message.embeds[0].title
        raid = beastmaster.groups[title]
        alias = await utils.getAlias(inter.user)
        await raid.add_member(alias, button.label, inter)
        
    async def backout_callback(inter):
        title = inter.message.embeds[0].title
        raid = beastmaster.groups[title]
        alias = await utils.getAlias(inter.user)
        await raid.remove_member(alias, inter)
  
                    
bot.run(token)

