import json
import discord
import asyncio
import login
from random import randint
from urllib.request import Request, urlopen

global imgur
global count

client = discord.Client()

def getMemes(sub):		
	global imgur
	global obtainedMemes
	# Add subreddit to the obtainedMemes array
	obtainedMemes.append(sub)	
	imgur = {}
	imgur[sub] = []
	req = 'http://reddit.com/r/' + sub + '/top.json?sort=top&t=day&limit=50'
	q = Request(req)
	q.add_header('User-Agent', 'Meme bot by /u/TheQuillmaster')
	with urlopen(q) as response:
		html = response.read()
		j = json.loads(html.decode("utf-8"))
		if response.status == 200:
			for i in range(0,50):
				next = j['data']['children'][i]['data']['url']
				print(next)
				imgur[sub].append(next)
			asyncio.get_event_loop().call_later(43200, getMemes, sub)

@client.event
async def on_message(message):
	global obtainedMemes
	global imgur
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
		
	elif message.content.startswith('~'):
		sub = message.content[1:]
		if sub not in obtainedMemes:
			print('Fetching meme list')
			getMemes(sub)
		memenum = randint(0,49)
		print(memenum)
		print(imgur[sub][memenum])
		
		await client.send_message(message.channel, imgur[sub][memenum])
		
		
		
		

@client.event
async def on_ready():
	global obtainedMemes
	obtainedMemes = []
	print('Logged in as')
	print(client.user.name)
	print('------------')
	count = -1
	
	


	
client.run(login.email(), login.password())
