import discord
import messaging_general
import messaging_other
import messaging_autonomous


async def receive_message(client, message=discord.Message):
	if message.author == client.user:
		return

	if message.author.bot:
		return

	def command(c): return message.content.startswith('..{0} '.format(c))

	# return if consumed. prevents intersections of commands (..history [] wig)

	consumed = await messaging_general.receive_message(client, message)
	if consumed:
		return

	consumed = await messaging_other.receive_message(client, message)
	if consumed:
		return

	consumed = await messaging_autonomous.receive_message(client, message)
	if consumed:
		return
