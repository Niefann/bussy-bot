import discord
import main
import json
import os


class Cache():
	def __init__(self, guild_id):
		self.id = guild_id

	def initialize(self):
		try:
			os.mkdir('../cache/{0}'.format(self.id))
		except:
			pass
		f = open('../cache/{0}/settings.json'.format(self.id), 'w')
		f.write('\{\"enabled_autos\":[\"wig\",\"peet-zer\"]\}')
		f.close()

	def __get_file(self, how):
		return open('../cache/{0}/settings.json'.format(self.id), how)

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