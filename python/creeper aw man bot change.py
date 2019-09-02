async def creeper(message):
	mycache = cache.Cache(message.guild.id)
	if 'creeper' not in mycache.get_enabled_autos():
		return False
	
	creeper_match = re.search(r'\bcreeper\b', message.content.lower())
	if creeper_match:
		await message.channel.send('aw man')
		return True