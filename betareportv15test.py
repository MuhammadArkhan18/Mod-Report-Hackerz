#Python Source Code v3
#By @VrozAnims2003
#--------------------------------------------------------------------------------------------------------------------
#Modul ini menggunakan python-telegram-bot.
#Silahkan didownload terlebih dahulu!
#https://github.com/python-telegram-bot/python-telegram-bot
#--------------------------------------------------------------------------------------------------------------------
#Script Bot v1:
#-First Release!
#-added response function for example
#-added polling system
#-added logging for handle error
#-added dispatcher for handle message
#
#Script Bot v2:
#-remake syntax code for good looking to read
#-added some explain about how-it-work?
#-added started bot message
#-added checking tokenbot
#-added checking module for handle import error
#
#Script Bot v3:
#-Added Debug Mode! For helping testing bot in polling
#-remake started bot message
#-added Bot Name for identity
#-added import run_async for handle multiple request from users (If we don't use this, will be big BUG!)
#-added webhook syntax for Heroku (Another Web Hosting Coming Soon!)
#####################################################################################################################

#Mengimpor Updater
try:
	from telegram.ext import Updater
	import os
	from pprint import pprint 
	from telegram.ext.dispatcher import run_async
	import sqlite3
except ImportError as e:
	print("Tolong download modul: https://github.com/python-telegram-bot/python-telegram-bot")
	exit()

#Isi token bot kamu
tokenbot = '410015493:AAFlE_X2ISDYMv-49dQ9GOUS22qWvP6Ktog'
namebot	 = 'MOD Report'
ScriptVer= 'v1.4 build 4'

gmodbase = sqlite3.connect("gmodli.db")
cmodbase = sqlite3.connect("cmod.db")

creator  = 297620679
tester   = [340639887, 296568646]
tag      = None
mod      = None
botdect  = False
clie     = None
stillr = {}
stilld = {}
countrymod= False
rulebreakerc = False
rulebreakerg = False
processgmod = False
processcmod = False
processbug = False
sendscreeng = False
sendscreenc = False
sendscreenb = False
kindmod = False
reportercmod= {}
reportergmod= {}
reporterbug = {}
checkbugdone = False
checkgmoddone = False
checkcmoddone = False
checkgmodadone = False
sendscreenalt = False
reportergn = {}
reportercn = {}
reporterbn = {}

gmodlist = gmodbase.execute("SELECT CHATID FROM GMOD;")
cmodlist = cmodbase.execute("SELECT CHATID FROM CMOD;")
cmodclist = cmodbase.execute("SELECT CHATID, COUNTRY FROM CMOD;")
countrylist = cmodbase.execute("SELECT COUNTRY FROM COUNTRY;")

gmoddata 	 = []
cmoddata 	 = []
countrycmoddata = {}

for gmod in gmodlist:
	gmodu = int(gmod[0])
	new	  = [gmodu]

	gmoddata+= new

for cmod in cmodlist:
	cmodu = int(cmod[0])
	new = [cmodu]
	cmoddata+= new

for countr in countrylist:
	co = str(countr[0])
	countrycmoddata.update({co:[]})

for cmo in cmodclist:
	chtd = int(cmo[0])
	cout = str(cmo[1])
	new = [chtd]
	countrycmoddata[cout]+= new

cmodbase.close()
gmodbase.close()

print(gmoddata)
print(countrycmoddata)
#jebakan bagi yang tidak mengisi token (jangan dihapus!)
#Menset variabel tokenbot agar ditangani oleh Updater
try:
	updater = Updater(tokenbot)
except ValueError as e:
	print("Tolong masukkan token bot!")
	exit()

#Webhook(Heroku):
#-------------------------------
PORT = int(os.environ.get('PORT', '5000'))
updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

updater.bot.start_webhook("https://secure-beyond-56551.herokuapp.com/" + TOKEN)
#--------------------------------

#Mengambil dispatcher untuk menangani command
dispatcher = updater.dispatcher

#####################################################################################################################

#mengimpor logging untuk menangani error
import logging

#menset peraturan logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#####################################################################################################################

#Mengimpor telegram (Untuk Markdown / html)
#Mengimpor run_async (untuk menangani masalah permintaan user)
try:
	import telegram
	import time
	import sys
	from functools import wraps
except ImportError as e:
	print("Masalah: ", e)
	exit()

######################################################################################################################

def gmod_only(func):
	global gmodlist
	global creator
	@wraps(func)
	def wrapped(bot, update, *args, **kwargs):
		user_id = update.effective_user.id
		if user_id not in gmodlist:
			print("Unauthorized access denied for {}.".format(user_id))
			return
		return func(bot, update, *args, **kwargs)
	return wrapped

#------------------------------------------------------------------------------------------------------------------------------------------

def pm_only(func):
	@wraps(func)
	def wrapped(bot, update, *args, **kwargs):
		user   = update.effective_user.id
		chatid = update.message.chat_id
		if chatid < 0:
			return
		return func(bot, update, *args, **kwargs)
	return wrapped

#------------------------------------------------------------------------------------------------------------------------------------------

def creator_only(func):
	global creator
	@wraps(func)
	def wrapped(bot, update, *args, **kwargs):
		user   = update.effective_user.id
		chatid = update.message.chat_id
		if chatid < 0:
			print("some group access command : {}.".format(user))
			return
		if chatid != creator:
			print("Unauthorized access denied for {}".format(user))
			return
		return func(bot, update, *args, **kwargs)
	return wrapped

#------------------------------------------------------------------------------------------------------------------------------------------

def group_only(func):
	@wraps(func)
	def wrapped(bot, update, *args, **kwargs):
		user   = update.effective_user.id
		chat_id= update.message.chat_id
		if chat_id >= 0:
			update.message.reply_text("Group Only!")
			return
		return func(bot, update, *args, **kwargs)
	return wrapped

#############################################################################################################################################

def creator_menu(bot, update):
	create= update.effective_user.username

	msg = "Hello `"+create+"`(creator) !\n"
	msg+= "\n"
	msg+= "You can look all user id, send message to user privately, and other as creator.\n"
	msg+= "\n"
	msg+= "----------------------------"

	custom_keyboard = [['Creator Menu'], ['Gmod Menu'], ['Cmod Menu'], ['User Menu']]

	reply_markup 	= telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup)

def tester_menu(bot, update):
	teste= update.effective_user.username

	msg = "Hello `"+teste+"` (Tester) !\n"
	msg+= "\n"
	msg+= "-------------------------------"

	custom_keyboard = [['Tester Menu'], ['Gmod Menu'], ['Cmod Menu'], ['User Menu']]

	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup)

def tester_menus(bot, update):
	msg = "*Tester Menu*:\n"
	msg+= "-------------------------\n"
	msg+= "This is menu for tester"

	custom_keyboard = [['Report', 'Accept Report'],['How To Report', 'Tester Command'], ['User Command', 'About This Bot'], ['Rules'], ['Back To Tester']]

	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup)

#------------------------------------------------------------------------------------------------------------------------------------------

@creator_only
def creator_menus(bot, update):
	msg = "*Creator Menu*:\n"
	msg+= "-------------------------\n"
	msg+= "This is menu for creator"

	custom_keyboard = [['Report', 'Accept Report'],['How To Report', 'Creator Command'], ['User Command', 'About This Bot'], ['Rules'], ['Back To Creator']]

	reply_markup	= telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------


