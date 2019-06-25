import discord
import info
import requests

async def receive_message(client, message=discord.Message):
	def command(c): return message.content.startswith('..{0}'.format(c))

	if command('ping'):
		await ping(client, message)
		return True

	if command('perish'):
		await perish(client, message)
		return True
		

async def ping(client, message):
	latency_ms = client.latency * 1000
	await message.channel.send('Pong! Time: {0} ms'.format(round(latency_ms, 2)))


async def perish(client, message):
	if message.author.id == info.get_creator_id():
		await message.channel.send(content='I die peacefully, father.', file=discord.File('../img/i_die_peacefully.jpg'))
		await client.close()
	else:
		await message.channel.send(content='You can\'t kill me, bitch.', file=discord.File('../img/then_perish.jpg'))

# ..vision (image link)
# ..vision (image)
# sends image to Google Vision API to see what Google thinks about it ;)

# ..dump (text channel)
# dumps all messages into a text file, then sends the text file
# might be wise to require server owner to approve it?

# ..quote [user]
# sends a random message from the user, or if none is provided, a random message. ignores bot commands.
# configure this with ..quote-config

# ..quote-config
# pops up a list (like FredBoat) of options.
# 1. Exclude channel - excludes a channel from the quote search
# 2. Include channel - includes a channel from the quote search
# 3. Exclude user - excludes a user from the quote search
# 4. Include user - includes a user from the quote search