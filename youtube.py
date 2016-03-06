import discord
import asyncio
import platform

async def youtube(vid, channel, client):
	if platform.system == "Windows"
		if not discord.opus.is_loaded():
			discord.opus.load_opus('opus')
	ytdlopt = {'simulate':True}
	voice = await client.join_voice_channel(channel)
	player = await voice.create_ytdl_player(vid, ytdl_options=ytdlopt)
	print('starting youtube player')
	player.start()
	await asyncio.sleep(player.duration)
	await voice.disconnect()