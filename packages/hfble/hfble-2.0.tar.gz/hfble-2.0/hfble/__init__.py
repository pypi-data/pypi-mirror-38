import hashlib, random, os
SALT_CHARS = list("013456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_")
def clear():
	os.system("cls" if os.name == "nt" else "clear")

class LoginEngine():
	def __init__(self):
		self._hasher = None
		self.db = [] # should be set to a list of dicts of username-hashedPassword-salt-extra

	def SaltGen(self):
		retStr = ""
		for x in range(8):
			retStr += random.choice(SALT_CHARS) # random salting character
		return retStr

	def Encrypt(self, content):
		if not type(content) == str:
			raise TypeError("Invalid content argument for LoginEngine.Encrypt()")
		self._hasher = hashlib.sha512() # make a hasher
		self._hasher.update(content.encode("utf-8")) # hash the content in utf-8 bytes
		return self._hasher.hexdigest() # use hex notation

	def AccountFind(self, username):
		if not(type(username) == str):
			raise TypeError("Invalid username argument for LoginEngine.AccountFind() - expected str, got " + str(type(username)))
		for x in range(len(self.db)): # iterate through the database
			if self.db[x]["username"] == username: # check if it matches
				return x
		else: # if there are no matches
			return -1

	def Login(self, username, password):
		if not type(username) == str and type(password) == str:
			raise TypeError("Invalid argument(s) for LoginEngine.Login()")
		for x in range(0, len(self.db)): # iterate through the database
			if self.db[x]["username"] == username: # check if the username matches
				y = password + self.db[x]["salt"] # what to hash
				if self.Encrypt(y) == self.db[x]["hashedPassword"]: # check for password hash match
					return "SuccessfulLogin"
				else:
					return "IncorrectPassword"
				break
		else: # if there are no username matches
			return "UserDoesNotExist"

	def Register(self, username, password, UNprohibited, extra):
		if not((type(username) == str and type(password) == str) and (type(UNprohibited) == str or type(UNprohibited) == list) and (type(extra) == tuple)):
			raise TypeError("Invalid argument(s) for LoginEngine.Register()")
		for x in username: # iterate through the characters in the username
			if x in UNprohibited: # if there's a forbidden character
				return "InvalidCharInUsername"
		if len(username) == 0:
			return "EmptyUsername"
		if self.AccountFind(username) != -1: # check if someone already has this
			return "UsernameTaken"
		salt = self.SaltGen() # generate a salt
		dbAdd = {"username":username, "salt":salt, "hashedPassword":self.Encrypt(password + salt), "extra":extra} # the data to add
		self.db.append(dbAdd) # add the data
		return "SuccessfulRegister"

	def ChangePassword(self, username, oldPassword, newPassword):
		if not(type(username) == str and type(oldPassword) == str and type(newPassword) == str):
			raise TypeError("Invalid argument(s) for LoginEngine.ChangePassword()")
		status = self.Login(username, oldPassword) # try to login with the old password
		if status in ["IncorrectPassword", "UserDoesNotExist"]: # if the login failed
			return "InvalidLogin"
		else:
			salt = self.SaltGen() # generate a new salt
			hashed = self.Encrypt(newPassword + salt) # hash stuff
			num = self.AccountFind(username) # get the account id
			self.db[num]["salt"] = salt # update the db
			self.db[num]["hashedPassword"] = hashed # ^
			return "SuccessfulPasswordChange"


