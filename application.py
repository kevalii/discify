import requests
import requests.auth
from dotenv import load_dotenv
import os
import discord
import asyncio
from spotify_searcher import search_helper

client = discord.Client()

load_dotenv()
DISC_TOKEN=os.getenv('DISC_TOKEN')

### DISCORD ###

# Validates query input
def validate(q, limit):
	try:
		q = int(q)

		if q > limit:
			return False
		return q
	except:
		return False

@client.event
async def on_message(message):
	# Ensures the bot does not respond to itself
	if message.author == client.user:
		return

	if message.content.startswith('$join'):
		if message.author.voice.voice_channel is None:
			await client.send_message(message.channel, '**You are not connected to a voice channel!**')
		else:
			await client.join_voice_channel(message.author.voice.voice_channel)
	elif message.content.startswith('$search '):
		await search_playlists(message)
 
async def search_playlists(message):
	# User query
	q = message.content.split(' ', 1)[1]

	# Display results
	results = list(enumerate(search_helper(q), 1))
	msg = f"**Results for {q}**"
	for count, result in results:
		msg += f"\n`{count}.` {result['name']} by {result['owner']['display_name']}"
	# Catch in the case where there are no results
	try:
		lim = count
	except UnboundLocalError:
		await client.send_message(message.channel, "**No results found**")
		return
	await client.send_message(message.channel, msg)

	# Follow-up
	await client.send_message(message.channel, "**Please choose or preview a playlist (e.g. '$choose 1' or '$preview 1').**")
	message = await client.wait_for_message(author=message.author)
	q = message.content.split(' ', 1)[1]

	# Query Validation; three attempts allowed
	count = 0
	while not validate(q, lim) and count < 3:
		count += 1
		await client.send_message(message.channel, f"Invalid input. Please try again. Attempt {count} out of 3")
		message = await client.wait_for_message(author=message.author)
		if not count <= 3:
			await client.send_message(message.channel, '**Resetting**')
			return
		q = message.content.split(' ', 1)[1]

	# Further follow-up
	q = int(q) - 1 if int(q) - 1 < 0 else 0
	playlist = results[int(q)][1]['external_urls']['spotify']

	# We process the query before the command is parsed to simplify things
	while(message.content.startswith('$preview ')):
		await client.send_message(message.channel, f"{playlist}")
		message = await client.wait_for_message(author=message.author)

	if message.content.startswith('$choose '):
		await client.send_message(message.channel, f"**Copy and paste the command below**\n\n`-play {playlist}`")

# Leave if channel is empty or if a user is AFK
@client.event
async def on_voice_state_update(before, after):
	if after.voice.is_afk or after.voice.voice_channel is None:
		for x in client.voice_clients:
			if x.channel == before.voice.voice_channel and len(before.voice.voice_channel.voice_members) == 1:
				await x.disconnect()
				break

@client.event
async def on_ready():
	print(f"Successfully logged in as {client.user.name}#{client.user.id}")

client.run(DISC_TOKEN)
