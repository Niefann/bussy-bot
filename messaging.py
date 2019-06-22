import discord
import messaging_general

# Maisy has said 'penis' {number} times for server {server}


async def receive_message(client, message=discord.Message):
	if message.author == client.user:
		return

	if not message.content.startswith('..'):
		return

	if message.author.bot:
		return

	def command(c): return message.content.startswith('..{0}'.format(c))

	await messaging_general.receive_message(client, message)

	if command('ping'):
		latency_ms = client.latency * 1000
		await message.channel.send('Pong! Time: {0} ms'.format(round(latency_ms, 2)))

	if command('perish'):
		await message.channel.send(file=discord.File('then_perish.jpg'))
		await client.close()
