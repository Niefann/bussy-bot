import discord
import info
import datetime
import requests


async def receive_message(client, message=discord.Message):
	def command(c): return message.content.startswith('..{0}'.format(c))

	if command('infinite'):
		await infinite(message)

	if command('history'):
		await history(message)

	if command('invite'):
		await invite(message)

	if command('help'):
		await help(message)

	if command('wiki'):
		await wiki(message)

async def help(message):
	mes = '``` General\n\n•My command prefix is \'..\'\n•..help: displays help message\n•..infinite: prints out the lyrics to the best song ever\n•..history [user] [phrase]: search the server for the number of times someone has said something. WARNING: this will take a _long_ time```'
	await message.channel.send(mes)


async def infinite(message):
	f = open('infinite.txt', 'r')
	mes = "".join([line for line in f.readlines()])
	await message.channel.send(mes)


async def invite(message):
	invite_url = info.get_invite_url()
	await message.channel.send('Thanks for asking! You can invite me here:\n{0}'.format(invite_url))


async def wiki(message):
	link = 'https://bussybopperslore.fandom.com/wiki/'
	parts = message.content.split()

	parts.reverse()
	parts.pop()
	parts.reverse()
	attempted_suffix = '_'.join(parts)
	suffix = 'Bussy_Boppers_Wiki'
	if len(parts) > 0:
		r = requests.get(link + attempted_suffix)
		if r.status_code == 200:
			suffix = attempted_suffix
	
	await message.channel.send('Add it to the wiki!\n' + link + suffix)


async def history(message):
	# ..history @Burst54
	parts = message.content.split()
	if len(parts) < 3:
		await message.channel.send('Command must be in the format: `..history [user] [phrase]`')
		return

	copy = parts.copy()
	copy.reverse()
	copy.pop()
	copy.pop()
	copy.reverse()
	phrase = ' '.join(copy)

	await message.channel.send('Hang on while I take a look around the server!')
	start = datetime.datetime.now()
	who = discord.utils.find(
		lambda u: u.mention == parts[1], message.guild.members)
	
	# TODO: replace message that says "hang on"
	frequency = 0
	print('Searching for phrase \"{0}\"'.format(phrase))
	for channel in message.guild.text_channels:
		print('Searching channel \"{0}\"'.format(channel.name))
		async for mes in channel.history(limit=None):
			if mes.author is not who:
				continue
			if phrase.lower() in mes.content.lower() and mes is not message:
				print(mes.content)
				frequency += 1
	timespan = datetime.datetime.now() - start
	print('Took {0}.'.format(timespan))
	await message.channel.send('{0} used the phrase \"{1}\" {2} times!'.format(who.mention, phrase, frequency))
