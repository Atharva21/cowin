import datetime, yaml, requests, re, json, time, os, playsound

COUNTER = 0
NOT_FOUND = True

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
		self.pincode = str(self.get_prop("user.pincode"))
		self.uri = str(self.get_prop("api.uri"))
		self.findByPin = str(self.get_prop("api.endpoints.findByPin"))
		self.calendarByPin = str(self.get_prop("api.endpoints.calendarByPin"))
	
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
		if(not (self.pincode.isnumeric() and len(self.pincode) == 6)):
			raise Exception("Invalid Pincode")

def getslots(data, date):
	query = "?pincode="+data.pincode+"&date="+date
	uri = data.uri + data.findByPin + query
	my_headers = {
		"accept": "application/json",
		"Accept-Language": "hi_IN"
	}
	return requests.get(uri, headers=my_headers)

def handleResponse(response):
	slots = {}
	os.system('cls')
	global COUNTER, NOT_FOUND
	print("uptime", COUNTER, "s")
	print(' '*52, 'slots')
	COUNTER = (COUNTER+1)%36000;
	for session in response.get("sessions"):
		slots[session.get("name")] = str(session.get("available_capacity_dose1"))
		# print(session.get("name") + ": " + str(session.get("available_capacity_dose1")))

	for hospital, slots in slots.items():
		if(slots == '0'):
			clr = bcolors.FAIL
		else:
			NOT_FOUND = False
			clr = bcolors.OKGREEN
		hlen = len(hospital[:50])
		buffer = ' '*(50-hlen)
		print(hospital, buffer, ":", clr, slots, bcolors.ENDC)

def run():
	global NOT_FOUND
	data = Data()
	try:
		while(NOT_FOUND):
			today = "-".join(str(datetime.datetime.now()).split(" ")[0].split("-")[::-1])
			response = json.loads(getslots(data, today).content.decode("utf-8"))
			handleResponse(response)
			time.sleep(1)
		if(not NOT_FOUND):
			playsound.playsound("./resources/alarm.mp3")
	except KeyboardInterrupt:
		os.system("cls")
		print("done")

if __name__ == "__main__":
	run()
