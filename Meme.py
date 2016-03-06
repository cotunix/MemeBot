import json
import discord
import asyncio
import login
from youtube import youtube
from random import randint
from urllib.request import Request, urlopen
from urllib import error

client = discord.Client()

def getMemes(sub):		
	# globals
	global imgur
	global obtainedMemes
	global memesize
		
	# Add subreddit to the obtainedMemes array
		
	req = 'http://reddit.com/r/' + sub + '/top.json?sort=top&t=day&limit=50'
	q = Request(req)
	q.add_header('User-Agent', 'Meme bot by /u/TheQuillmaster')
	try:		
		response = urlopen(q)
		obtainedMemes.append(sub)	
		imgur[sub] = []
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
	except error.HTTPError as e:
		raise IOError("Subreddit does not exist")
	

	

	
@client.event
async def on_server_join(server):
	await client.send_message(server.default_channel, "Hello! I'm MemeBot! Type !help to see available commands.")

@client.event
async def on_message(message):
	global obtainedMemes
	global imgur
	global memesize
	
	directerror = "This message is only permitted through direct message. Send a direct message to MemeBot to run this command!"
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
		
	elif message.content.startswith('!school'):
		await client.send_message(message.channel, 'https://www.youtube.com/watch?v=RffAHV3tcgM')
		
	elif message.content.startswith('!shitmall'):
		await client.send_message(message.channel, 'https://www.youtube.com/watch?v=5rczW1lNejw')
		
	elif message.content.startswith('!join'):
		if isinstance(message.channel, discord.PrivateChannel):
			invite = message.content.split(' ')[1]
			await client.accept_invite(invite)
		else:
			await client.send_message(message.channel, directerror)
			
	elif message.content.startswith('!yt'):
		await youtube(message.content.split(' ')[1], message.author.voice_channel) 
	
	elif message.content.startswith('!beyond'):
		await youtube('https://www.youtube.com/watch?v=8TGalu36BHA', message.author.voice_channel, client)
	
	elif message.content.startswith('!stop'):
		if client.is_voice_connected():
			print("Disconnecting")
			await client.voice.disconnect()
		else:
			print("No voice connected")
			
	
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