@run_async
def gmod_menu(bot, update):
	global creator
	global tester
	if update.message.chat_id == creator or update.message.chat_id in tester:
		if update.message.chat_id == creator:
			msg = "*Gmod Menu*:\n"
			msg+= "------------------------\n"
			msg+= "This is menu for Gmod"

			custom_keyboard = [['Report', 'Accept Report'],['How To Report', 'Gmod Command'], ['User Command', 'About This Bot'], ['Rules'], ['Back To Creator']]

			reply_markup	= telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
			bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

		elif update.message.chat_id in tester:
			msg = "*Gmod Menu*:\n"
			msg+= "------------------------\n"
			msg+= "This is menu for Gmod"

			custom_keyboard = [['Report', 'Accept Report'],['How To Report', 'Gmod Command'], ['User Command', 'About This Bot'], ['Rules'], ['Back To Tester']]

			reply_markup	= telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
			bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

	elif update.message.chat_id != creator or update.message.chat_id not in tester:

		user= update.message.from_user
		first_name = user.first_name

		msg = "Welcome `"+first_name+"` !\n"
		msg+= "---------------------------\n"
		msg+= "*GMOD Menu*:\n"
		msg+= "---------------------------"

		custom_keyboard = [['Report', 'Accept Report'],['How To Report', 'Gmod Command'], ['User Command', 'About This Bot'], ['Rules']]

		reply_markup 	= telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
		bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
def cmod_menu(bot, update):
	global creator
	global tester
	if update.message.chat_id == creator or update.message.chat_id in tester:
		if update.message.chat_id == creator:
			msg = "*Cmod Menu*:\n"
			msg+= "-----------------------\n"
			msg+= "This is menu for Cmod"

			custom_keyboard = [['Report', 'Accept Report'],['How To Report', 'Cmod Command'], ['User Command', 'About This Bot'], ['Rules'], ['Back To Creator']]

			reply_markup	= telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
			bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

		elif update.message.chat_id in tester:
			msg = "*Cmod Menu*:\n"
			msg+= "------------------------\n"
			msg+= "This is menu for Cmod"

			custom_keyboard = [['Report', 'Accept Report'],['How To Report', 'Cmod Command'], ['User Command', 'About This Bot'], ['Rules'], ['Back To Tester']]

			reply_markup	= telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
			bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

	elif update.message.chat_id != creator or update.message.chat_id not in tester:

		user = update.message.from_user
		first_name = user.first_name

		msg = "Welcome `"+first_name+"` !\n"
		msg+= "----------------------------\n"
		msg+= "*CMOD Menu*:\n"
		msg+= "----------------------------\n"

		custom_keyboard = [['Report', 'Accept Report'],['How To Report', 'Cmod Command'], ['User Command','About This Bot'], ['Rules']]

		reply_markup	= telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
		bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
def user_menu(bot, update):
	global creator
	global tester
	if update.message.chat_id == creator or update.message.chat_id in tester:
		if update.message.chat_id == creator:
			msg = "*User Menu*:\n"
			msg+= "-------------------\n"
			msg+= "This is menu for User"

			custom_keyboard = [['Report'],['How To Report', 'User Command'], ['About This Bot'], ['Rules'], ['Back To Creator']]

			reply_markup	= telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
			bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

		elif update.message.chat_id in tester:
			msg = "*User Menu*:\n"
			msg+= "------------------------\n"
			msg+= "This is menu for Gmod"

			custom_keyboard = [['Report'],['How To Report', 'User Command'], ['About This Bot'], ['Rules'], ['Back To Tester']]

			reply_markup	= telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
			bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

	elif update.message.chat_id != creator or update.message.chat_id not in tester:

		user = update.message.from_user
		first_name = user.first_name

		msg = "Welcome `"+first_name+"` !\n"
		msg+= "---------------------------\n"
		msg+= "*USER MENU*:\n"
		msg+= "---------------------------\n"

		custom_keyboard = [['Report'],['How To Report', 'User Command'], ['About This Bot'], ['Rules']]

		reply_markup	= telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
		bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)



#############################################################################################################################################

@run_async
@pm_only
def start(bot, update):
	user = update.message.from_user
	first_name = user.first_name

	msg = "*WELCOME TO MOD REPORT*\n"
	msg+= "------------------------\n"
	msg+= "Hello "+first_name+" !\n"
	msg+= "\n"
	msg+= "I'am MOD REPORT BOT BETA\n"
	msg+= "You can report user in Hackerz game in here.\n"
	msg+="Just send report and wait Mod for confirm it..\n"
	msg+= "\n"
	msg+= "------------------------\n"
	msg+= "*NEW UPDATES "+ScriptVer+"!!*\n"
	msg+= "-> Tester can add, look, and remove\nGMOD Access from user\n"
	msg+= "-> SQL Database added 100% COMPLETE\n"
	msg+= "-> Some feature removed\n"
	msg+= "------------------------"

	custom_keyboard = [['Menu']]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@pm_only
def menu(bot, update):
	global gmoddata
	global cmoddata
	global creator
	global tester

	print(cmoddata)
	print(gmoddata)

	if update.message.chat_id == creator:
		creator_menus(bot, update)

	elif update.message.chat_id in tester:
		tester_menus(bot, update)

	elif update.message.chat_id in gmoddata:
		gmod_menu(bot, update)


	elif update.message.chat_id in cmoddata:
		cmod_menu(bot, update)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@pm_only
def reportalt(bot, update, args):
	global creator
	global tester
	global mod
	global user
	global reasn
	global region
	global usern
	global chatid
	global reportergmod
	global reportercmod
	global reporterbug
	global sendscreenalt
	global countrycmoddata

	banbase = sqlite3.connect("ban.db")
	banlist = banbase.execute("SELECT CHATID FROM BAN;")
	bandata = []
	for ban in banlist:
		banu = int(ban[0])
		new = [banu]
		bandata+= new

	banlist.close()
	usern = update.effective_user.username
	chatid = update.message.chat_id

	if update.effective_user.username == None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set your @ username...")
		return

	if update.message.chat_id in bandata:
		msg = "*Your Access Has Been Blocked!*"
		bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

	elif update.message.chat_id > 0:
		try:
			mod = str(args[0])
		except ValueError as e:
			update.message.reply_text("Kind of mod invalid, please check again...")
			return
		if mod == 'gmod':
			user = str(args[1])
			if user == '':
				update.message.reply_text("Check your command again...")
				return
			reasn = str(' '.join(args[2:]))
			if reasn == '' or '_' in reasn:
				update.message.reply_text("Please don't use underscore or blank reason..")

			update.message.reply_text("Send SS for proof your report..")
			sendscreenalt = True
			return

		elif mod == 'cmod':
			region = str(args[1])
			user = str(args[2])
			if region == '' or len(region) != 2:
				update.message.reply_text("Sorry, your Country Tag is invalid")
				return
			if user == '' or len(user) > 13:
				update.message.reply_text("Seem you just spamming, please use report feature for REPORT RULES BREAKER, not SPAMMING MODS!")
				return
			reasn = str(' '.join(args[3:]))
			if reasn == '' or '_' in reasn:
				update.message.reply_text("Please don't use underscore or blank reason..")

			try:
				test = countrycmoddata[region]
			except KeyError as e:
				bot.send_message(chat_id=update.message.chat_id, text="Sorry, your country tag is invalid or not registered. Please pm @VrozAnims2003 for resolve this..")

			update.message.reply_text("send SS for proof your report..")
			sendscreenalt = True

			return

		elif mod == 'bug':
			reasn = str(' '.join(args[1:]))
			if reasn == '' or '_' in reasn:
				update.message.reply_text("Please don't use underscore or blank bug content..")

			update.message.reply_text("send SS for helping developer to fix it...")
			sendss = True
			return

		else:
			update.message.reply_text("Receiver argument is invalid, please check your command syntax!")



