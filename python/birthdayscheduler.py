import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def start_scheduler(_client):
	scheduler.start()
	scheduler.add_job(job, 'interval', minutes=360, next_run_time=datetime.datetime.now(), kwargs={'client':_client})
	print('Scheduler started.')


def job(client):
	print('[INFO]\tRunning scheduled birthday checker.')
	f = open('../txt/birthdays.json', 'r')
	bdata = json.load(f)
	f.close()

	now = datetime.datetime.now()
	bdata.sort(key=lambda d : datetime.datetime.strptime(d.get('date'), '%B %d %Y') - now)
	next_date = datetime.datetime.strptime(bdata[0].get('date'), '%B %d %Y')
	next = bdata[0]
	print('Next birthday: {}'.format(next.get('date')))

	if next_date.month == now.month and next_date.day == now.day:
		import cache
		c = cache.Cache(549059925784002584)
		channel = c.get_channel_with_name('general', client)
		if channel is not None:
			import asyncio
			loop = client.loop
			loop.create_task(birthday_send(channel, next.get('name')))
			update_file()
		else:
			print('[ERROR]\tChannel was none.')


async def birthday_send(channel, name):
	await channel.send('Today is {}\'s birthday! Wish them a happy birthday!'.format(name))
	pass

def update_file():
	f = open('../txt/birthdays.json', 'r')
	bdata = json.load(f)
	f.close()

	now = datetime.datetime.now()
	bdata.sort(key=lambda d : datetime.datetime.strptime(d.get('date'), '%B %d %Y') - now)

	next_date = datetime.datetime.strptime(bdata[0].get('date'), '%B %d %Y')
	next_year = next_date.year + 1
	import calendar

	bdata[0]['date'] = '{} {} {}'.format(calendar.month_name[next_date.month], next_date.day, next_year)
	with open('../txt/birthdays.json', 'w') as outfile:
		json.dump(bdata, outfile)