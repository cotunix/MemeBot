import discord
import asyncio
import json
from urllib.request import Request, urlopen
from urllib import error
from platform import system
from random import randint
from queue import Queue

class MemeBot(discord.Client):
	def __init__(self):
		discord.Client.__init__(self)	
		self.obtainedMemes = []
		self.memesize = {}
		self.imgur = {}	
		self.vidqueue = Queue(maxsize=0)
		self.player = None
		# specify which commands we don't want to print help for
		self.nohelp = ["do", "getMemes", "help", "__module__", "__doc__"]
		self.ytdlopt = {'simulate':True}

	async def do(self, cmd, message):
		''' Function to call other functions from Meme.py '''
		await (MemeBot.__dict__)[cmd](self, message)
		
	async def join(self, message):
		''' Adds MemeBot to another server. Usage: !join <instant invite> '''
		if isinstance(message.channel, discord.PrivateChannel):
				invite = message.content.split(' ')[1]
				await self.accept_invite(invite)
		else:
			await send_message(message.channel, "This command is only available through private message.")
				
	async def yt(self, message):	
		''' Plays the audio of a given youtube URL. Usage: !yt <URL> '''
		if (message.content.split(" ")[1]).lower() == "beyond":
			vid = "https://www.youtube.com/watch?v=8TGalu36BHA"
		elif message.content.split(" ")[1].lower() == "shitmall":
			vid = "https://www.youtube.com/watch?v=5rczW1lNejw"
		elif message.content.split(" ")[1].lower() == "school":
			vid = "https://www.youtube.com/watch?v=RffAHV3tcgM"
		else:
			vid = message.content.split(" ")[1]
			if "youtu" not in vid:
				return
		# If we're running this on Windows we have to load opus.dll from the working directory
		if system == "Windows":
			if not discord.opus.is_loaded():
				discord.opus.load_opus('opus')
		if self.voice is not None and self.voice.is_connected():
			print("adding video to queue")
			self.vidqueue.put(vid)
			return
		else:
			voice = await self.join_voice_channel(message.author.voice_channel)
			if 't=' in vid:
				time = vid.split('t=')
				# -ss starts alittle late, so setting back 3 seconds to ensure it starts at that point or a little early
				if time[1].endswith('s'):
					time = int(time[1][:-1]) - 1
				else:
					time = int(time[1]) - 1
				ffmpegopt = '-ss ' + str(time)
				self.player = await voice.create_ytdl_player(vid, ytdl_options=self.ytdlopt,options=ffmpegopt)
			else:
				self.player = await self.voice.create_ytdl_player(vid, ytdl_options=self.ytdlopt)
			print('starting youtube player')
			self.player.start()
			await asyncio.sleep(self.player.duration + 5)
			if self.player.is_done() and self.voice.is_connected:
				print("ending")
				await self.next()
			else:
				print("nothing")
			

	async def stop(self, message):
		''' Immediately stops MemeBot's audio and disconnects MemeBot from the voice channel. Usage: !stop '''
		if self.is_voice_connected():
			await self.voice.disconnect()
			self.vidqueue = Queue(maxsize=0)
	
	async def next(self, message=None):
		''' Advances to the next video in the queue. Disconnects if there is none. Usage: !next '''
		if self.is_voice_connected():
			if self.vidqueue.empty():
				print("Disconnecting")
				await self.voice.disconnect()
			else:
				self.player.stop()
				print("Advancing to next song.")
				vid = self.videqueue.get()
				if 't=' in vid:
					time = vid.split('t=')
					if time[1].endswith('s'):
						time = int(time[1][:-1]) - 1
					else:
						time = int(time[1]) - 1
					ffmpegopt = '-ss ' + str(time)
					self.player = await voice.create_ytdl_player(vid, ytdl_options=self.ytdlopt,options=ffmpegopt)
				else:
					self.player = await self.voice.create_ytdl_player(vid, ytdl_options=self.ytdlopt)
				self.player.start()			
				await asyncio.sleep(self.player.duration)
				if self.player.is_done():
					await self.next()
					
		else:
			print("No voice connected")
				
	async def meme(self, message):
		''' Gets a meme from the given subreddit and posts the link in the chat. Usage: !meme <subreddit*> '''
		if len(message.content) > 5:
			sub = (message.content.split(' '))[1]
		else:
			sub = "me_irl"
		if sub not in self.obtainedMemes:
			print('Fetching meme list')
			try:
				self.getMemes(sub)
			except IOError as e:
				print(str(e))
				await self.send_message(message.channel, "Error: " + str(e))
				return
		memenum = randint(0, self.memesize[sub] - 1)
		await self.send_message(message.channel, self.imgur[sub][memenum])
		
	async def help(self, message):
		''' Obtains the help message for a given command '''
		tosend = "\n"
		if len(message.content.split(" ")) == 1:
			for func in MemeBot.__dict__:
				if func not in self.nohelp and func not in discord.Client.__dict__:
					tosend += "!" + func + "\n"		
			tosend += "\nTo learn more about a specific command, type !help <command>"			
		else:
			if (message.content.split(" ")[1].startswith("!")):
				func = (message.content.split(" ")[1])[1:]
			else:
				func = (message.content.split(" ")[1])
			try:
				tosend = func + " :" + (MemeBot.__dict__)[func].__doc__
			except(KeyError):
				tosend = "Command not recognized"
		await self.send_message(message.channel, tosend)
			
		
	def getMemes(self, sub):
		''' Helper function for meme, to obtain memes from the subreddit '''
		
		# Add subreddit to the obtainedMemes array
		req = 'http://reddit.com/r/' + sub + '/top.json?sort=top&t=day&limit=50'
		q = Request(req)
		q.add_header('User-Agent', 'Meme bot by /u/TheQuillmaster')
		try:		
			response = urlopen(q)
			self.obtainedMemes.append(sub)	
			self.imgur[sub] = []
			html = response.read()
			j = json.loads(html.decode("utf-8"))
			if response.status == 200:
				if len(j['data']['children']) == 0:
					raise IOError("Invalid subreddit")
				self.memesize[sub] = len(j['data']['children'])
				for i in range(0, self.memesize[sub]):
					next = j['data']['children'][i]['data']['url']
					print(next)
					self.imgur[sub].append(next)
				asyncio.get_event_loop().call_later(43200, self.getMemes, sub)
		except error.HTTPError as e:
			raise IOError("Subreddit does not exist")

	
				