@run_async
@pm_only
def sendssalt(bot, update):
	global creator
	global tester
	global mod
	global region
	global user
	global reasn
	global sendss
	global gmoddata
	global reportergmod
	global reportercmod
	global reporterbug
	global reportergn
	global reportercn
	global reporterbn
	global sendscreenalt
	global countrycmoddata

	#reporter database
	user_name = '`'+update.message.from_user.first_name+'`'
	username  = '`@'+update.effective_user.username+'`'
	userq = '`'+user+'`'
	reasnq = '`'+reasn+'`'

	if mod == 'gmod':
		msgg = "*GMOD REPORT*\n"
		msgg+= "-----------------------------\n"
		msgg+= "*User*   : "+user_name+"\n"
		msgg+= "*Username* : "+username+"\n"
		msgg+= "*User Breaker* : "+user+"\n"
		msgg+= "*Reason* : \n"+reasnq+"\n"
		msgg+= "-----------------------------"

		photos = update.message.photo[-1].file_id

		sendscreenalt = False

		newreporterq = {update.effective_user.username:update.message.chat_id}
		newreporterw = {update.effective_user.username:update.message.from_user.first_name}
		reportergmod.update(newreporterq)
		reportergn.update(newreporterw)

		update.message.reply_text("Your Report has been sent, wait until CMOD/GMOD accept it..")

		bot.send_message(chat_id=creator, text=msgg, parse_mode=telegram.ParseMode.MARKDOWN)
		bot.send_photo(chat_id=creator, photo=photos)

		for test in tester:
			bot.send_message(chat_id=test, text=msgg, parse_mode=telegram.ParseMode.MARKDOWN)
			bot.send_photo(chat_id=test, photo=photos)

		try:
			for gmod in gmoddata:
				bot.send_message(chat_id=gmod, text=msgg, parse_mode=telegram.ParseMode.MARKDOWN)
				bot.send_photo(chat_id=gmod, photo=photos)
		except telegram.TelegramError as e:
			bot.send_message(chat_id=creator, text="Some GMOD Not PM Manually...")

	elif mod == 'cmod':
		cmodregiondata = []

		for cmod in countrycmoddata[region]:
			cmodu = int(cmod)
			new = [cmodu]
			cmodregiondata+= new

		tag = region.upper()

		msgc = "["+tag+"] *CMOD REPORT*\n"
		msgc+= "-----------------------------\n"
		msgc+= "*User*   : "+user_name+"\n"
		msgc+= "*Username* : "+username+"\n"
		msgc+= "*User Breaker* : "+user+"\n"
		msgc+= "*Reason* : \n"+reasnq+"\n"
		msgc+= "-----------------------------"

		photos = update.message.photo[-1].file_id

		sendscreenalt = False

		newreporterq = {update.effective_user.username:update.message.chat_id}
		newreporterw = {update.effective_user.username:update.message.from_user.first_name}
		reportergmod.update(newreporterq)
		reportergn.update(newreporterw)

		update.message.reply_text("Your Report has been sent, wait until CMOD/GMOD accept it..")

		bot.send_message(chat_id=creator, text=msgg, parse_mode=telegram.ParseMode.MARKDOWN)
		bot.send_photo(chat_id=creator, photo=photos)

		for test in tester:
			bot.send_message(chat_id=test, text=msgg, parse_mode=telegram.ParseMode.MARKDOWN)
			bot.send_photo(chat_id=test, photo=photos)

		try:
			for gmod in gmoddata:
				bot.send_message(chat_id=gmod, text=msgg, parse_mode=telegram.ParseMode.MARKDOWN)
				bot.send_photo(chat_id=gmod, photo=photos)
		except telegram.TelegramError as e:
			bot.send_message(chat_id=creator, text="Some GMOD Not PM Manually...")

		finally:
			try:
				for cmod in cmodregiondata:
					bot.send_message(chat_id=cmod, text=msgc, parse_mode=telegram.ParseMode.MARKDOWN)
					bot.send_photo(chat_id=cmod, photo=photos)
			except telegram.TelegramError as e:
				bot.send_message(chat_id=creator, text="Some CMOD Blocked or Not PM Manually this chat...")


@run_async
@pm_only
def report(bot, update):
	global creator
	global tester
	global kindmod
	global stillr
	
	banbase = sqlite3.connect("ban.db")
	banlist = banbase.execute("SELECT CHATID FROM BAN;")
	bandata = []
	for ban in banlist:
		banu = int(ban[0])
		new = [banu]
		bandata+= new

	banlist.close()
	usern = update.effective_user.username
	chatid = update.message.chat_id

	if update.effective_user.username == None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set your @ username...")
		return

	if update.message.chat_id in bandata:
		msg = "*Your Access Has Been Blocked!*"
		bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

	if update.message.chat_id not in bandata:
		if update.message.chat_id > 0:
			kindmod = True
			stillr.update({usern:chatid})
			custom_keyboard = [['Gmod', 'Cmod', 'Bug'], ['Cancel']]
			reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
			bot.send_message(chat_id=update.message.chat_id, text="What kind report do you want?", reply_markup=reply_markup)
		elif update.message.chat_id < 0:
			return

@run_async
@pm_only
def reportbreaker(bot, update):
	global kindmod
	global rulebreakerg
	global countrymod
	global rulebreaker
	global processbug
	global stillr
	choice = update.message.text.split(' ')
	if choice[0] == 'Cancel':
		kindmod = False
		del stillr[update.effective_user.username]
		bot.send_message(chat_id=update.message.chat_id, text="Go out from report")
		return menu(bot, update)
	if choice[0] == "gmod" or choice[0] == "Gmod":
		reply_markup = telegram.ReplyKeyboardRemove()
		bot.send_message(chat_id=update.message.chat_id, text="Please input Rules Breaker's name (IGN)..", reply_markup=reply_markup)
		kindmod = False
		rulebreakerg = True
		return
	elif choice[0] == "cmod" or choice[0] == "Cmod":
		reply_markup = telegram.ReplyKeyboardRemove()
		bot.send_message(chat_id=update.message.chat_id, text="Please input your country (use tag)..", reply_markup=reply_markup)
		kindmod = False
		countrymod = True
		return
	elif choice[0] == "bug" or choice[0] == "Bug":
		reply_markup = telegram.ReplyKeyboardRemove()
		bot.send_message(chat_id=update.message.chat_id, text="Please explain bug in this bot..", reply_markup=reply_markup)
		kindmod = False
		processbug = True
		return
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Please input correctly, try again..")

@run_async
@pm_only
def reportreasong(bot, update):
	global rulebreakerg
	global rulebreakerq
	global processgmod
	if ' ' in update.message.text or '' == update.message.text:
		bot.send_message(chat_id=update.message.chat_id, text="Please input rules breaker's name correctly, try again..")
		return
	rulebreakerq = "`"+str(update.message.text)+"`"
	bot.send_message(chat_id=update.message.chat_id, text="Please input reason for reporting user to gmod..")
	rulebreakerg = False
	processgmod = True