class LoginConsoleInteractivity(LoginEngine):
	def __init__(self, UNrestrict):
		super(LoginConsoleInteractivity, self).__init__()
		if not(type(UNrestrict) == str or type(UNrestrict) == list):
			raise TypeError("Invalid argument(s) for LoginConsoleInteractivity.__init__()")
		self.account = None
		self.UNrestrict = UNrestrict # forbidden username characters
	
	def UILogin(self, v=False):
		clear()
		status = None
		while status != "SuccessfulLogin":
			username = input("Username: ") # get username and password inputs
			password = input("Password: ")
			status = self.Login(username, password) # try to log in
			if v:
				print(status)
			if status in ["IncorrectPassword", "UserDoesNotExist"]:
				quit = input("Access denied. Enter \"quit\" to quit, press enter to continue.")
				if quit.strip().lower().startswith("q"): # if they want to quit
					self.UIMain(v) # go back to the homescreen
					return
		self.account = username # after they're successful
		input("Successfully logged in as '" + username + "'.\n(Press enter to continue)")
		self.UIMain() # go back to the homescreen
	
	def UIRegister(self, v=False):
		clear()
		status = None
		while status != "SuccessfulRegister":
			username = input("Username: ") # get username and password inputs
			password = input("Password: ")
			status = self.Register(username, password, self.UNrestrict, ()) # try to register
			if v:
				print(status)
			if status in ["InvalidCharInUsername", "UsernameTaken", "EmptyUsername"]:
				quit = input("Invalid username. Enter \"quit\" to quit, press enter to continue.")
				if quit.strip().lower().startswith("q"): # if they want to quit
					self.UIMain(v) # go back to the homescreen
					return
		self.account = username # after they're successful
		input("Successfully registered as '" + username + "'.\n(Press enter to continue)")
		self.UIMain() # go back to the homescreen

	def UIReadData(self, v=False):
		clear()
		try:
			accID = self.AccountFind(self.account) # get account number
		except TypeError: # if they're not logged in
			input("You're not logged in; log in first.\nPress enter to continue.")
			self.UIMain(v) # return to homescreen
			return
		data = self.db[accID]["extra"] # get user data
		if v:
			print(repr(data))
		for x in data: # output the data
			print(x)
		if len(data) == 0: # if there's nothing there
			input("You don't have any data; you might want to store some.\nPress enter to continue.")
		else:
			input("There's your data; press enter to continue.")
		self.UIMain(v) # return to the homescreen
		return

	def UIWriteData(self, v=False):
		clear()
		try:
			accID = self.AccountFind(self.account) # get account number
		except TypeError: # if they're not logged in
			input("You're not logged in; log in first.\nPress enter to continue.")
			self.UIMain(v) # return to homescreen
			return
		while True:
			try:
				dataNum = int(input("Enter the location/IDN of the data item you want to replace (starting with 1): ")) # what index of their data they want to replace
			except ValueError: # if they didn't enter a number
				input("Invalid input.\nPress enter to continue.")
			else:
				dataNum -= 1 # python indexing starts at 0, user indexing starts at 1
				break
		data = input("Enter the data you want to use to replace the previous data: ") # get replacement data
		try:
			data = int(data) # try to interpret it as a number
		except ValueError:
			try:
				data = float(data) # if it's not an integer, maybe it's a floating-point
			except ValueError:
				pass # if it's not a number at all, leave it as a string
		temp = self.db[accID]["extra"] # saving typing
		self.db[accID]["extra"] = temp[:dataNum] + (data,) + temp[dataNum + 1:] # insert the new data
		input("Editing successful.\nPress enter to continue.")
		self.UIMain(v) # return to homescreen
		return

	def UIAppendData(self, v=False):
		clear()
		try:
			accID = self.AccountFind(self.account) # get account number
		except TypeError: # if they're not logged in
			input("You're not logged in; log in first.\nPress enter to continue.")
			self.UIMain(v) # return to homescreen
			return
		data = input("Enter the data you want to use to append to your user data: ") # get appendable data
		try:
			data = int(data) # try to interpret it as an integer
		except ValueError:
			try:
				data = float(data) # if it's not an integer, maybe it's a floating-point
			except ValueError:
				pass # if it's not a number at all, leave it as a string
		self.db[accID]["extra"] = self.db[accID]["extra"] + (data,) # append the new data
		input("Appending successful.\nPress enter to continue.")
		self.UIMain(v) # return to homescreen
		return

	def UIChangePassword(self, v=False):
		clear() # clear the screen
		if v:
			print("self.account:", self.account)
		if self.account != None: # logged in
			old = input("Enter your old password: ") # get user inputs
			new1 = input("Enter your new password: ") # ^
			new2 = input("Re-enter your new password: ") # ^
			if new1 == new2: # if the copies of the new password match
				status = self.ChangePassword(self.account, old, new1) # try to change the password
				if status == "SuccessfulPasswordChange": # it worked?
					input("Password successfully changed.\nPress enter to continue.")
					self.UIMain(v) # return to the homescreen
					return
				else: # it didn't work
					input("Incorrect old password.\nPress enter to continue.")
					self.UIMain(v) # return to the homescreen
					return
			else: # if the copies of the new password don't match
				input("New passwords do not match.\nPress enter to continue.")
				self.UIMain(v) # return to the homescreen
				return
		else: # not logged in
			input("You're not logged in; log in first.\nPress enter to continue.")
			self.UIMain(v) # return to the homescreen
			return
		
	def UIMain(self, v=False):
		clear()
		if v:
			print(self.db)
			print(self.account)
		select = "_"
		while select[0] not in "lrqeac":
			clear()
			print("Powered by hfble")
			print(("Logged in as " + self.account) if (self.account) else ("Not logged in"))
			select = input("Do you want to log in, register, read your data, edit your data, append a data element, change your password, or exit the login menu?\nType in your choice and press enter. ") # have the user pick what to do
			select = select.strip().lower()
		if select[0] == "l": # log in
			self.UILogin(v)
		elif select[0] == "r": # register or read data
			try:
				if select[2] == "a": # read data
					self.UIReadData(v)
				else: # everything else, assume register
					self.UIRegister(v)
			except IndexError: # if they only gave "r" or "re", assume register
				self.UIRegister(v)
		elif select[0] == "a": # append
			self.UIAppendData(v)
		elif select[0] == "c": # change password
			self.UIChangePassword(v)
		elif select[0] == "e": # exit or edit data
			try:
				if select[1] == "d": # edit data
					self.UIWriteData(v)
				else: # everything else, asssume exit
					return
			except IndexError: # if they only gave "e", assume exit
				return
		elif select[0] == "q": # quit
			return
		else: # this should never happen
			print("DEBUG:")
			print(repr(select))
			print(select[0])
			print(select[0] in "lrqe")
			raise FileExistsError("Something very unexpected happened in LoginConsoleInteractivity.UIMain()...")


