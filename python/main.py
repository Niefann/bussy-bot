import discord
import info
import messaging
import cache
import birthdayscheduler


class DiscordClient(discord.Client):
	restart_on_kill = False

	async def on_ready(self):
		import datetime
		now = datetime.datetime.now()
		print('Created at {0}!'.format(now.strftime('%H:%M:%S')))
		mycache = cache.Cache(0)
		mycache.refresh(self)
		print('Cache refreshed.')
		birthdayscheduler.start_scheduler(self)


	async def on_message(self, message):
		await messaging.receive_message(self, message)


	async def on_guild_join(self, guild):
		# initialize cache
		mycache = cache.Cache(guild.id)
		mycache.initialize(guild)
		print('Joined server \"{0}\"'.format(guild.name))
		general = discord.utils.find(lambda x: x.name == 'general', guild.text_channels)
		await general.send('Hi, Boppers!')


def main():
	client = DiscordClient()
	client.run(info.get_token())
	# ..restart has been called
	if client.restart_on_kill:
		print('restarting')
		import subprocess
		subprocess.call(['../restart.sh'])
		pass


if __name__ == '__main__':
	main()
