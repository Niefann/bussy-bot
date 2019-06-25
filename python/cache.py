import discord
import main
import json
import os


class Cache():
	def __init__(self, guild_id):
		self.id = guild_id


	def initialize(self, guild):
		try:
			os.mkdir('../cache/{0}'.format(self.id))
		except:
			pass
		f = open('../cache/{0}/data.json'.format(self.id), 'w')
		data = {}
		data['enabled_autos'] = ['wig', 'peet-zer', 'queen']
		data['members'] = []
		for member in guild.members:
			if member.bot:
				continue
			data['members'].append({
				'id': member.id,
				'mention': member.mention,
				'tag': member.name,
				'discriminator': member.discriminator
			})
		data['channels'] = []
		for channel in guild.text_channels:
			data['channels'].append({
				'id': channel.id,
				'name': channel.name
			})
		f.write(json.dumps(data))
		f.close()


	def refresh(self):
		client = main.get_client()
		for guild in client.guilds:
			print('Refreshing cache for guild {0}...'.format(guild.name))
			self.id = guild.id
			f = self.__get_file('r+')
			jsonstr = f.read()
			f.close()
			f = self.__get_file('w').close()
			f = self.__get_file('r+')
			data = json.loads(jsonstr)
			if [m['id'] for m in data['members']] != [m.id for m in guild.members]:
				data['members'] = []
				for member in guild.members:
					if member.bot:
						continue
					data['members'].append({
						'id': member.id,
						'mention': member.mention,
						'tag': member.name,
						'discriminator': member.discriminator
					})

			if [c['id'] for c in data['channels']] != [c.id for c in guild.text_channels]:
				data['channels'] = []
				for channel in guild.text_channels:
					data['channels'].append({
						'id': channel.id,
						'name': channel.name
					})
			f.write(json.dumps(data))
			f.close()
			print('Done.')


	def __get_file(self, how):
		return open('../cache/{0}/data.json'.format(self.id), how)


	def __load_data(self):
		client = main.get_client()
		f = self.__get_file('r')
		data = f.read()
		f.close()
		return json.loads(data)


	def get_enabled_autos(self):
		data = self.__load_data()
		return set(data.get('enabled_autos'))


	def set_enabled_autos(self, enabled):
		data = self.__load_data()
		data['enabled_autos'] = enabled
		f = self.__get_file('w')
		f.write(json.dumps(data))
		f.close()


	def get_member_with_tag(self, discord_tag):
		data = self.__load_data()
		members = data['members']
		match = filter(lambda m: m.get('tag').lower() == discord_tag.lower(), members)
		return match


	def get_channel_with_name(self, channel_name):
		data = self.__load_data()
		channels = data['channels']
		match = filter(lambda c: channel_name.lower() in c.get('name').lower(), channels)
		return match
