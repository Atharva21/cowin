import datetime, yaml, requests, re, json, time, os, playsound
from colorama import init, Fore, Back
init()

NOT_FOUND = True

def printc(color, text, line=True):
	if(line):
		print(color + text + Fore.RESET)
	else:
		print(color + text + Fore.RESET, end='')

class Data:
	prop_file = "./resources/application.yml"
	
	def __init__(self):
		with open(Data.prop_file) as yamlfile:
			self.yml = yaml.load(yamlfile, Loader=yaml.FullLoader)
		if(self.yml is None or len(self.yml) == 0):
			raise Exception("error parsing yaml file")
		self.parse_props()
		self.validate()

	def parse_props(self):
		self.pincodes = str(self.get_prop("user.pincodes")).split(' ')
		self.uri = str(self.get_prop("api.uri"))
		self.findByPin = str(self.get_prop("api.endpoints.findByPin"))
		self.calendarByPin = str(self.get_prop("api.endpoints.calendarByPin"))
		self.botTimeout = str(self.get_prop("bot.timeout"))
	
	def get_prop(self, prop):
		# @Param: takes a "." seperated string ex: api.uri
		# @Returns: api->uri prop from self.yml
		try:
			if(prop is None or len(prop) == 0):
				raise Exception()
			keys = prop.split(".")
			value = None
			lookup = self.yml
			for key in keys:
				value = lookup.get(key)
				lookup = value
			if(value is None):
				raise Exception()
			return value
		except Exception as e:
			msg = "cannot find " + str(prop) + " in file " + Data.prop_file
			raise Exception(msg)
	
	def validate(self):
		for pincode in self.pincodes:
			if(pincode.isalpha() or len(pincode) != 6):
				raise Exception("Invalid Pincode")
		if(self.botTimeout.isalpha()):
			raise Exception("Invalid timeout")

def getslots(uri):
	my_headers = {
		"accept": "application/json",
		"Accept-Language": "hi_IN"
	}
	return json.loads(requests.get(uri, headers=my_headers).content.decode("utf-8"))

def printResponse(response):
	if(len(response.get("sessions")) == 0):
		printc(Fore.RED, "-------- No Slots found-----------")
		return
	global NOT_FOUND
	print(' '*46, 'slots')
	slots = {}
	for session in response.get("sessions"):
		slots[session.get("name")] = str(session.get("available_capacity_dose1"))

	for hospital, slots in slots.items():
		if(int(slots) < 2):
			clr = Fore.RED
		else:
			NOT_FOUND = False
			clr = Fore.GREEN
		hlen = len(hospital[:50])
		buffer = ' '*(50-hlen)
		printc(Fore.BLUE, hospital, False)
		print(buffer, ":    ", end='')
		printc(clr, slots)
		# print(hospital, buffer, ":", clr, slots)

def clrscr():
	# clears screen
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

def run():
	global NOT_FOUND
	data = Data()
	start_time = datetime.datetime.now()
	try:
		while(NOT_FOUND):
			clrscr()
			now = datetime.datetime.now()
			diff = now - start_time
			print("uptime: ", str(diff).split('.')[0])
			#### per pincode: ####
			today = "-".join(str(now).split(" ")[0].split("-")[::-1])
			for pincode in data.pincodes:
				print("\n\n" + Fore.YELLOW + pincode, Fore.RESET, end='')
				query = "?pincode="+pincode+"&date="+today
				uri = data.uri + data.findByPin + query
				response = getslots(uri)
				printResponse(response)
			if(not NOT_FOUND):
				playsound.playsound("./resources/alarm.mp3")
				break
			time.sleep(int(data.botTimeout))
	except KeyboardInterrupt:
		printc(Fore.GREEN, "done")

if __name__ == "__main__":
	run()
