import json
import discord
import asyncio
import login
from urllib.request import Request, urlopen

global imgur
global count

client = discord.Client()

def getMemes():		
	global imgur	
	imgur = []	
	q = Request('http://reddit.com/r/meirl/hot.json?limit=10')
	q.add_header('User-Agent', 'Meme bot by /u/TheQuillmaster')
	with urlopen(q) as response:
		html = response.read()
		j = json.loads(html.decode("utf-8"))
		if response.status == 200:
			for i in range(0,10):
				next = j['data']['children'][i]['data']['url']
				print(next)
				imgur.append(next)

@client.event
async def on_message(message):
	global count
	global imgur
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
		
	elif message.content.startswith('!meme'):
		print(count)
		print(imgur[count])
		count = count + 1
		if count == 10:
			getMemes()
			count = 0
		await client.send_message(message.channel, imgur[count])
		
		
		
		

@client.event
async def on_ready():
	global count
	print('Logged in as')
	print(client.user.name)
	print('------------')
	count = -1
	getMemes()
	


	
client.run(login.email(), login.password())
