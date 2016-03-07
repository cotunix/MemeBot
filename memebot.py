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
		self.ytdlopt = {'simulate':True}

	async def do(self, cmd, message):
		await (MemeBot.__dict__)[cmd](self, message)
		
	async def join(self, message):
		if isinstance(message.channel, discord.PrivateChannel):
				invite = message.content.split(' ')[1]
				await self.accept_invite(invite)
		else:
			await send_message(message.channel, directerror)
				
	async def yt(self, message):	
		if message.content.split(" ")[1] == "beyond":
			vid = "https://www.youtube.com/watch?v=8TGalu36BHA"
		elif message.content.split(" ")[1] == "shitmall":
			vid = "https://www.youtube.com/watch?v=5rczW1lNejw"
		elif message.content.split(" ")[1] == "school":
			vid = "https://www.youtube.com/watch?v=RffAHV3tcgM"
		else:
			vid = message.content.split(" ")[1]
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
			self.player = await voice.create_ytdl_player(vid, ytdl_options=self.ytdlopt)
			print('starting youtube player')
			self.player.start()
			await asyncio.sleep(self.player.duration)
		while True:
			if self.vidqueue.empty() and self.player.is_done():
				await voice.disconnect()
				return
			elif self.player.is_done():
				self.player = await voice.create_ytdl_player(self.vidqueue.get(), ytdl_options=self.ytdlopt)
				self.player.start()
				await asyncio.sleep(self.player.duration)
			
		
	
	async def stop(self, message):
		if self.is_voice_connected():
			if self.vidqueue.empty():
				print("Disconnecting")
				await self.voice.disconnect()
			else:
				self.player.stop()
				print("player stopped")
				self.player = await self.voice.create_ytdl_player(self.vidqueue.get(), ytdl_options=self.ytdlopt)
				self.player.start()
			
		else:
			print("No voice connected")
				
	async def meme(self, message):
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
		
	def getMemes(self, sub):			
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

	
				