@run_async
@pm_only
def reportcountryc(bot, update):
	global countrymod
	global tagcountry
	global rulebreakerc
	global countrycmoddata
	if ' ' in update.message.text or '' == update.message.text:
		bot.send_message(chat_id=update.message.chat_id, text="Please input country correctly, try again..")
		return
	if len(update.message.text) > 2 or len(update.message.text) < 2:
		bot.send_message(chat_id=update.message.chat_id, text="Use tag for country, like -> id (Indonesia), us (USA), gb (British), and other")
	try:
		test = countrycmoddata[update.message.text]
	except KeyError as e:
		bot.send_message(chat_id=update.message.chat_id, text="Your Country unregistered or invalid, please PM @VrozAnims2003 for resolve this")
	tagcountry = str(update.message.text)
	bot.send_message(chat_id=update.message.chat_id, text="Please input Rules Breaker's name (IGN)..")
	rulebreakerc = True
	countrymod = False

@run_async
@pm_only
def reportreasonc(bot, update):
	global rulebreakerc
	global rulebreakerw
	global processcmod
	if ' ' in update.message.text or '' == update.message.text:
		bot.send_message(chat_id=update.message.chat_id, text="Please input rules breaker's name correctly, try again..")
		return
	rulebreakerw = "`"+str(update.message.text)+"`"
	bot.send_message(chat_id=update.message.chat_id, text="Please input reason for reporting user to cmod..")
	rulebreakerc = False
	processcmod = True

@run_async
@pm_only
def reportprocessg(bot, update):
	global processgmod
	global rulebreakerq
	global sendscreeng
	global msgg
	global userg
	user = update.message.from_user
	last_name = user.last_name
	if last_name == None:
		last_name = ''
	user_name = "`"+user.first_name+last_name+"`"
	userg = user_name
	username = update.effective_user.username
	reasong = "`"+str(update.message.text)+"`"
	usern = "`"+username+"`"
	msgg = "*GMOD REPORT*\n"
	msgg+= "-----------------------------\n"
	msgg+= "*User*   : "+user_name+"\n"
	msgg+= "*Username* : @"+usern+"\n"
	msgg+= "*User Breaker* : "+rulebreakerq+"\n"
	msgg+= "*Reason* : \n"+reasong+"\n"
	msgg+= "-----------------------------"
	bot.send_message(chat_id=update.message.chat_id, text="Please send screenshot for proof your report...")
	processgmod = False
	sendscreeng = True

@run_async
@pm_only
def reportprocessc(bot, update):
	global processcmod
	global rulebreakerw
	global sendscreenc
	global msgc
	global tagcountry
	global tagup
	global userc
	user = update.message.from_user
	last_name = user.last_name
	if last_name == None:
		last_name = ''
	user_name = "`"+user.first_name+last_name+"`"
	userc = user_name
	username = update.effective_user.username
	reasonc = "`"+str(update.message.text)+"`"
	tagup = tagcountry.upper()
	usern = "`"+username+"`"
	msgc = " ["+tagup+"] *CMOD REPORT*\n"
	msgc+= "-----------------------------\n"
	msgc+= "*User Name* : "+user_name+"\n"
	msgc+= "*Username* : @"+usern+"\n"
	msgc+= "*Rules Breaker* : "+rulebreakerw+"\n"
	msgc+= "*Reason* : \n"+reasonc+"\n"
	msgc+= "-----------------------------"
	bot.send_message(chat_id=update.message.chat_id, text="Please send screenshot for proof your report...")
	processcmod = False
	sendscreenc = True

@run_async
@pm_only
def reportprocessb(bot, update):
	global processbug
	global sendscreenb
	global msgb
	global userb
	content = "`"+str(update.message.text)+"`"
	user = update.message.from_user
	last_name = user.last_name
	if last_name == None:
		last_name = ''
	user_name = "`"+user.first_name+last_name+"`"
	userb = user_name
	username = update.effective_user.username
	usern = "`"+username+"`"
	msgb = "*BUG REPORT*\n"
	msgb+= "-----------------------------\n"
	msgb+= "*User*   : "+user_name+"\n"
	msgb+= "*Username*: @"+usern+"\n"
	msgb+= "*Reason* : \n"+content+"\n"
	msgb+= "-----------------------------"
	bot.send_message(chat_id=update.message.chat_id, text="Please send screenshot for make bot dev easy to fix it...")
	sendscreenb = True
	processbug = False

@run_async
@pm_only
def sendssg(bot, update):
	global sendscreeng
	global creator
	global tester
	global msgg
	global reportergmod
	global reportergn
	global rep
	global stillr
	global gmoddata

	photos = update.message.photo[-1].file_id
	pprint(update.to_dict())
	user = update.message.from_user
	if user.last_name == None:
		user.last_name = ''
	name = "`"+user.first_name+user.last_name+"`"
	username = update.effective_user.username
	sendscreeng = False
	log = str(update.message.chat_id)
	gmodr = {username:update.message.chat_id}
	gnr = {username:name}
	reportergn.update(gnr)
	reportergmod.update(gmodr)
	del stillr[username]

	bot.send_message(chat_id=update.message.chat_id, text="Your report is done, wait until GMOD accept your report..")
	bot.send_message(chat_id=creator, text=msgg, parse_mode=telegram.ParseMode.MARKDOWN)
	bot.send_photo(chat_id=creator, photo=photos)
	bot.send_message(chat_id=creator, text=log)
	try:
		for test in tester:
			bot.send_message(chat_id=test, text=msgg, parse_mode=telegram.ParseMode.MARKDOWN)
			bot.send_photo(chat_id=test, photo=photos)
	except telegram.TelegramError as e:
		bot.send_message(chat_id=creator, text="Some Tester not pm manually...")
	try:
		for gmod in gmoddata:
			print(gmod)
			bot.send_message(chat_id=gmod, text=msgg, parse_mode=telegram.ParseMode.MARKDOWN)
			bot.send_photo(chat_id=gmod, photo=photos)
		return menu(bot, update)
	except telegram.TelegramError as e:
		print("error: ", e)
		bot.send_message(chat_id=creator, text="Some GMOD not pm manually...")
		return menu(bot, update)

@run_async
@pm_only
def sendssc(bot, update):
	global sendscreenc
	global creator
	global tester
	global msgc
	global reportercmod
	global tagcountry
	global reportercn
	global gmoddata
	global stillr
	global countrycmoddata
	global tagcountry

	photos = update.message.photo[-1].file_id
	pprint(update.to_dict())
	user = update.message.from_user
	if user.last_name == None:
		user.last_name = ''
	name = "`"+user.first_name+user.last_name+"`"
	username = update.effective_user.username
	sendscreenc = False
	cmodr = {username:update.message.chat_id}
	cnr = {username:name}
	reportercn.update(cnr)
	reportercmod.update(cmodr)
	log = str(update.message.chat_id)
	del stillr[username]
	bot.send_message(chat_id=update.message.chat_id, text="Your report is done, wait until CMOD accept your report..")
	bot.send_message(chat_id=creator, text=msgc, parse_mode=telegram.ParseMode.MARKDOWN)
	bot.send_photo(chat_id=creator, photo=photos)
	bot.send_message(chat_id=creator, text=log)
	try:
		for test in tester:
			bot.send_message(chat_id=test, text=msgc, parse_mode=telegram.ParseMode.MARKDOWN)
			bot.send_photo(chat_id=test, photo=photos)
	except telegram.TelegramError as e:
		bot.send_message(chat_id=creator, text="Some Tester not pm manually...")
		return menu(bot, update)
	try:
		for cmod in countrycmoddata[tagcountry]:
			bot.send_message(chat_id=cmod, text=msgc, parse_mode=telegram.ParseMode.MARKDOWN)
			bot.send_photo(chat_id=cmod, photo=photos)
	except telegram.TelegramError as e:
		bot.send_message(chat_id=creator, text="Some CMOD not pm manually...")
		return menu(bot, update)
	try:
		for gmod in gmoddata:
			bot.send_message(chat_id=gmod, text=msgc, parse_mode=telegram.ParseMode.MARKDOWN)
			bot.send_photo(chat_id=gmod, photo=photos)
		return menu(bot, update)
	except telegram.TelegramError as e:
		bot.send_message(chat_id=creator, text="Some GMOD not pm manually...")
		return menu(bot, update)

