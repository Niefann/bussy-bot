import discord
import info
import messaging
import cache

CLIENT = None

class DiscordClient(discord.Client):
	async def on_ready(self):
		import datetime
		now = datetime.datetime.now()
		print('Created at {0}!'.format(now.strftime('%H:%M:%S')))

	async def on_message(self, message):
		await messaging.receive_message(self, message)

	async def on_guild_join(self, guild):
		# initialize cache
		mycache = cache.Cache(guild.id)
		mycache.initialize(guild.id)
		print('Joined server \"{0}\"'.format(guild.name))
		general = discord.utils.find(lambda x: x.name == 'general', guild.text_channels)
		await general.send('Hi, Boppers!')

def get_client():
	return CLIENT

def main():
	client = DiscordClient()
	global CLIENT
	CLIENT = client
	client.run(info.get_token())


if __name__ == '__main__':
	main()
