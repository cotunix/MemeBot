import json
import discord
import asyncio
import login
import youtube
from random import randint
from urllib.request import Request, urlopen
from urllib import error

client = discord.Client()


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
		await youtube.run(message.content.split(' ')[1], message.author.voice_channel,client) 
	
	elif message.content.startswith('!beyond'):
		await youtube.run('https://www.youtube.com/watch?v=8TGalu36BHA', message.author.voice_channel, client)
	
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
		if sub not in youtube.obtainedMemes:
			print('Fetching meme list')
			try:
				youtube.getMemes(sub)
			except IOError as e:
				print(str(e))
				await client.send_message(message.channel, "Error: " + str(e))
				return
		memenum = randint(0, youtube.memesize[sub] - 1)
		print(memenum)
		print(youtube.imgur[sub][memenum])
		
		await client.send_message(message.channel, youtube.imgur[sub][memenum])
	
@client.event
async def on_ready():
	#initialize globals
	global obtainedMemes
	global imgur
	global memesize
	
	
	
	print('Logged in as')
	print(client.user.name)
	print('------------')
	count = -1
		
client.run(login.email(), login.password())