@run_async
@pm_only
def sendssb(bot, update):
	global sendscreenb
	global creator
	global tester
	global msgb
	global reporterbug
	global reporterbn
	global stillr

	photos = update.message.photo[-1].file_id
	pprint(update.to_dict())
	username = update.effective_user.username
	user = update.message.from_user
	name = "`"+user.first_name+user.last_name+"`"
	sendscreenb = False
	bur = {username:update.message.chat_id}
	log = str(update.message.chat_id)
	bnr = {username:name}
	reporterbn.update(bnr)
	reporterbug.update(bur)
	del stillr[username]
	bot.send_message(chat_id=update.message.chat_id, text="Your report is done, wait until Bot Staff accept your report..")
	bot.send_message(chat_id=creator, text=msgb, parse_mode=telegram.ParseMode.MARKDOWN)
	bot.send_photo(chat_id=creator, photo=photos)
	bot.send_message(chat_id=creator, text=log)
	try:
		for test in tester:
			bot.send_message(chat_id=test, text=msgb , parse_mode=telegram.ParseMode.MARKDOWN)
			bot.send_photo(chat_id=test, photo=photos)
		return menu(bot, update)
	except telegram.TelegramError as e:
		bot.send_message(chat_id=creator, text="Some Tester not pm manually...")
		return menu(bot, update)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@pm_only
def done(bot, update):
	global creator
	global tester
	global clue
	global clie
	global userg
	global userc
	global userb
	global reporterbug
	global reportergmod
	global reportercmod
	global checkbugdone
	global checkgmodadone
	global checkcmoddone
	global gmoddata
	global cmoddata

	user = update.message.from_user
	last_name = user.last_name
	if last_name == None:
		last_name = ''
	first_name = user.first_name+last_name
	iduser = update.effective_user.username
	chatid = str(update.message.chat_id)
	stilld.update({iduser:update.message.chat_id})

	if update.message.chat_id == creator or update.message.chat_id in tester:
		checkbugdone = True
		pesan = "Please insert Reporter's Username..."
		custom_keyboard = [['Cancel']]
		for reporter in reporterbug:
			new = list(reporter)
			t   = ''.join(reporter)
			n   = [t]
			print(n)
			custom_keyboard.append(n)
		print(custom_keyboard)
		reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
		bot.send_message(chat_id=update.message.chat_id, text=pesan, reply_markup=reply_markup)

	if update.message.chat_id != creator:
		if update.message.chat_id in gmoddata:
			checkgmodadone = True
			pesan = "Please Choose kind of reporter.."
			custom_keyboard = [['Gmod Reporter', 'Cmod Reporter']]
			reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
			bot.send_message(chat_id=update.message.chat_id, text=pesan, reply_markup=reply_markup)

		if update.message.chat_id not in gmoddata:
			if update.message.chat_id in cmoddata:
				checkcmoddone = True
				pesan = "Please insert Reporter's Username..."
				custom_keyboard = []
				for reporter in reportercmod:
					new = list(reporter)
					t   = ''.join(reporter)
					n   = [t]
					custom_keyboard.append(n)
				reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
				bot.send_message(chat_id=update.message.chat_id, text=pesan, reply_markup=reply_markup)

			if update.message.chat_id not in cmoddata:
				print("Someone Unauthorized to access command!")

@run_async
@pm_only
def gmodchoose(bot, update):
	global checkgmodadone
	global checkgmoddone
	global reportergmod
	global reportercmod
	global k
	choice = update.message.text

	if choice == "Gmod Reporter":
		checkgmodadone = False
		checkgmoddone = True
		pesan = "Please choose Reporter's Username..."
		custom_keyboard = []
		for reporter in reportergmod:
			new = list(reporter)
			t   = ''.join(reporter)
			n   = [t]
			custom_keyboard.append(n)
		k = 'gmodre'
		reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
		bot.send_message(chat_id=update.message.chat_id, text=pesan, reply_markup=reply_markup)

	elif choice == "Cmod Reporter":
		checkgmodadone = False
		checkgmoddone = True
		pesan = "Please choose Reporter's Username..."
		custom_keyboard = []
		for reporter in reportercmod:
			new = list(reporter)
			t   = ''.join(reporter)
			n   = [t]
			custom_keyboard.append(n)
		k = 'cmodre'
		reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
		bot.send_message(chat_id=update.message.chat_id, text=pesan, reply_markup=reply_markup)

