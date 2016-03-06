import discord
import asyncio
import platform
from urllib.request import Request, urlopen
from urllib import error
import json

obtainedMemes = []
memesize = {}
imgur = {}


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

async def run(vid, channel, client):
	if platform.system == "Windows":
		if not discord.opus.is_loaded():
			discord.opus.load_opus('opus')
	ytdlopt = {'simulate':True}
	voice = await client.join_voice_channel(channel)
	player = await voice.create_ytdl_player(vid, ytdl_options=ytdlopt)
	print('starting youtube player')
	player.start()
	await asyncio.sleep(player.duration)
	await voice.disconnect()
