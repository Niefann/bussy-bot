import discord
import info
import datetime
import requests
import re


async def receive_message(client, message=discord.Message):
	def command(c): return message.content.startswith('..{0}'.format(c))

	if command('infinite'):
		await infinite(message)
		return True

	if command('history'):
		await history(message)
		return True

	if command('invite'):
		await invite(message)
		return True

	if command('help'):
		await help(message)
		return True

	if command('wiki'):
		await wiki(message)
		return True


async def help(message):
	f = open('../txt/help.txt', 'r')
	mes = ''.join(f.readlines())
	await message.channel.send(mes)


async def infinite(message):
	f = open('../txt/infinite.txt', 'r')
	mes = "".join([line for line in f.readlines()])
	await message.channel.send(mes)


async def invite(message):
	# invite_url = info.get_invite_url()
	# await message.channel.send('Thanks for asking! You can invite me here:\n{0}'.format(invite_url))
	await message.channel.send('(disabled)')


async def wiki(message):
	link = 'https://bussybopperslore.fandom.com/wiki/'
	parts = message.content.split()

	parts = parts[1:]
	parts = list(map(lambda a : a.capitalize(), parts))
	attempted_suffix = '_'.join(parts)
	suffix = 'Bussy_Boppers_Wiki'
	if len(parts) > 0:
		r = requests.get(link + attempted_suffix)
		if r.status_code == 200:
			suffix = attempted_suffix
	
	await message.channel.send('Add it to the wiki!\n' + link + suffix)


async def history(message):
	parts = message.content.split()
	if len(parts) < 3:
		await message.channel.send('Command must be in the format: `..history [user] [phrase]`')
		return

	phrase = ' '.join(parts[2:])

	sent_message = await message.channel.send('Hang on while I take a look around the server!')
	start = datetime.datetime.now()
	if '!' not in parts[1]:
		print('no \"!\" in mention. adding it now.')
		split_mention = parts[1].split('@')
		parts[1] = '@!'.join(split_mention)
		print(parts[1])

	who = discord.utils.find(
		lambda u: u.mention == parts[1], message.guild.members)
	if who is None:
		await sent_message.edit(content='Hey, programmer man, you suck. There was an error.', delete_after=10.0)
		return True
	

	frequency = 0
	for channel in message.guild.text_channels:
		print('Searching channel \"{0}\" for phrase \"{1}\"'.format(channel.name, phrase))
		async for mes in channel.history(limit=None):
			if mes.author is not who or mes.content.startswith('..'):
				continue

			mes_lower = mes.content.lower()
			phrase_lower = phrase.lower()
			if phrase_lower in mes_lower and mes is not message:
				escaped = re.escape(phrase_lower)
				matches = re.findall(r'\b{0}\b'.format(escaped), mes_lower)
				count = len(matches)
				print('{0} ({1})'.format(mes.content, count))
				frequency += count
	timespan = datetime.datetime.now() - start
	print('Took {0}.'.format(timespan))
	await sent_message.edit(content='{0} used the phrase \"{1}\" {2} times!'.format(who.mention, phrase, frequency))
