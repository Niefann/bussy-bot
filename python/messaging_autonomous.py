import discord
import re

# autonomous responses that are not triggered by a '..' command.

async def receive_message(client, message=discord.Message):
	wig_match = re.search(r'\bwig\b', message.content.lower())
	if wig_match:
		await message.channel.send('wig')
		return True