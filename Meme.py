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
	# globals
	global imgur
	global obtainedMemes
	global memesize
	
	
	# Add subreddit to the obtainedMemes array
	obtainedMemes.append(sub)	
	imgur[sub] = []
	
	
	req = 'http://reddit.com/r/' + sub + '/top.json?sort=top&t=day&limit=50'
	q = Request(req)
	q.add_header('User-Agent', 'Meme bot by /u/TheQuillmaster')
	with urlopen(q) as response:
		html = response.read()
		j = json.loads(html.decode("utf-8"))
		if response.status == 200:
			if len(j['data']['children']) == 0:
				raise IOError("Invalid subreddit")
			memesize[sub] = len(j['data']['children'])
			for i in range(0,memesize[sub]):
				next = j['data']['children'][i]['data']['url']
				print(next)
				imgur[sub].append(next)
			asyncio.get_event_loop().call_later(43200, getMemes, sub)

@client.event
async def on_message(message):
	global obtainedMemes
	global imgur
	global memesize
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
		
	elif message.content.startswith('!meme'):
		if len(message.content) > 5:
			sub = (message.content.split(' '))[1]
		else:
			sub = "me_irl"
		if sub not in obtainedMemes:
			print('Fetching meme list')
			try:
				getMemes(sub)
			except IOError as e:
				print(str(e))
				await client.send_message(message.channel, "Error: " + str(e))
				return
		memenum = randint(0, memesize[sub] - 1)
		print(memenum)
		print(imgur[sub][memenum])
		
		await client.send_message(message.channel, imgur[sub][memenum])
		
		
		
		

@client.event
async def on_ready():
	#initialize globals
	global obtainedMemes
	global imgur
	global memesize
	
	obtainedMemes = []
	memesize = {}
	imgur = {}
	print('Logged in as')
	print(client.user.name)
	print('------------')
	count = -1
	
	


	
client.run(login.email(), login.password())
