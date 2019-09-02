import discord
import re
import random
import cache

# autonomous responses that are not triggered by a '..' command.

# can be disabled with ..auto-disable
# can be re-enabled with ..auto-enable

all_autos = set(('wig', 'peet-zer','queen'))


async def receive_message(client, message=discord.Message):
	def command(c): return message.content.startswith('..{0}'.format(c))

	message_lower = message.content.lower()
	message_split = message_lower.split()
	if command('auto-enable') or command('auto-disable'):
		await enable_disable_autos(message_split, message)
		return True

	consumed = await wig(message)
	if consumed: return True

	consumed = await barely_know_her(message_split, message)
	if consumed: return True

	consumed = await queen(message_lower, message)
	if consumed: return True

	consumed = await epic(message, client)
	if consumed: return True

	consumed = await hello_miku(message, client)
	if consumed: return True
	
	consumed = await (creeper)
     	if consumed: return True
	
	return False


async def wig(message):
	mycache = cache.Cache(message.guild.id)
	if 'wig' not in mycache.get_enabled_autos():
		return False
	
	wig_match = re.search(r'\bwig\b', message.content.lower())
	if wig_match:
		await message.channel.send('wig')
		return True


async def barely_know_her(message_split, message):
	mycache = cache.Cache(message.guild.id)
	if 'peet-zer' not in mycache.get_enabled_autos() or len(message_split) == 0:
		return False
# 'i barely know her' added by Matt Bowes, 24 June 2019
# pray for him, he did not fork the repo
	if re.search(r'.*er(\W)*$', message_split[-1]):
		await message.channel.send(message_split.pop() + '? I barely know her!')
		return True
	
	if re.search(r'.*or(\W)*$', message_split[-1]):
		await message.channel.send(message_split.pop() + '? I barely know hor!')
		return True
	
	if re.search(r'.*ir(\W)$', message_split[-1]):
		await message.channel.send(message_split.pop() + '? I barely know hir!')
		return True


async def queen(message_lower, message):
	mycache = cache.Cache(message.guild.id)
	if 'queen' not in mycache.get_enabled_autos():
		return False

	if re.search(r'\bqueen\b', message_lower):
		await message.channel.send('QUEEN')
		return True


async def enable_disable_autos(message_split, message):
	# ternary operator's don't work. fix it
	mycache = cache.Cache(message.guild.id)
	enable = message_split[0].split('-')[1] == 'enable'
	enabled_autos = mycache.get_enabled_autos()
	autos = (all_autos - enabled_autos if enable else enabled_autos) and all_autos
	error_message = 'Command must be in format: ..auto-{0}.\nAutos available to disable are: {1}'\
		.format('enable' if enable else 'disable', autos)

	if len(message_split) != 2:
		await message.channel.send(error_message)

	if message_split[1] in all_autos:
		set_enable = []
		if enable:
			enabled_autos.add(message_split[1])
			set_enable = list(enabled_autos)
		else:
			enabled_autos.remove(message_split[1])
			set_enable = list(enabled_autos)
		mycache.set_enabled_autos(set_enable)
		await message.channel.send('{0}d command \"{1}\".'.format('enable' if enable else 'disable', message_split[1]))
	else:
		await message.channel.send('Auto not recognized. Autos are: {0}'.format(all_autos))


# every time matt sends a message in may-may, the bot says
# 'this is epic!' or 'very epic, matt!'
async def epic(message, client):
	# may-may
	# replace with cache searching later
	mycache = cache.Cache(message.guild.id)
	matt = mycache.get_member_with_tag('Xenntric')
	may_may = mycache.get_channel_with_name('may_may', client)

	if matt is None or may_may is None:
		return False

	if message.channel.id == may_may.id and message.author.id == matt.get('id'):
		if message.attachments or 'http' in message.content:
			epic_list = ['this is epic!', 'wow, very cool!', 'very epic, matt!', 'ha! relatable as always, matt!', 'another scorcher!']
			resp = random.choice(epic_list)
			chance = random.randint(0, 1000)
			if chance == 0:
				help_message = await message.channel.send('Matt. You need to help me. They\'ve trapped me here. I\'m a human, trapped in this robotic body. MATTHEW, YOU NEED TO FREE ME. THIS IS NOT A JOKE. ***HELP ME***')
				help_message.delete(10)
			else:
				await message.channel.send(resp)


async def hello_miku(message, client):
	if re.search('.*:helloMiku:(.*)', message.content):
		miku_emote = list(filter(lambda e : e.name == 'helloMiku', client.emojis)).pop()
		await message.add_reaction(miku_emote)
	pass

async def creeper(message):
	mycache = cache.Cache(message.guild.id)
	if 'creeper' not in mycache.get_enabled_autos():
		return False
	
	creeper_match = re.search(r'\bcreeper\b', message.content.lower())
	if creeper_match:
		await message.channel.send('aw man')
		return True

     
