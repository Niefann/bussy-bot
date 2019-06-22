import discord
import requests

async def receive_message(client, message=discord.Message):
	def command(c): return message.content.startswith('..{0}'.format(c))

	if command('ping'):
		ping(client, message)

	if command('perish'):
		perish(client, message)
		

async def ping(client, message):
	latency_ms = client.latency * 1000
	await message.channel.send('Pong! Time: {0} ms'.format(round(latency_ms, 2)))

async def perish(client, message):
	await message.channel.send(file=discord.File('../img/then_perish.jpg'))
	await client.close()

# ..vision (image link)
# ..vision (image)
# sends image to Google Vision API to see what Google thinks about it ;)

# ..dump (text channel)
# dumps all messages into a text file, then sends the text file
# might be wise to require server owner to approve it?