@run_async
@pm_only
def processdone(bot, update):
	global gmoddata
	global cmoddata
	global creator
	global tester
	global userb
	global userg
	global userc
	global reporterbug
	global reportergmod
	global reportercmod
	global checkbugdone
	global checkgmoddone
	global checkcmoddone
	global reporterbn
	global reportergn
	global reportercn
	global k
	global coun

	user = update.message.from_user
	last_name = user.last_name
	usernam = update.effective_user.username
	if last_name == None:
		last_name = ''
	first_name = "`"+user.first_name+last_name+"`"
	del stilld[usernam]
 
	if update.message.chat_id == creator or update.message.chat_id in tester:
		if ' ' in update.message.text or '@' in update.message.text:
			bot.send_message(chat_id=update.message.chat_id, text="Please don't use `@` or space, try again...", parse_mode=telegram.ParseMode.MARKDOWN)
			return menu(bot, update)
		if update.message.text == 'Cancel':
			checkbugdone = False
			bot.send_message(chat_id=update.message.chat_id, text="Go out from accept report...")
			return menu(bot, update)
		userna = str(update.message.text)
		try:
			targetid = reporterbug[userna]
			del reporterbug[userna]
		except KeyError as e:
			update.message.reply_text("Username is invalid or reporter have been accepted, please try again...")
			return done(bot, update)
		reportern = reporterbn[userna]
		del reporterbn[userna]
		checkbugdone = False
		notif = first_name+" accepted report from : "+reportern
		update.message.reply_text("Your accept has been notified to reporter")
		bot.send_message(chat_id=targetid, text="Your report accepted by Bot Staff ("+first_name+")")
		bot.send_message(chat_id=creator, text=notif, parse_mode=telegram.ParseMode.MARKDOWN)
		try:
			for test in tester:
				bot.send_message(chat_id=test, text=notif, parse_mode=telegram.ParseMode.MARKDOWN)
		except telegram.TelegramError as e:
			bot.send_message(chat_id=creator, text="Some testers not pm this bot...")
		finally:
			return menu(bot, update)

	elif update.message.chat_id in gmoddata:
		if k == "gmodre":
			d = reportergmod
			u = reportergn
		elif k == "cmodre":
			d = reportercmod
			u = reportercn
		if ' ' in update.message.text or '@' in update.message.text:
			bot.send_message(chat_id=update.message.chat_id, text="Please don't use `@` or space, try again...", parse_mode=telegram.ParseMode.MARKDOWN)
			return menu(bot, update)
		if update.message.text == 'Cancel':
			checkgmoddone = False
			bot.send_message(chat_id=update.message.chat_id, text="Go out from accept report...")
			return menu(bot, update)
		userna = str(update.message.text)
		try:
			targetid = d[userna]
			print(targetid)
			del d[userna]
		except KeyError as e:
			update.message.reply_text("Username is invalid or reporter have been accepted, please try again...")
			return done(bot, update)
		reportern = u[userna]
		checkgmoddone = False
		notif = first_name+" accepted report from : "+reportern
		print(reportern)
		del reportern
		update.message.reply_text("Your accept has been notified to reporter")
		bot.send_message(chat_id=targetid, text="Your report accepted by GMOD ("+first_name+")")
		bot.send_message(chat_id=creator, text=notif, parse_mode=telegram.ParseMode.MARKDOWN)
		for test in tester:
			bot.send_message(chat_id=test, text=notif, parse_mode=telegram.ParseMode.MARKDOWN)
		try:
			for gmod in gmoddata:
				bot.send_message(chat_id=gmod, text=notif, parse_mode=telegram.ParseMode.MARKDOWN)
			return menu(bot, update)
		except telegram.TelegramError as e:
			bot.send_message(chat_id=creator, text="Some GMOD not pm manually...")
			return menu(bot, update)

	elif update.message.chat_id in cmoddata:
		if ' ' in update.message.text or '@' in update.message.text:
			bot.send_message(chat_id=update.message.chat_id, text="Please don't use `@` or space, try again...", parse_mode=telegram.ParseMode.MARKDOWN)
			return menu(bot, update)
		if update.message.text == 'Cancel':
			checkcmoddone = False
			bot.send_message(chat_id=update.message.chat_id, text="Go out from accept report...")
			return done(bot, update)
		userna = str(update.message.text)
		try:
			targetid = reportercmod[userna]
			del reportercmod[userna]
		except KeyError as e:
			update.message.reply_text("Username is invalid or reporter have been accepted, please try again...")
			return menu(bot, update)
		checkcmoddone = False
		k = None
		notif = first_name+" accepted report from : "+reportercn[userna]
		del reportercn[userna]
		update.message.reply_text("Your accept has been notified to reporter")
		bot.send_message(chat_id=targetid, text="Your report accepted by CMOD ("+first_name+")")
		bot.send_message(chat_id=creator, text=notif, parse_mode=telegram.ParseMode.MARKDOWN)
		for test in tester:
			bot.send_message(chat_id=test, text=notif, parse_mode=telegram.ParseMode.MARKDOWN)
		try:
			for cmod in cmoddata:
				bot.send_message(chat_id=cmod, text=notif, parse_mode=telegram.ParseMode.MARKDOWN)
			return menu(bot, update)
		except telegram.TelegramError as e:
			bot.send_message(chat_id=creator, text="Some CMOD not pm manually...")
			return menu(bot, update)


