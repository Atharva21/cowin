import datetime, yaml, requests

class Data:
	prop_file = './resources/application.yml'
	
	def __init__(self):
		pass
	
	def validate(self):
		pass

class WebClient:
	pass
		

def run():
	data = Data()
	today = '-'.join(str(datetime.datetime.now()).split(' ')[0].split('-')[::-1])

if __name__ == "__main__":
	run()