class SaveManagerText(): # strictly uses the same format as LoginEngine.db
	def __init__(self, filename):
		if type(filename) != str:
			raise TypeError("Invalid filename argument for SaveManagerText.__init__()")
		self.filename = filename
		self._writeFile = None # to hold file objects
		self._readFile = None
		try: # test if the file exists
			x = open(self.filename, "r")
		finally:
			x.close()
	
	def Read(self):
		try:
			self._readFile = open(self.filename, "r") # get file object
			t = self._readFile.read() # get text
			t = t.split("\n") # it's line-seperated
			retList = []
			d = {} # temporary dict
			ind = 0
			while True:
				try:
					a = t[ind + 1]
					d = {}
					d["username"] = t[ind]; ind += 1 # sequentially get items
					d["hashedPassword"] = t[ind]; ind += 1
					d["salt"] = t[ind]; ind += 1
					d["extra"] = eval(t[ind]); ind += 1 # this one is different - it stores repr() of the tuple
					retList.append(d) # store the dict on the end of retList
				except IndexError:
					return retList
		finally:
			self._readFile.close()
	
	def Write(self, db):
		if type(db) != list:
			raise TypeError("Invalid db argument for SaveManagerText.Write()")
		try:
			self._writeFile = open(self.filename, "w") # get a file object
			for x in db: # iterate through the database
				self._writeFile.write(x["username"] + "\n" + x["hashedPassword"] + "\n" + x["salt"] + "\n" + repr(x["extra"]) + "\n") # write all the things
		finally:
			self._writeFile.close()
