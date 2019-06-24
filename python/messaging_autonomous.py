import discord
import re

# autonomous responses that are not triggered by a '..' command.

async def receive_message(client, message=discord.Message):
	message_lower = message.content.lower()
	message_split = message_lower.split()
	wig_match = re.search(r'\bwig\b', message.content.lower())
	if wig_match:
		await message.channel.send('wig')
		return True

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

	if re.search(r'\bqueen\b', message_lower):
		await message.channel.send('QUEEN')