#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@pm_only
def myid(bot, update):
	yourid = str(update.message.chat_id)

	msg = "Your id is *"+yourid+"*"

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@group_only
def groupid(bot, update):
	grupid = str(update.message.chat_id)

	msg = "Your group id is *"+grupid+"*"

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@pm_only
def howreport(bot, update):
	msg = "*HOW TO REPORT?*\n"
	msg+= "----------------------\n"
	msg+= "1. Tap Report Button.\n"
	msg+= "2. Choose kind of mod (gmod/cmod), you can choose `bug` if you found.\n"
	msg+= "3. type your country tag, like `id`(Indonesia) or `us`(USA)(Skip this if you don't choose CMOD)\n"
	msg+= "4. Type Rules breaker (please don't use space)\n"
	msg+= "5. Type your reason why you report that user\n"
	msg+= "6. Send Screenshot for proof your report\n"
	msg+= "7. Wait until GMOD/CMOD/Bot Staff accept your report\n"
	msg+= "----------------------\n"
	msg+= "You can contact @VrozAnims2003 for more info.."

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
@creator_only
def announ(bot, update, args):
	global tester
	global creator
	global gmoddata
	global cmoddata
	conten = ' '.join(args[0:])
	msg = "     *Announcement*\n"
	msg+= "------------------------------\n"
	msg+= conten+"\n"
	msg+= "------------------------------"
	update.message.reply_text("Your Announcement has been announced!")
	bot.send_message(chat_id=creator, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
	for test in tester:
		bot.send_message(chat_id=test, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
	try:
		for cmod in cmoddata:
			print(update.message.chat_id)
			bot.send_message(chat_id=cmod, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
	except telegram.TelegramError as e:
		bot.send_message(chat_id=creator, text="Some CMODs blocked this bot...")
	try:
		for gmod in gmoddata:
			print(update.message.chat_id)
			bot.send_message(chat_id=gmod, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
	except telegram.TelegramError as e:
		bot.send_message(chat_id=creator, text="Not all Gmod pm report bot...")

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@pm_only
def get_chat(bot, update):
	data = bot.getChat(chat_id=update.message.chat_id)
	pprint(data)

@run_async
@pm_only
def creatorcommand(bot, update):
	msg = "*CREATOR COMMAND*\n"
	msg+= "---------------------------\n"
	msg+= "`/sendm <user> <message>`\n"
	msg+= "`/bann <user>`\n"
	msg+= "`/done <user>`\n"
	msg+= "`/makeb`\n"
	msg+= "`/makec`\n"
	msg+= "`/makecm <country>`\n"
	msg+= "`/addg <user id>`\n"
	msg+= "`/showg`\n"
	msg+= "`/delg <no list>`\n"
	msg+= "`/addc <tag country> <user id>`\n"
	msg+= "`/showc`\n"
	msg+= "`/delc <no list>`\n"
	msg+= "`/getchat`\n"
	msg+= "`/announ <gmod/cmod> <content>`\n"
	msg+= "----------------------------"

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@pm_only
def testercommand(bot, update):
	msg = "*TESTER COMMAND*\n"
	msg+= "--------------------------\n"
	msg+= "*How To Accept Report?*\n"
	msg+= "1.Tap Accept Report button\n"
	msg+= "2.Choose Reporter's Username\n"
	msg+= "in menu.\n"
	msg+= "3.Your accept will be notified\n"
	msg+= "to Reporter\n"
	msg+= "\n"
	msg+= "*Why we use Accept Report?*\n"
	msg+= "because we don't want reporter\n"
	msg+= "still waiting for her/his report.\n"
	msg+= "\n"
	msg+= "--------------------------\n"
	msg+= "`/addg [user id]`-> for adding gmod\n"
	msg+= "`/showg [user id]`-> for look all gmod id\n"
	msg+= "`/delg [gmod list number]`-> remove gmod access\n"
	msg+= "--------------------------" 

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
@pm_only
def gmodcommand(bot, update):
	msg = "*GMOD COMMAND*\n"
	msg+= "--------------------------\n"
	msg+= "*How To Accept Report?*\n"
	msg+= "1.Tap Accept Report button\n"
	msg+= "2.Choose Reporter's Username\n"
	msg+= "in menu.\n"
	msg+= "3.Your accept will be notified\n"
	msg+= "to Reporter\n"
	msg+= "\n"
	msg+= "*Why we use Accept Report?*\n"
	msg+= "because we don't want reporter\n"
	msg+= "still waiting for her/his report.\n"
	msg+= "\n"
	msg+= "--------------------------"

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@pm_only
def cmodcommand(bot, update):
	msg = "*CMOD COMMAND*\n"
	msg+= "--------------------------\n"
	msg+= "*How To Accept Report?*\n"
	msg+= "1.Tap Accept Report button\n"
	msg+= "2.Choose Reporter's Username\n"
	msg+= "in menu.\n"
	msg+= "3.Your accept will be notified\n"
	msg+= "to Reporter\n"
	msg+= "\n"
	msg+= "*Why we use Accept Report?*\n"
	msg+= "because we don't want reporter\n"
	msg+= "still waiting for her/his report.\n"
	msg+= "\n"
	msg+= "--------------------------"

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@pm_only
def usercommand(bot, update):
	 msg = "*USER COMMAND*\n"
	 msg+= "--------------------------\n"
	 msg+= "-> *My ID Command*\n"
	 msg+= "This command for show your ID(PM Only)\n"
	 msg+= "_Command_:\n"
	 msg+= "`/myid`\n"
	 msg+= "\n"
	 msg+= "-> *Group ID Command*\n"
	 msg+= "This command for show your group ID (Group Only)\n"
	 msg+= "_Command_:\n"
	 msg+= "`/groupid`\n"
	 msg+= "\n"
	 msg+= "-> *Rules Command*\n"
	 msg+= "This command for show rules in this bot (Group Only)\n"
	 msg+= "_Command_:\n"
	 msg+= "`/rules`\n"
	 msg+= "\n"
	 msg+= "--------------------------"

	 bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@pm_only
def about(bot, update):
	msg = "*About This Bot*\n"
	msg+= "--------------------------\n"
	msg+= "*Bot Name*   : Hackerz Report\n"
	msg+= "*Bot Version*: "+ScriptVer+"\n"
	msg+= "*Developer*  : @VrozAnims2003\n"
	msg+= "--------------------------"

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@pm_only
def rules(bot, update):
	msg = "*RULE*\n"
	msg+= "--------------------------\n"
	msg+= "-> Don't send fake report\n"
	msg+= "-> Please use your username\n"
	msg+= "-> Don't Spamming\n"
	msg+= "-> Don't use bad word for reason\n"
	msg+= "--------------------------\n"
	msg+= "If you doing this 3 time, you will be banned!\n"
	msg+= "--------------------------\n"
	msg+= "For more info, contact @VrozAnims2003"

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
def rules1(bot, update):
	print("test")
	if update.message.chat_id > 0:
		return
	msg = "*RULE*\n"
	msg+= "--------------------------\n"
	msg+= "-> Don't send fake report\n"
	msg+= "-> Please use your username\n"
	msg+= "-> Don't Spamming\n"
	msg+= "-> Don't use bad word for reason\n"
	msg+= "--------------------------\n"
	msg+= "If you doing this 3 time, you will be banned!\n"
	msg+= "--------------------------\n"
	msg+= "For more info, contact @VrozAnims2003"

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@creator_only
def sendm(bot, update, args):
	userid = int(args[0])
	pesan  = ' '.join(args[1:])

	msg = "*From Developer*\n"
	msg+= "--------------------------\n"
	msg+= "*Message*:\n"
	msg+= pesan+"\n\n"
	msg+= "--------------------------"

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@creator_only
def bann(bot, update, args):
	banbase = sqlite3.connect("ban.db")
	banbase.execute("INSERT INTO BAN (CHATID) VALUES ({});".format(str(args[0])))
	banbase.commit()
	banbase.close()
	notif = "User has been added in banlist.."
	update.message.reply_text(notif)

@run_async
@creator_only
def showban(bot, update):
	banbase = sqlite3.connect("ban.db")
	banlist = banbase.execute("SELECT * FROM BAN")
	woe = "---------------------\n"
	for ban in banlist:
		q = "`"+str(ban[0])+' '+str(ban[1])+"`"
		woe+= q+"\n"
	woe+= "---------------------"
	banbase.close()

	bot.send_message(chat_id=update.message.chat_id, text=woe, parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
@creator_only
def delban(bot, update, args):
	banbase = sqlite3.connect("ban.db")

	bana = str(args[0])
	banbase.execute("DELETE FROM BAN WHERE ID={}".format(bana))
	banbase.commit()
	banbase.close()

	update.message.reply_text("USER HAS BEEN DELETED...")


#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
def addg(bot, update, args):
	global creator, tester

	if update.message.chat_id == creator or update.message.chat_id in tester:
			gmodbase = sqlite3.connect("gmodli.db")

			try:
				gmod = str(args[0])
			except ValueError as e:
				pesan = "Argument is invalid, please check the command.."
				update.message.reply_text(pesan)
				gmodbase.close()
				return

			gmodbase.execute('''INSERT INTO GMOD (CHATID) \
				VALUES ({});'''.format(gmod))

			gmodbase.commit()
			gmodbase.close()
	
			notif = "Success added user as Gmod"
			update.message.reply_text(notif)
			time.sleep(0.2)
			os.execl(sys.executable, sys.executable, *sys.argv)

@run_async
def delg(bot, update, args):
	global creator, tester

	if update.message.chat_id == creator or update.message.chat_id in tester:
			gmodbase = sqlite3.connect("gmodli.db")

			try:
				gmod = int(args[0])
			except ValueError as e:
				pesan = "Argument is invalid, please check the command.."
				update.message.reply_text(pesan)
				gmodbase.close()
				return

			gmodbase.execute("DELETE FROM GMOD WHERE ID={};".format(gmod))
			gmodbase.commit()
			gmodbase.close()
			update.message.reply_text(str(gmod)+" [GMOD] Successfully deleted...")
			time.sleep(0.2)
			os.execl(sys.executable, sys.executable, *sys.argv)

@run_async
def showg(bot, update):
	global creator, tester

	if update.message.chat_id == creator or update.message.chat_id in tester:
			gmodbase = sqlite3.connect("gmodli.db")

			a = gmodbase.execute("SELECT * FROM GMOD;")
			win ="---------------------\n"
			for d in a:
				new = "`"+str(d[0])+' '+d[1]+"`"
				win+= new+"\n"
			win+="---------------------"
			gmodbase.close()

			bot.send_message(chat_id=update.message.chat_id, text=win, parse_mode=telegram.ParseMode.MARKDOWN)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@creator_only
def addc(bot, update, args):
	cmodbase = sqlite3.connect("cmod.db")
	try:
		cmod = int(args[1])
	except ValueError as e:
		pesan = "Argument is invalid, please check the command.."
		update.message.reply_text(pesan)
		return

	cmods = str(cmod)
	country  = str(args[0])

	cmodbase.execute("INSERT INTO CMOD (CHATID, COUNTRY) VALUES ({}, {});".format(cmods, country))
	cmodbase.commit()
	cmodbase.close()

	c = country.upper()

	notif = "Success added user as ["+c+"] Cmod"
	update.message.reply_text(notif)

@run_async
@creator_only
def showc(bot, update):
	cmodbase = sqlite3.connect("cmod.db")

	listcmod = cmodbase.execute("SELECT * FROM CMOD;")

	msg = "------CMOD LIST------\n"
	for cm in listcmod:
		ida = "`"+str(cm[0])+"`"
		chati = "`"+str(cm[1])+"`"
		count = "`"+str(cm[2])+"`"

		msg+= ida+' '+chati+' '+count+"\n"

	msg+= "---------------------"

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
	cmodbase.close()

@run_async
@creator_only
def delc(bot, update, args):
	cmodbase = sqlite3.connect("cmod.db")

	idw = str(args[0])

	cmodbase.execute("DELETE FROM CMOD WHERE ID={};".format(idw))
	cmodbase.commit()
	cmodbase.close()

	update.message.reply_text("CMOD access Successfully removed!")


#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
def main(bot, update):
	global creator
	global resce
	global kindmod
	global countrymod
	global rulebreakerg
	global rulebreakerc
	global processgmod
	global processcmod
	global processbug
	global sendscreeng
	global sendscreenc
	global sendscreenb
	global checkcmoddone
	global checkgmoddone
	global checkbugdone
	global checkgmodadone
	global stillr
	global stilld
	if update.message.chat_id != creator:
		if update.message.chat_id > 0:
			chatid  ="`"+str(update.message.chat_id)+"`"
			user    = update.message.from_user
			first_name = user.first_name
			last_name = user.last_name
			msg = '`'+str(update.message.text)+'`'
			if last_name == None:
				last_name = ''
			name = "`"+first_name+last_name+"`"
			m = chatid+' '+name+' : '+msg
			bot.send_message(chat_id=creator, text=m, parse_mode=telegram.ParseMode.MARKDOWN)

	username = update.effective_user.username

	if update.message.text == "Creator Menu":
		if update.message.chat_id != creator:
			return
		creator_menus(bot, update)

	if update.message.text == "Gmod Menu":
		gmod_menu(bot, update)

	if update.message.text == "Cmod Menu":
		cmod_menu(bot, update)

	if update.message.text == "User Menu":
		user_menu(bot, update)

	if update.message.text == "Back To Creator":
		if update.message.chat_id != creator:
				return
		creator_menu(bot, update)

	if update.message.text == "Back To Tester":
		if update.message.chat_id not in tester:
			return
		tester_menu(bot, update)

	if update.message.text == "How To Report":
		howreport(bot, update)

	if update.message.text == "Creator Command":
		if update.message.chat_id != creator:
			return
		creatorcommand(bot, update)

	if update.message.text == "Tester Menu":
		if update.message.chat_id not in tester:
			return
		tester_menus(bot, update)

	if update.message.text == "Gmod Command":
		gmodcommand(bot, update)

	if update.message.text == "Cmod Command":
		cmodcommand(bot, update)

	if update.message.text == "User Command":
		usercommand(bot, update)

	if update.message.text == "Tester Command":
		if update.message.chat_id not in tester:
			return
		testercommand(bot, update)

	if update.message.text == "About This Bot":
		about(bot, update)
	if update.message.text == "Menu":
		menu(bot, update)
	if update.message.text == "Rules":
		rules(bot, update)
	if update.message.text == "Report":
		report(bot, update)
	if username in stillr:
		if kindmod == True:
			reportbreaker(bot, update)
		if countrymod == True:
			reportcountryc(bot, update)
		if rulebreakerg == True:
			reportreasong(bot, update)
		if rulebreakerc == True:
			reportreasonc(bot, update)
		if processgmod == True:
			reportprocessg(bot, update)
		if processcmod == True:
			reportprocessc(bot, update)
		if processbug == True:
			reportprocessb(bot, update)
	if update.message.text == "Accept Report":
		done(bot, update)
	if username in stilld:
		if checkbugdone == True:
			processdone(bot, update)
		if checkgmoddone == True:
			processdone(bot, update)
		if checkcmoddone == True:
			processdone(bot, update)
		if update.message.text == "rules":
			rules1(bot, update)
		if checkgmodadone == True:
			gmodchoose(bot, update)


#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
def log_command(bot, update):
	userid     = str(update.effective_user.id)
	user       = update.message.from_user
	first_name = str(user.first_name)
	username   = update.effective_user.username
	message    = update.message.text
	loglist	   = open("logclist.txt", 'a')
	isi        = userid+" "+username+" "+first_name+" : "+message+"\n"
	loglist.write(isi)
	loglist.close()

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
def log_text(bot, update):
	userid     = str(update.effective_user.id)
	user       = update.message.from_user
	first_name = str(user.first_name)
	username   = update.effective_user.username
	message    = update.message.text
	loglist    = open("loglist.txt", 'a')
	isi        = userid+" "+username+" "+first_name+" : "+message+"\n"
	loglist.write(isi)
	loglist.close()

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
def photo_report(bot, update):
	global sendscreeng
	global sendscreenc
	global sendscreenb
	global sendscreenalt

	print("a")

	username = update.effective_user.username

	if sendscreenalt == True:
		print("aa")
		sendssalt(bot, update)

	if sendscreeng == True:
		sendssg(bot, update)
	if sendscreenc == True:
		sendssc(bot, update)
	if sendscreenb == True:
		sendssb(bot, update)

#------------------------------------------------------------------------------------------------------------------------------------------

@run_async
@creator_only
def res(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Bot is restarting...")
	time.sleep(0.2)
	os.execl(sys.executable, sys.executable, *sys.argv)

#############################################################################################################################################

try:
	from telegram.ext import CommandHandler
	from telegram.ext import MessageHandler
	from telegram.ext import Filters
except ImportError as e:
	print("Modul error!")
	exit()

#############################################################################################################################################

#Menampung Command

start_handler  = CommandHandler('start', start) #contoh: [nama command]_handler = CommandHandler('[command]', [fungsi command])
myid_handler   = CommandHandler('myid', myid)
groupid_handler= CommandHandler('groupid', groupid)
res_handler	   = CommandHandler('res', res)
sendm_handler  = CommandHandler('sendm', sendm, pass_args=True)
bann_handler   = CommandHandler('bann', bann, pass_args=True)
main_handler   = MessageHandler(Filters.text, main)
addg_handler   = CommandHandler('addg', addg, pass_args=True)
showg_handler  = CommandHandler('showg', showg)
delg_handler   = CommandHandler('delg', delg, pass_args=True)
addc_handler   = CommandHandler('addc', addc, pass_args=True)
showc_handler  = CommandHandler('showc', showc)
delc_handler   = CommandHandler('delc', delc, pass_args=True)
photor_handler = MessageHandler(Filters.photo, photo_report)
announ_handler = CommandHandler('announ', announ, pass_args=True)
get_chat_handler = CommandHandler('getchat', get_chat)
reportalt_handler= CommandHandler('report', reportalt, pass_args=True)
showban_handler = CommandHandler('showban', showban)
delban_handler  = CommandHandler('delban', delban, pass_args=True)

#############################################################################################################################################

#Menampung Semua Variabel Command dan ditangani oleh dispatcher
dispatcher.add_handler(start_handler)#contoh -> dispatcher.add_handler([variable handler])
dispatcher.add_handler(myid_handler)
dispatcher.add_handler(groupid_handler)
dispatcher.add_handler(res_handler)
dispatcher.add_handler(sendm_handler)
dispatcher.add_handler(bann_handler)
dispatcher.add_handler(main_handler)
dispatcher.add_handler(addg_handler)
dispatcher.add_handler(addc_handler)
dispatcher.add_handler(photor_handler)
dispatcher.add_handler(announ_handler)
dispatcher.add_handler(get_chat_handler)
dispatcher.add_handler(reportalt_handler)
dispatcher.add_handler(showg_handler)
dispatcher.add_handler(delg_handler)
dispatcher.add_handler(showban_handler)
dispatcher.add_handler(delban_handler)
dispatcher.add_handler(showc_handler)
dispatcher.add_handler(delc_handler)

#############################################################################################################################################

#Memulai Polling

updater.idle() #untuk menjalankan webhook(heroku)

#############################################################################################################################################
