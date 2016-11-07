from celery import Celery

app = Celery('tasks', backend='rpc://', broker='amqp://')

@app.task
def parse_price_file(data_to_parse):
	pass