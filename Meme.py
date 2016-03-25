import discord
import asyncio
import login
from memebot import MemeBot

'''This script handles catching all of the events that discord gives us and any non command logic.
The logic revolving the events handled in commands can be found in memebot.py'''

client = MemeBot()


@client.event
async def on_server_join(server):
	await client.send_message(server.default_channel, "Hello! I'm MemeBot! Type !help to see available commands.")

@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
	if message.author == "sharamall":
		return
	if message.author == "Micro":
		return
		
	elif message.content.startswith("!"):
		await client.do((message.content.split()[0][1:]).lower(), message)
	
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print('------------')
	
		
client.run(login.email(), login.password())
