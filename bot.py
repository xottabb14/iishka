#-*- coding: utf-8 -*-
#тело бота

import config #Подключаем свой конфиг (там токен)
import regularfrazes
import goroskop
import telebot #Подключаем апи телеграма
#from telebot import apihelper
from random import random, randrange
import re #модуль с поиском в файле
import time
import os
from os import path
import datetime
import subprocess
import requests
import json
import sys
#import shutil
from telebot import types
from multiprocessing import Process
from func import get_html
from iishkaAI import gpt_message

os.chdir('/opt/iishka')

#ПЕРЕМЕННЫЕ
bot = telebot.TeleBot(config.token) #прописываем токен из конфига
chat_idwork = config.chat_idwork
test_chat = config.test_chat
user_admin = config.user_admin

temp_file = config.temp_file #временный файл
wordsfile = config.wordsfile #файл с базой ответов
helpfile = config.helpfile #файл с базой ответов
vusersm = config.vusersm #список пидоров
vusersw = config.vusersw #список тпшек
firstfraze = config.firstfraze #первая фраза бота-пидотп
secondfraze = config.secondfraze #вторая фраза бота-пидотп
thirdfraze = config.thirdfraze #третьяфраза бота-пидотп
pidofraze = config.pidofraze #пидор фраза бота-пидотп
tpshfraze = config.tpshfraze #тп фраза бота-пидотп
alkash = config.alkash #имя алкаша в файле
alkashfr = config.alkashfr #фразы для алкаша
listdaupid = config.listdaupid #текущий пидар
listdautp = config.listdautp #текущая ТП
listpolz = config.listpolz #отметка времени с прошлой рулетки
helppidtp = config.helppidtp #хелп пидотпбота
rouletteus = config.rouletteus #список юзеров рулетки
shmappc = config.shmappc #фразы убийцы шмы
shmaotvet = config.shmaotvet #фразы для троллинга шмы
privetnew = config.privetnew #fo privet
xuutro = config.xuutro #no comments
#время
meeteng_io_meet=""

#____________________вспомогательные функции_______________

def rulles(message): #проверка. Есть ли ID админов в message
	rule = False
	for admin in config.admin_list:
		try:
			if admin in str(message.from_user.id):
				rule = True
				break
			else:
				pass
		except:
			pass
	return rule

def modrulles(message): #проверка. Есть ли ID модеров в message
	rule = False
	for moder in config.moder_list:
		try:
			if moder in str(message.from_user.id):
				rule = True
				break
			else:
				pass
		except:
			pass
	return rule

def kalicalls(message): #Вызов Кали в чат 
	pass


def memasik(message): #парсинг мема и отправка в чат
	url = 'https://www.anekdot.ru/random/mem/'
	try:
		text_p = get_html(url) #получаем html текст
		mem_data = str(text_p.split("https://www.anekdot.ru/i/caricatures/normal/")[1].split('.jpg')[0])
		url_mem = "https://www.anekdot.ru/i/caricatures/normal/"+mem_data+'.jpg'
		#print(url_mem)
		bot.send_photo(message.chat.id,url_mem)
	except Exception as e:
		print (e)


def covidget(covid_chat_id,main_str): #вывод статистики ковид по запросу
	try:
		covid_cur = readlistfile("cur_covid.ii")
		conf_plus_list = readlistfile("plus_covid.ii")
		str_covid = main_str+"\n\n😷Заболело: *"+str(covid_cur[0].replace('\n',''))+"* чел.(+"+str(conf_plus_list[0].replace('\n',''))+" чел.)\n👍Выздоровело: *"+str(covid_cur[1].replace('\n',''))+"* чел.(+"+str(conf_plus_list[1].replace('\n',''))+" чел.)\n🦠Умерло: *"+str(covid_cur[2].replace('\n',''))+"* чел.(+"+str(conf_plus_list[2].replace('\n',''))+" чел.)\n\n`Берегите себя!❤️`\n"+config.str_covidparty
		bot.send_sticker(covid_chat_id,'CAACAgIAAx0CSiOOwwACB4hfs-3i3TRVN8a0H6a3zHSWtnqnbwACXAADVSx4C01PSHLmRFaqHgQ')
		bot.send_message(covid_chat_id,str_covid,parse_mode="Markdown")
	except Exception as e:
		print (e)
		bot.send_message(covid_chat_id,"Не удалось получить данные по COVID-19...")

def covid(covid_chat_id,main_str): #парсинг статистики ковид и вывод (ежедневно)
	url = 'https://www.newkaliningrad.ru/'
	try:
		text_p = get_html(url) #получаем html текст
		confirum = str(text_p.split("<span class=\"confirm\" style=\"color: #ffa337;\">&#8226;</span>")[1].split('<span class')[0]).replace(' ','').replace('\n','')
		recover = str(text_p.split("<span class=\"recover\" style=\"color: #03c8a4;\">&#8226;</span>")[1].split('<span class')[0]).replace(' ','').replace('\n','')
		deaths = str(text_p.split("<span class=\"death\" style=\"color: #cd0712;\">&#8226;</span>")[1].split('</a>')[0]).replace(' ','').replace('\n','')
		covid_cur = readlistfile("cur_covid.ii")
		conf_plus_list = readlistfile("plus_covid.ii")

		confirum_plus = int(confirum) - int(covid_cur[0].replace('\n',''))
		confirum_plus = str(confirum_plus)

		recover_plus = int(recover) - int(covid_cur[1].replace('\n',''))
		recover_plus = str(recover_plus)

		deaths_plus = int(deaths) - int(covid_cur[2].replace('\n',''))
		deaths_plus = str(deaths_plus)


		data_plus = confirum_plus+'\n'+recover_plus+'\n'+deaths_plus
		rewritetofile("plus_covid.ii",data_plus)
		
		str_covid = main_str+"\n\n😷Заболело: *"+confirum+"* чел.(+"+confirum_plus+" чел.)\n👍Выздоровело: *"+recover+"* чел.(+"+recover_plus+" чел.)\n🦠Умерло: *"+deaths+"* чел.(+"+deaths_plus+" чел.)\n\n`Берегите себя!❤️`\n"+config.str_covidparty
		f_data = confirum+'\n'+recover+'\n'+deaths
		rewritetofile("cur_covid.ii",f_data)
		bot.send_sticker(covid_chat_id,'CAACAgIAAx0CSiOOwwACB4hfs-3i3TRVN8a0H6a3zHSWtnqnbwACXAADVSx4C01PSHLmRFaqHgQ')
		bot.send_message(covid_chat_id,str_covid,parse_mode="Markdown")
	except Exception as e:
		print (e)
		bot.send_message(covid_chat_id,"Не удалось получить данные по COVID-19...")

def any_get_all(url_any): #любой get-запрос
	response = requests.get(url_any)
	response.encoding = 'utf-8'
	val_brigh = response.text
	return val_brigh

def writetofile(f_name,f_data): #дозапись в конец файла
	w_f = open(f_name, "a", encoding = "utf-8") #открываем файл в режиме перезаписи
	w_f.write(f_data)
	w_f.close() #закрываем файл

def rewritetofile(f_name,f_data): #перезапись файла
	w_f = open(f_name, "w+", encoding = "utf-8") #открываем файл в режиме перезаписи
	w_f.write(f_data)
	w_f.close() #закрываем файл

def readlistfile(f_name): #чтение файла в виде списка
	w_f = open(f_name, "r", encoding = "utf-8") #открываем файл в режиме перезаписи
	listfw = list(w_f)
	w_f.close() #закрываем файл
	return listfw

def readfile(f_name): #чтение файла в виде текста
	w_f = open(f_name, "r", encoding = "utf-8") #открываем файл в режиме перезаписи
	listfw = w_f.read()
	w_f.close() #закрываем файл
	return listfw

def logging(ErType,ErStr): #логгирование в файл
	log_f = open('logII.txt', "a", encoding = "utf-8") #открываем файл в режиме перезаписи
	now_time = time.time()+21600#текущее время в сек
	log_time = time.ctime(now_time) #текущее время в нормальном виде
	log_str = str(log_time)+"  "+ErType+"  "+str(ErStr)+"\n"
	log_f.write(log_str)
	log_f.close() #закрываем файл

def get_html(url): #получение кода html страницы в виде текста
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
	r = requests.get(url,headers = headers)	# Получаем метод Response
	r.encoding = 'utf8'	  #'cp1251'# У меня были проблемы с кодировкой, я задал в ручную
	return str(r.text)			# Вернем данные объекта text 

#функция зачистки строки от символов препинания
def clean_text (text):
			if not isinstance(text, str):
				raise TypeError('Это не текст')
			for i in [',', '.', ':', ';', '!', '?']:
				text = text.replace(i,'')
			return text

#функция зачистки строки от символов препинания, включая Enter
def clean_textn (text):
			if not isinstance(text, str):
				raise TypeError('Это не текст')
			for i in [',', '.', ':', ';', '!', '?','\n']:#,'(',')'
				text = text.replace(i,'')
			return text

#очищаем начальную фразу от ошибочных символов
def clean_tostart (text):
			if not isinstance(text, str):
				raise TypeError('Это не текст')
			for i in ['(',')','?','^','*','=',':']:
				text = text.replace(i,'')
			return text

#очищает только от enter
def clean_enter (text):
			if not isinstance(text, str):
				raise TypeError('Это не текст')
			for i in ['\n']:
				text = text.replace(i,'')
			return text

#очищает только от иишки
def clean_iishka (text):
			if not isinstance(text, str):
				raise TypeError('Это не текст')
			for i in ['Иишка ','ИИшка ','иишка ',' Иишка ',' ИИшка ',' иишка ','Иишка, ','ИИшка, ','иишка, ','Иишка. ','ИИшка. ','иишка. ',' Иишка. ',' ИИшка. ',' иишка. ']:
				text = text.replace(i,'')
			return text

#очищает только от --namename--
def clean_namename (text,nametext):
			if not isinstance(text, str):
				raise TypeError('Это не текст')
			for i in ['--namename--']:
				text = text.replace(i,nametext)
			return text

#очищает только от #
def clean_resh (text):
			if not isinstance(text, str):
				raise TypeError('Это не текст')
			for i in ['#']:
				text = text.replace(i,'')
			return text
#очищает только от запятых и апострофов
def clean_qvadr (text):
			if not isinstance(text, str):
				raise TypeError('Это не текст')
			for i in ['[',']','\'']:
				text = text.replace(i,'')
			return text

#записываем строку в temp-файл
def temp_fw(t_string):
	f = open(temp_file, "w+", encoding = "utf-8") #открываем файл в режиме перезаписи
	temp_string = f.write(t_string)
	f.close() #закрываем файл

#читаем строку из temp-файла
def temp_fr():
	f = open(temp_file, "r", encoding = "utf-8") #открываем файл в режиме чтения
	temp_string = f.read()
	f.close() #закрываем файл
	return temp_string

#записываем строку в known-файл
def known_fw(t_string,knw_fn):
	f = open(knw_fn, "w+", encoding = "utf-8") #открываем файл в режиме перезаписи
	temp_string = f.write(t_string)
	f.close() #закрываем файл

#читаем строку из known-файла
def known_fr(knw_fn):
	f = open(knw_fn, "r", encoding = "utf-8") #открываем файл в режиме чтения
	temp_string = f.read()
	f.close() #закрываем файл
	return temp_string

#Проверяем, введено число или текст
def isint(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

#функция приведения сообщения пользователя к нижнему регистру, без знаков препинания и с переносом строки после фразы
def spl_clean(message):
	spl_all = message+'\n'
	spl = str.lower(spl_all)
	spl = clean_textn(spl)
	return spl

#функция приведения фразы из базы к нижнему регистру, без знаков препинания для сравнения
def w_clean(w):
	low_w = str.lower(w) #переводим все строки из файла в нижний регистр для проверки
	loww_w = clean_textn(low_w)
	return loww_w

#функция удаления и замены определенной строки
def del_str(str_ing,simvol): #удаляем последнюю строку, когда записи ответа не последовало
	words_file = open(wordsfile, "r", encoding = "utf-8") #открываем файл в режиме добавления в конец файла
	file_string = words_file.read()
	words_file.close() #закрываем файл

	file_string = (re.sub(('\n'+str_ing), simvol, file_string)) #если что то тут убрать \n file_string = (re.sub(('\n'+str_ing), "\n", file_string))

	words_file = open(wordsfile, "w", encoding = "utf-8") #открываем файл в режиме добавления в конец файла
	file_string = words_file.write(file_string)
	words_file.close() #закрываем файл

#функция удаления через темп
def del_strS(str_ing,simvol): #удаляем последнюю строку, когда записи ответа не последовало
	f = open(wordsfile,'r', encoding = "utf-8")
	o = open(temp_file,'w+', encoding = "utf-8")
	while 1:
	  line = f.readline()
	  if not line: break
	  str_ing = clean_enter(str_ing)+'\n'
	  line = line.replace(str_ing,simvol)
	  o.write(line)
	o.close()
	f.close()

#перезаписываем из темпа в исходный файл
def rewrite_ft(): #удаляем последнюю строку, когда записи ответа не последовало
	f = open(temp_file,'r', encoding = "utf-8")
	text = f.read()
	f.close()
	o = open(wordsfile,'w+', encoding = "utf-8")
	o.write(text)
	o.close()

def goroskop_find(message): #отправка гороскопа
	if '!овен' in message.text.lower():
		horo_str = goroskop.aries
	elif '!телец' in message.text.lower():
		horo_str = goroskop.little_bodies
	elif '!близнец' in message.text.lower():
		horo_str = goroskop.twins
	elif '!рак' in message.text.lower():
		horo_str = goroskop.cancer
	elif '!лев' in message.text.lower():
		horo_str = goroskop.lion
	elif '!дев' in message.text.lower():
		horo_str = goroskop.maiden
	elif '!весы' in message.text.lower():
		horo_str = goroskop.scales
	elif '!скорпион' in message.text.lower():
		horo_str = goroskop.scorpion
	elif '!стрелец' in message.text.lower():
		horo_str = goroskop.sagittarius
	elif '!козерог' in message.text.lower():
		horo_str = goroskop.capricorn
	elif '!водоле' in message.text.lower():
		horo_str = goroskop.aquarius
	elif '!рыбы' in message.text.lower():
		horo_str = goroskop.fishes
	elif '!толерантный гороскоп' in message.text.lower():
		horo_str = readfile('tolgoroskop.txt')
	else:
		pass
	bot.send_message(message.chat.id,horo_str,parse_mode="Markdown")


#____________________________________Конец вспомогательных функций___________________________________


#____________________________________Команды бота_________________________________
#обработчик команды Start
@bot.message_handler(commands=['start'])
def handle_start(message):
	i = randrange(0,5)
	if i == 0:
		bot.send_message(message.chat.id, 'Да, да я на связи^^')
	elif i == 1:
		bot.send_message(message.chat.id, 'Вы что то хотели?')
	elif i == 2:
		bot.send_message(message.chat.id, 'Я всегда рядом и молчаливо слежу за вами))')
	elif i == 3:
		bot.send_message(message.chat.id, 'Вы меня звали?')
	elif i == 4:
		bot.send_message(message.chat.id, 'О, про меня вспомнили) Какая милота^^')
	else:
		pass

#вставляем по команде гифу
@bot.message_handler(commands=['kldgif'])
def handle_kldgif(message):
	bot.send_animation(message.chat.id,'BQACAgIAAxkBAAJlhF_jpdlutPJxspqoCIlhan_WgpKKAAIUCAAC6M4gS_k_eWC2OeGOHgQ')
	bot.send_message(message.chat.id,'¯\_(ツ)_/¯')

#вставляем по команде смайлик
@bot.message_handler(commands=['shrug'])
def handle_shrug(message):
	bot.send_message(message.chat.id,'¯\_(ツ)_/¯')

#вставляем по команде смайлик
@bot.message_handler(commands=['song'])
def handle_song(message): #парсинг моего плейлиста и последнюю песню в чат
	url = 'https://music.yandex.ru/users/vkeduardyo/playlists/3'
	try:
		text_p = get_html(url) #получаем html текст
		json_mus = str(text_p.split("\"track\":")[1].split(']')[0])+"]"
		json_list = json.loads(json_mus)
		last_song = "Песенка от Xottabb14😏:\n"+str(json_list[0]["name"])+"\n"+str(json_list[0]["url"])
		bot.send_message(chat_idwork,last_song)
	except:
		bot.send_message(message.chat.id,'Отправка не удалась(')

#задаем количество секунд таймера обучения
@bot.message_handler(commands=['timer'])
def handle_timer(message):
	send = bot.send_message(message.chat.id,'Ведите количество секунд числом от 5 до 60 сек.:')
	bot.register_next_step_handler(send, write_timer) #слушаем фразу для для таймера

#команда вставки фразы
@bot.message_handler(commands=['insert'])
def handle_insert(message):
	send = bot.send_message(message.chat.id,'Введите фразу, для которой требуется добавить вариант ответа:')
	bot.register_next_step_handler(send, insertf) #слушаем фразу для замены

#команда замены фразы
@bot.message_handler(commands=['replace'])
def handle_replace(message):
	send = bot.send_message(message.chat.id,'Введите или скопируйте точную фразу для изменения ее в базе:')
	bot.register_next_step_handler(send, replacef) #слушаем фразу для замены

#команда удаления фразы
@bot.message_handler(commands=['del'])
def handle_del(message):
	send = bot.send_message(message.chat.id,'Введите или скопируйте точную фразу для удаления:')
	bot.register_next_step_handler(send, del_fraze) #слушаем фразу для удаления

#Обработчик команды Info
@bot.message_handler(commands=['help'])
def handle_help(message):
	f = open(helpfile, "r", encoding = "utf-8") #открываем файл в режиме чтения
	help_string = f.read()
	f.close() #закрываем файл
	bot.send_message(message.chat.id,help_string)
	f = open(helppidtp, "r", encoding = "utf-8") #открываем файл в режиме чтения
	helppt_string = f.read()
	f.close() #закрываем файл
	bot.send_message(message.chat.id,helppt_string)

#вывод raw сообщения
@bot.message_handler(commands=['rawmessage'])
def handle_rawmessage(message):
	mymess = str(message)
	bot.send_message(message.chat.id,mymess)
#raw в файл
@bot.message_handler(commands=['rawsave'])
def handle_rawsave(message):
	f = open('rawsave.ii', "w+", encoding = "utf-8") #открываем файл в режиме перезаписи
	f.write(str(message))
	f.close() #закрываем файл
	f_raw = open('rawsave.ii',"r", encoding = "utf-8")
	bot.send_document(message.chat.id, f_raw)
	f_raw.close()
	bot.send_message(message.chat.id,"Данные выгружены...")

#выводим рейтинг чата
@bot.message_handler(commands=['rating'])
def handle_allrating(message):
	lvlfile = open('reiting.ii', "r", encoding = "utf-8") #открываем файл в режиме чтения
	lvllist = list(lvlfile)
	lvlfile.close()
	numrow = 0
	textlvls = "🤘Рейтинг пользователей чата:🤘\n>>>>>>>>>\n"
	num = 0
	for i in lvllist:
		ii = clean_enter(i)
		if numrow % 2 == 0:
			num=num+1
			lvl_znach = clean_enter(lvllist[numrow+1])
			textlvls = textlvls+str(num)+". "+str(ii)+" ----- ("+lvl_znach+")\n"
		numrow = numrow+1
	textlvls = textlvls+">>>>>>>>>"
	bot.send_message(message.chat.id, textlvls)

#запрашиваем айди чата
@bot.message_handler(commands=['idchat'])
def handle_idchat(message):
	f = open('tempid.ii','w+', encoding = "utf-8")#vusersm
	idchat = str(message.chat.id)
	f.write(idchat)
	f.close()
	bot.send_message(message.chat.id, idchat)

#вообще хз что это
@bot.message_handler(commands=['onemessage'])
def handle_onemessage(message):
	mymess = str(bot.parse_entitys)
	bot.send_message(message.chat.id,mymess)

#создать ощибку в работе бота
@bot.message_handler(commands=['errortest'])
def handle_errortest(message):
	x = 2
	y = x/0
	bot.send_message(message.chat.id,'Вроде не упал^^ Но это не точно XD')

#pin сообщения
@bot.message_handler(commands=['pin'])
def handle_pinmessage(message):
	if rulles(message) == True:
			try:
				bot.pin_chat_message(message.chat.id,message.reply_to_message.message_id)
			except Exception as e:
				print("ExceptionpinError:", e)
				logging("ERROR_PIN",e)
				bot.send_message(message.chat.id,'`Хуеpin`🤦‍♂️',parse_mode="Markdown")
	else:
		bot.send_message(message.chat.id,'@pipinsorry?',parse_mode="Markdown")

#unpin сообщения
@bot.message_handler(commands=['unpin'])
def handle_unpinmessage(message):
	meeterid = known_fr('meeter.ii')
	if rulles(message) == True:
		try:
			bot.unpin_chat_message(message.chat.id)
		except Exception as e:
			print("ExceptionUnpinError:", e)
			logging("ERROR_UNPIN",e)
			bot.send_message(message.chat.id,'`Нечего UNPINить`🤦‍♂️',parse_mode="Markdown")
	elif meeterid in str(message.from_user.id):
		try:
			bot.unpin_chat_message(message.chat.id)
		except Exception as e:
			print("ExceptionUnpinError2:", e)
			logging("ERROR_UNPIN_2",e)
			bot.send_message(message.chat.id,'`Нечего UNPINить`🤦‍♂️',parse_mode="Markdown")

	else:
		bot.send_message(message.chat.id,'Ага, сейчас. Наивное существо...🤦‍♂️')


@bot.message_handler(commands=['ruleskld'])
def handle_ruleskld(message):
	f = open('ruleskld.ii', "r", encoding = "utf-8") #открываем файл в режиме чтения
	help_string = f.read()
	f.close() #закрываем файл
	bot.send_message(message.chat.id,help_string,reply_to_message_id=message.message_id)


#____________________________________Конец команд бота_________________________________


#____________________________________ОСНОВНЫЕ ФУНКЦИИ БОТА________________________________________
#функция добавления ответа для фразы
def insertf(message):
	words_file = open(wordsfile, "r", encoding = "utf-8") #открываем файл в режиме чтения
	file_string = list(words_file)
	words_file.close()
	spl = spl_clean(message.text)
	spl = clean_tostart (spl)
	spl = '#'+spl
	for w in file_string:
		io=0
		lw = w_clean(w)
		if spl == lw:
			io=0
			temp_fw (w)
			sendd = bot.send_message(message.chat.id,'Я знаю такую фразу. Введите фразу-ответ:')
			bot.register_next_step_handler(sendd, ins_fraze) #слушаем фразу для удаления
			break
		else:
			io=1
	if io ==1:
		bot.send_message(message.chat.id,'К сожалению, такой фразы нет в моей базе. Вы можете научить меня, отправив мне эту фразу в разговоре.')
		io=0
	else:
		pass

#функция "склеивания" сохраненной фразы с добавленной пользователем фразой
def ins_fraze(message):
	str_ing = temp_fr()
	if str(message.content_type) != 'document':
		try:
			repl_clean = message.text#clean_skob (message.text)
			rep_str = str_ing+repl_clean+'\n'
			del_strS(str_ing,rep_str)
			rewrite_ft()
			bot.send_message(message.chat.id,'Фраза-ответ добавлена!')
		except:
			pass
	else:
		try:
			repl_clean = 'its_document_id---'+str(message.document.file_id)
			rep_str = str_ing+repl_clean+'\n'
			del_strS(str_ing,rep_str)
			rewrite_ft()
			bot.send_message(message.chat.id,'Гифка-ответ добавлена!')
		except:
			pass

#функция замены фразы в файле базы ответов
def replacef(message):
	words_file = open(wordsfile, "r", encoding = "utf-8") #открываем файл в режиме чтения
	file_string = list(words_file)
	words_file.close()
	spl = spl_clean(message.text)
	for w in file_string:
		io=0
		lw = w_clean(w)
		if spl == lw:
			io=0
			temp_fw(w)
			sendd = bot.send_message(message.chat.id,'Введите фразу для замены:')
			bot.register_next_step_handler(sendd, re_fraze) #слушаем фразу для замены
			break
		else:
			io=1
	if io ==1:
		bot.send_message(message.chat.id,'К сожалению, такой фразы нет в моей базе ответов.')
		io=0
	else:
		pass

#функция замены указанной пользователем фразы
def re_fraze(message):
	repl_clean = message.text#clean_skob (message.text)
	rep_str = repl_clean+'\n' #'\n'+
	str_ing = temp_fr()
	del_strS(str_ing,rep_str)
	rewrite_ft()
	bot.send_message(message.chat.id,'Фраза изменена!')

#функция удаления фразы из базы ответов
def del_fraze(message):
	words_file = open(wordsfile, "r", encoding = "utf-8") #открываем файл в режиме добавления в конец файла
	file_string = list(words_file)
	words_file.close()
	spl = spl_clean(message.text)
	for w in file_string:
		io=0
		lw = w_clean(w)
		if spl == lw:
			io=0
			if w != '-end-':
				del_strS (w,'') #(message.text)
				rewrite_ft()
				bot.send_message(message.chat.id,'Фраза удалена!')
			else:
				pass
			break
		else:
			io=1
	if io ==1:
		bot.send_message(message.chat.id,'К сожалению, такой фразы нет в моей базе ответов.')
		io=0
	else:
		pass

#______________________________ТАЙМЕР_______________________
#функция изменения значения таймера
def write_timer(message): #меняем время таймера
	e = isint(message.text) #проверяем, число ли?
	if e == True:
		d = int(message.text)
		a = 0
		b = 0
		c = 0
		if d < 61: #Проверяем, находится ли введенное значение в диапазоне от 5 до 60 сек
			a=1
		else:
			pass
		if d > 4:
			b = 2
		else:
			pass
		c = a+b
		if c == 3: #если диапазон верный - записываем значение в файл
			timer_file = open("timer.ii", "w+", encoding = "utf-8")
			timer_file.write(message.text)
			timer_file.close()
			time_s = "Время изменено: "+message.text
			bot.send_message(message.chat.id, time_s)
		else:
			bot.send_message(message.chat.id, 'Вы указали время неправильно. Попробуйте снова...')
	else:
		bot.send_message(message.chat.id, "Вы ввели текст, не обманывайте меня!")

#читаем значение таймера из файла
def t_timer():
	words_file = open("timer.ii", "r", encoding = "utf-8") #открываем файл в режиме чтения
	file_string = words_file.read()
	words_file.close() #закрываем файл
	return file_string
#_________________________________Конец ТАЙМЕРА______________________


#_______________________________________________РАЗГОВОРНЫЕ ФУНКЦИИ_______________________________
#функция добавления ответа в базу ответов бота
def add_ans(message):
	ss = len(re.findall(r"[\n']+?", open(wordsfile, "r", encoding = "utf-8").read())) #количество строк в начале обработки файла
	words_file = open(wordsfile, "a", encoding = "utf-8") #открываем файл в режиме добавления в конец файла
	cl_message = clean_iishka (message.text)
	start_fraze = clean_tostart ('\n'+'#'+cl_message)#
	words_file.write(start_fraze)#записываем в файл стартовую фразу ('\n'+'#'+message.text)#
	words_file.close() #закрываем файл
	t_str = t_timer()
	sent = bot.send_message(message.chat.id, 'Итак, слушаю в течение ' +t_str+' сек. Потом я все забуду!^^. (Или введи "ОТМЕНА"):')
	bot.register_next_step_handler(sent, obrab) #слушаем фразу для ответа
	time.sleep(int(t_str)) #таймер
	bot.clear_step_handler(sent) #отмена после таймера
	s = len(re.findall(r"[\n']+?", open(wordsfile, "r", encoding = "utf-8").read())) #количество строк в конце обработки файла
	if s == ss+1:
		mess_clean = '#'+cl_message
		messa_clean = clean_tostart(mess_clean)
		del_str (messa_clean,'')#('#'+message.text,'')
	else:
		pass

# функция записи ответа на фразу в файл
def obrab(message):
	#print(str(message))
	if str(message.content_type) != 'document':
		try:
			can_cel = str.lower(message.text)
			if can_cel != 'отмена':
				words_file = open(wordsfile, "a", encoding = "utf-8")
				messs_clean = clean_iishka(message.text) #clean_skob ()
				obrab_ans = '\n'+messs_clean+'\n'
				words_file.write(obrab_ans)#записываем ответ на фразу
				words_file.write('-end-')#ставим индикатор конца списка в файле
				words_file.close()
				bot.send_message(message.chat.id, 'Хорошо, я запомню^^')
			else:
				bot.send_message(message.chat.id, 'ОК! Забыли^^')
		except:
			pass
	else:
		try:
			can_cel = str(message.document.file_id)
			if can_cel != 'отмена':
				words_file = open(wordsfile, "a", encoding = "utf-8")
				obrab_ans = '\n'+'its_document_id---'+can_cel+'\n'
				words_file.write(obrab_ans)#записываем ответ на фразу
				words_file.write('-end-')#ставим индикатор конца списка в файле
				words_file.close()
				bot.send_message(message.chat.id, 'Хорошо, я запомню^^')
			else:
				bot.send_message(message.chat.id, 'ОК! Забыли^^')
		except:
			pass

def word_list(message):
	words_file = open(wordsfile, "r", encoding = "utf-8")
	com_and = list(words_file)
	n=0
	spl_all = clean_iishka (message.text)
	spl_all = spl_all +'\n'
	spl = str.lower(spl_all)
	spl = clean_text(spl)
	spl = clean_tostart (spl)
	spl = '#'+spl #помечаем главную фразу!!!!!!!!!!!!!!
	for w in com_and: #перебираем все ответы в полном списке
		io = 0 #если 0 то ищем ответ
		low_w = str.lower(w) #str.lower #переводим все строки из файла в нижний регистр для проверки
		loww_w = clean_text(low_w)
		if spl == loww_w: #если сообщение совпадает с ответами в базе
			spl_s = com_and[n:len(com_and)] #режем список от текущей строки до конца списка
			i = 0
			end_ans = ('-end-\n')
			for ww in spl_s:
				if ww == end_ans: #перебираем ответы оставшегося списка, чтобы найти его конец
					break
				else:
					pass
				i += 1
			nn = n+1
			ii = n+i-1
			if nn < ii: #!если не так, то ранг рандома будет равен минусу или нулю
				answer = randrange(nn, ii) #задаем индекс ответа от следующего эелемента после совпадения до строки -end-
				if 'its_document_id---' in com_and[answer]:
					gif_str_id = com_and[answer].replace('its_document_id---','').replace('\n','')
					bot.send_animation(message.chat.id,gif_str_id)
				else:
					bot.send_message(message.chat.id, com_and[answer],reply_to_message_id=message.message_id)
				words_file.close() #закрываем файл
				break
			elif nn == ii:
				answer = ii #задаем индекс ответа от следующего эелемента после совпадения до строки -end-
				if 'its_document_id---' in com_and[answer]:
					gif_str_id = com_and[answer].replace('its_document_id---','').replace('\n','')
					bot.send_animation(message.chat.id,gif_str_id)
				else:
					bot.send_message(message.chat.id, com_and[answer],reply_to_message_id=message.message_id)
				words_file.close() #закрываем файл
				break
			else:
				pass
		else:
			io = 1 #если 1 то говорим, что ответа нет
		n += 1

	if io == 1:
		'''not_ans = (message.from_user.first_name+', в моей базе нет ответа. Вы можете его добавить. Для этого напишите мне точную фразу, которой я должен был Вам ответить.')#message.from_user.first_name - вывод первого имени пользователя в телеграме
		bot.send_message(message.chat.id, not_ans)
		add_ans(message) #добавляем функцию базы
 		'''
		message_text = gpt_message(message.text)
		bot.send_message(message.chat.id,message_text,reply_to_message_id=message.message_id)
		io=0
	else:
		pass
	words_file.close()

#_____________________________________________ПИДО-ТП-БОТ_________________________________________________________
#функция проврки пользователя в базе
def sex_all(message):
	sex = 0
	sexw = 0
	f = open(vusersm,'r', encoding = "utf-8")#vusersm
	spisokp = list(f)
	f.close()
	#ff = str(spisokp)
	#bot.send_message(message.chat.id,sex)
	name = message.from_user.username+"\n"
	for w in spisokp:
		if w==name:
			bot.send_message(message.chat.id,'Вы зарегистрированны в списке потенциальных ПИДОРОВ!')
			sex = 0
			break
		else:
			sex = 1
	f = open(vusersw,'r', encoding = "utf-8")#vusersm
	spisokp = list(f)
	f.close()
	name = message.from_user.username+'\n'
	for w in spisokp:
		if w==name:
			bot.send_message(message.chat.id,'Вы зарегистрированны в списке потенциальных ТПШЕК!')
			sexw = 0
			break
		else:
			sexw = 1
	sex_all = sex+sexw
	return sex_all


#Обработчик команды regrull - регистрация в рулетке (виртуальная клавиатура)
@bot.message_handler(commands=['regrull'])
def handle_regrull(message):
	s = sex_all(message)
	if s == 2:
		msg = bot.send_message(message.chat.id,'Регистрирую... Говори, кто ты по жизни? "Мужик" или "Девчуля"? Введи мне ответ:')
		bot.register_next_step_handler(msg, process_step)
		ss = sex_all(message)
		if ss == 1:
			bot.clear_step_handler(msg)
		elif ss == 0:
			bot.clear_step_handler(msg)
		else:
			pass

	elif s==1:
		pass
	else:
		pass

#добавляем ник пользователя в базу
def process_step(message):
	name = message.from_user.username+'\n'+'0'+'\n'
	msg_mwan = str.lower(message.text)
	msg_mwan = clean_textn (msg_mwan)
	msg_mwan = clean_tostart (msg_mwan)
	msg_mwan = clean_resh (msg_mwan)
	if msg_mwan=='мужик':
		#sex = 1
		o = open(vusersm,'a', encoding = "utf-8")
		o.write(name)
		o.close()
		bot.send_message(message.chat.id, message.from_user.first_name)
		bot.send_message(message.chat.id,'Поздравляю! Вы добавлены в список потенциальных ПИДОРОВ!')
	elif msg_mwan=='девчуля':
		#sex = 0
		o = open(vusersw,'a', encoding = "utf-8")
		o.write(name)
		o.close()
		bot.send_message(message.chat.id, message.from_user.first_name)
		bot.send_message(message.chat.id,'Поздравляю! Вы добавлены в список потенциальных ТПШЕЧЕК!')
	else:
		bot.send_message(message.chat.id,'Эй, не тормози раньше времени! Забиваешь мне ерундой голову. Пиши точно: Мужик ты или Девчуля? Давай начнем снова с ввода команды регистрации...')

#Обработчик команды delrull - регистрация в рулетке (виртуальная клавиатура)
@bot.message_handler(commands=['delrull'])
def handle_delrull(message):
	s = sex_all(message)
	if s == 2:
		bot.send_message(message.chat.id,'Вы еще не регистрировались в базе потенциальных ПИДОРОВ или ТПШЕЧЕК!')
	elif s==1:
		bot.send_message(message.chat.id,'Удаляю вас из базы...')
		name = message.from_user.username+'\n'

		#del_pids(name,vusersm)
		#rewrite_ftlist(vusersm)
		#del_pids(name,vusersw)
		del_pidsS(name,vusersm)
		rewrite_ftlist(vusersm)
		del_pidsS(name,vusersw)
		rewrite_ftlist(vusersw)
	else:
		pass


#_______________________________________ПРОБА-СРАБОТАЛО______________
def del_pidsS(str_ing,base_s): #удаляем последнюю строку, когда записи ответа не последовало
	f = open(base_s,'r', encoding = "utf-8")
	names = list(f)
	f.close()
	n=0
	for w in names:
		if w==str_ing:
			break
		else:
			pass
		n+=1

	newnames = names[0:(n)]
	nnewlist = names[(n+2):len(names)]
	f = open(temp_file,'w+', encoding = "utf-8")
	for w in newnames:
		f.write(w)
	for w in nnewlist:
		f.write(w)
	f.close()

#перезапись из темпа в лист юзверей
def rewrite_ftlist(file):
	f = open(temp_file,'r', encoding = "utf-8")
	text = f.read()
	f.close()
	o = open(file,'w+', encoding = "utf-8")
	o.write(text)
	o.close()

#Поучение строки из файла
def str_from_file (file):
	f = open(file, "r", encoding = "utf-8")
	spis = list(f)
	f.close()
	return spis

#функция выбора случайной фразы
def select_fr(frlist):
	ffi = randrange(0,len(frlist))
	ffraze = frlist[ffi]
	return ffraze

#команда по поиску пидорасов и тпшек
@bot.message_handler(commands=['pidotp'])
def handle_pidotp(message):
	now_time = time.time()#текущее время в сек
	t_timet = time.ctime(now_time) #текущее время в нормальном виде
	point_time = str_from_file (listpolz)
	str_point = str(point_time) #время из файла строка


	tttt = clean_qvadr (str_point)
	ttt=time.strptime(tttt)
	#bot.send_message(message.chat.id,tttt)
	str_ttt = time.asctime (ttt)
	fl_tm = time.mktime(ttt)+86400
	#bot.send_message(message.chat.id,str_ttt)
	trtime=str(now_time)
	#bot.send_message(message.chat.id,trtime)
	if now_time > fl_tm:
		f = open(listdaupid,'w+', encoding = "utf-8")
		f.write('empty')
		f.close()
		f = open(listdautp,'w+', encoding = "utf-8")
		f.write('empty')
		f.close()
	else:
		pass
	now_pid = stat_read(listdaupid)
	if now_pid == 'empty':
		#ищем пидорасов
		ffraze = select_fr(firstfraze)#первая фраза
		bot.send_message(message.chat.id,ffraze)
		sfraze = select_fr(secondfraze)#вторая фраза
		bot.send_message(message.chat.id,sfraze)
		tfraze = select_fr(thirdfraze)#третья фраза
		bot.send_message(message.chat.id,tfraze)

		pidors = str_from_file(vusersm)
		len_f = (len(pidors)-1)
		p = randrange(1,len_f,2)
		p = randrange(1,len_f,2)
		p = randrange(1,len_f,2)
		#ЗДЕСЬ ПРОВЕРЯМ, В ЧАТЕ ЛИ ЮЗЕР

		#здесь начисляем баллы для p
		p_str = pidors[p]
		pn_str = clean_enter(p_str)
		nowpid_file = open(listdaupid, "w+", encoding = "utf-8")
		nowpid_file.write(pn_str)
		nowpid_file.close()
		points = points_pidsS(p_str,vusersm)
		points_int = int(points)+1#начисляем балл
		points_str = str(points_int)#делаем новые баллы строкой
		rep_points(p_str,points_str,vusersm)
		rewrite_ftlist(vusersm)

		pidfraze = select_fr(pidofraze)#ловим пидора фраза
		pidor = pidfraze+'@'+pidors[p]
		bot.send_message(message.chat.id,pidor)
	else:
		now_fraze = 'Согласно моей информации, по результатам сегодняшнего розыгрыша пидор дня - '+now_pid
		bot.send_message(message.chat.id,now_fraze)

	now_tp = stat_read(listdautp)
	if now_tp == 'empty':
		#ищем тпшек
		tpps = str_from_file(vusersw)
		len_f = (len(tpps)-1)
		p = randrange(1,len_f,2)
		p = randrange(1,len_f,2)
		p = randrange(1,len_f,2)
		#здесь начисляем баллы для p
		p_str =tpps[p]
		pn_str = clean_enter(p_str)
		nowtp_file = open(listdautp, "w+", encoding = "utf-8")
		nowtp_file.write(pn_str)
		nowtp_file.close()
		points = points_pidsS(p_str,vusersw)
		points_int = int(points)+1
		points_str = str(points_int)#делаем новые баллы строкой
		rep_points(p_str,points_str,vusersw)
		rewrite_ftlist(vusersw)

		tpfraze = select_fr(tpshfraze)#ловим тп фраза
		tpp = tpfraze+'@'+tpps[p]
		bot.send_message(message.chat.id,tpp)
		#записываем время в файл
		f = open(listpolz,'w+', encoding = "utf-8")
		#ow_time=time.asctime(now_time)
		f.write(t_timet)
		f.close()

	else:
		nowtp_fraze = 'Согласно моей информации, по результатам сегодняшнего розыгрыша ТПшка дня - '+now_tp
		bot.send_message(message.chat.id,nowtp_fraze)
		hours = int(((fl_tm-now_time)//60)//60)
		hours_str = str(hours)
		minutes = int((fl_tm-now_time)//60)-(hours*60)
		minutes_str = str(minutes)
		seconds = int((fl_tm-now_time)-(((hours*60)+minutes)*60))
		seconds_str = str(seconds)
		do_timer = 'До следующего запуска рулетки осталось: '+hours_str+' часов '+minutes_str+' минут '+seconds_str+' секунд.'
		bot.send_message(message.chat.id,do_timer)

#команда по поиску пидорасов и тпшек
@bot.message_handler(commands=['ptstat'])
def handle_ptstat(message):

	bot.send_message(message.chat.id,'Статистика __пидоров__ чата:')
	stat_pid(vusersm)
	stat_string = stat_read(temp_file)
	bot.send_message(message.chat.id,stat_string)

	bot.send_message(message.chat.id,'Статистика __ТПшек__ чата:')
	stat_pid(vusersw)
	stat_string = stat_read(temp_file)
	bot.send_message(message.chat.id,stat_string)

#записываем статистику в темп файл
def stat_pid(base_s):
	f = open(base_s,'r', encoding = "utf-8")
	names = list(f)
	f.close()
	o = open(temp_file,'w+', encoding = "utf-8")
	n=0

	for w in names:
		nnw = clean_enter (w)
		if len(w)>4:
			n+=1
			num = str(n)+'. '
			numw = num+nnw
			o.write(numw)
		elif nnw=='#':
			pass
		elif len(w)<=4:
			stw=' - '+nnw+' раз(а)'+'\n'
			o.write(stw)
		else:
			pass

	o.close()

def stat_read(file): #читаем текст из любого файла
	f = open(file, "r", encoding = "utf-8") #открываем файл в режиме чтения
	stat_string = f.read()
	f.close() #закрываем файл
	return stat_string

#замена строки на строку в определенном файле
def rep_points(str_ing,rep_str,f): #str_ing - имя пользователя rep_str - новые баллы f - файл-база
	words_file = open(f, "r", encoding = "utf-8") #открываем файл в режиме чтения
	names = list(words_file)
	words_file.close()
	n=0
	for w in names:
		if w==str_ing:
			break
		else:
			pass
		n+=1

	donames = names[0:(n+1)]
	rep_str = rep_str+'\n'
	poslenames = names[(n+2):len(names)]
	f = open(temp_file,'w+', encoding = "utf-8")
	for w in donames:
		f.write(w)
	f.write(rep_str)
	for w in poslenames:
		f.write(w)
	f.close()

#находим сколько баллов у пользователя
def points_pidsS(str_ing,base_s):
	f = open(base_s,'r', encoding = "utf-8")
	names = list(f)
	f.close()
	n=0
	for w in names:
		if w==str_ing:
			break
		else:
			pass
		n+=1
	points = names[(n+1)]
	return points

#команда удаления пользователя из базы пидаров
@bot.message_handler(commands=['deluser'])
def handle_deluser(message):
	sendd = bot.send_message(message.chat.id,'Введите ник пользователя, которого нужно удалить из базы(без @):')
	bot.register_next_step_handler(sendd, ddel_uspid) #слушаем фразу для удаления

def ddel_uspid(message):
	name = message.text+'\n'
	del_pidsS(name,vusersm)
	rewrite_ftlist(vusersm)
	del_pidsS(name,vusersw)
	rewrite_ftlist(vusersw)
	bot.send_message(message.chat.id,'Если ник введен верно, то пользователь удален!')

#__________________________________АЛКАШ___________________________
@bot.message_handler(commands=['alkash'])
def handle_alkash(message):
	f = open(alkash,'r', encoding = "utf-8")#vusersm
	name = f.read()
	f.close()
	name = '#'+str(name)
	ffraze = select_fr(alkashfr)+name#первая фраза
	bot.send_message(message.chat.id,ffraze)

@bot.message_handler(commands=['addalk'])
def handle_alkash(message):
	sendd = bot.send_message(message.chat.id,'Введите имя алкаша:')
	bot.register_next_step_handler(sendd, alko_fraze) #слушаем фразу для удаления

def alko_fraze(message):
	f = open(alkash,'w+', encoding = "utf-8")#vusersm
	f.write(message.text)
	f.close()
	bot.send_message(message.chat.id,'Имя алкаша изменено^^')


#перезапуск бота по команде
@bot.message_handler(commands=['restart'])
def handle_restart(message):
	cmd = 'bot_REstart .bat'
	PIPE = subprocess.PIPE
	p = subprocess.Popen(cmd, shell = True)
	p.wait()

#_____________________________________убийца шмы__________________________-
#убийца
@bot.message_handler(commands=['shmaubeisya'])
def handle_shmakill(message):
	time_fo_ban = message.date+300;	#Время бана в секундах
	chatid = message.chat.id;
	userid = "200164142";
	bot.restrict_chat_member(chatid,userid,until_date=time_fo_ban,can_send_messages=False);
	fr_kill = "Шма, "+select_fr(shmappc)
	bot.send_message(message.chat.id,fr_kill)


#_________________________________русская рулетка_________________________

#по команде регистрируем пользователя рулетки
@bot.message_handler(commands=['regrulet'])
def handle_regrulet(message):
	rulname = message.from_user.first_name #Имя пользователя из чата
	iduser = message.from_user.id #id пользователя из чата
	Siduser = str(iduser); #id пользователя из чата в строковом формате
	#bot.send_message(message.chat.id,rulname)
	#bot.send_message(message.chat.id,iduser)
	f = open(rouletteus, "r", encoding = "utf-8") #открываем файл в режиме чтения
	fromlist = list(f) #читаем все имена из списка смертников
	for ur in fromlist:
		ur = clean_enter(ur) #очищаем от энтеров
		if ur==rulname:
			yes = 1
			break
		else:
			yes = 0
	f.close()
	if yes ==1:
		bot.send_message(message.chat.id,'😈Вы уже зарегистрированы в списке смертников русской рулетки!😈')
	else: #если пользователя нет в списке, заносим его
		bot.send_message(message.chat.id,'👻Добавляю Вас в список бесстрашных суицидников русской рулетки!👻')
		f = open(rouletteus, "a", encoding = "utf-8") #открываем файл в режиме дозаписи
		f.write(rulname + '\n')
		f.write('#'+Siduser + '\n')
		f.close()

#по команде удаляем пользователя рулетки
@bot.message_handler(commands=['delrulet'])
def handle_delrulet(message):
	rulname = message.from_user.first_name #Имя пользователя из чата
	iduser = message.from_user.id #id пользователя из чата
	Siduser = str(iduser); #id пользователя из чата в строковом формате
	f = open(rouletteus, "r", encoding = "utf-8") #открываем файл в режиме чтения
	fromlist = list(f) #читаем все имена из списка смертников
	for ur in fromlist:
		ur = clean_enter(ur) #очищаем от энтеров
		if ur==rulname:
			yes = 1
			break
		else:
			yes = 0
	f.close()
	if yes ==1:
		bot.send_message(message.chat.id,'Вы образумились? Отлично. Удаляю Вас из списка потенциальных трупов.👍👍👍')
		f = open(rouletteus, "r", encoding = "utf-8") #открываем файл в режиме добавления в конец файла
		f_string = f.read()
		f.close() #закрываем файл

		f_string = (re.sub((rulname+'\n'+'#'+Siduser+'\n'), '', f_string)) #если что то тут убрать \n file_string = (re.sub(('\n'+str_ing), "\n", file_string))

		f = open(rouletteus, "w", encoding = "utf-8") #открываем файл в режиме добавления в конец файла
		f_string = f.write(f_string)
		f.close() #закрываем файл
	else: #если пользователя нет в списке, говорим, что надо зарегаться
		bot.send_message(message.chat.id,'🤔А Вы в здравом уме, раз не регистрировались в списке для русской рулетки, но если я ошибаюсь можете сделать это командой /regrulet')

#по команде начинаем русскую рулетку
@bot.message_handler(commands=['rusrul'])
def handle_rusrul(message):
	time_fo_ban = message.date+30;	#Время бана в секундах
	chatid = message.chat.id; #id чата
	killer = message.from_user.first_name
	f = open(rouletteus, "r", encoding = "utf-8") #открываем файл в режиме добавления в конец файла
	fromlist = list(f)
	num = 0
	for n in fromlist:
		if not '#' in n:
			num=num+1
		else:
			pass
	str_kand = '#'+killer+' заряжает револьвер.'+'\n😏 В списке смертников '+str(num)+' кандидатов... \n#'+killer+' наводит пистолет на...'

	numS = num*2
	i = randrange(0,numS)
	i = randrange(0,numS)
	i = randrange(0,numS)
	if '#' in fromlist[(i)]:
		jert = fromlist[(i-1)]
		jertid = clean_resh(fromlist[(i)])
	else:
		jert = fromlist[(i)]
		jertid = clean_resh(fromlist[(i+1)])
	jert = clean_enter(jert)

	patr = randrange(0,2)
	if patr == 1:
		jertid = int(jertid)
		bot.send_message(message.chat.id,str_kand+'#' + jert + '. \nМедленно нажимает на курок... 😱\n💥💥💥Бабах!💥💥💥 #' + jert + ' убит на 30 секунд!')
		bot.restrict_chat_member(chatid,jertid,until_date=time_fo_ban,can_send_messages=False);
	else:
		bot.send_message(message.chat.id,str_kand+'#' + jert + '. \nМедленно нажимает на курок... 😱\n😇Фууууух! #' + jert + ', похоже сегодня твой день. Пронесло. 😇 #'+killer+' промахнулся!')
	f.close() #закрываем файл

'''
#________________________________________WAKIE_________________________
#обработка команды wakie
@bot.message_handler(commands=['wakie'])
def handle_wakie(message):
	user = message.from_user.username
	wake_io = 0
	f = open('wakie.ii','r', encoding = "utf-8")#vusersm
	spisokp = list(f)
	f.close()
	name = '*'+user+"\n"
	for w in spisokp:
		if w==name:
			bot.send_message(message.chat.id,'Вы уже установили будильник. Удалите его, чтобы установить новый!')
			wake_io = 0
			break
		else:
			wake_io = 1
	if wake_io == 1:
		sendd = bot.send_message(message.chat.id,'Введите точное время по Калининграду(GMT+2), когда вас разбудить:')
		bot.register_next_step_handler(sendd, wakie) #слушаем фразу для удаления
	else:
		pass

def wakie(message):

	#bot.send_message(message.chat.id,message.text) #выводим время которое отправил пользователь
	wake_time = message.text
	if len(wake_time)==4:
		hour = wake_time[0]
		minutes = wake_time[2:4]
	elif len(wake_time)==5:
		hour = wake_time[0:2]
		if int(hour[0])==0:
			hour = wake_time[1]
		else:
			pass
		minutes = wake_time[3:5]
	else:
		bot.send_message(message.chat.id,'Неверный формат времени! Попробуй что-то типа 18.15')

	if int(hour) >= 0:
		if int(hour)<25:
				if int(minutes) >= 0:
					if int(minutes)<61:
						wakie_allok(message,hour,minutes)
					else:
						bot.send_message(message.chat.id,"Неверный формат времени! Попробуй что-то типа 18.15")
				else:
					bot.send_message(message.chat.id,"Неверный формат времени! Попробуй что-то типа 18.15")
		else:
			bot.send_message(message.chat.id,"Неверный формат времени! Попробуй что-то типа 18.15")
	else:
		bot.send_message(message.chat.id,"Неверный формат времени! Попробуй что-то типа 18.15")


#добавление будильника в базу!!!!!!!!!!!!!!!!!
def wakie_allok(message,hour,minutes):
	#bot.send_message(message.chat.id,hour)
	#bot.send_message(message.chat.id,minutes)

	user = message.from_user.username #присваиваем в переменную имя пользователя
	#bot.send_message(message.chat.id,user)# выводим имя пользователя

	now_time = time.time()#текущее время в сек
	t_timet = time.ctime(now_time) #текущее время в нормальном виде
	hmn_time = time.strptime(t_timet) #текущее время в строке
	str_hn = time.strftime("%H",hmn_time) #текущие часы в строке
	str_mn = time.strftime("%M", hmn_time) #текущие минут в строке
	str_hmn = 'Сейчас: '+str_hn+' часов '+str_mn+' минут' #строка для вывода текущего времени
	#bot.send_message(message.chat.id,str_hmn)# выводим строку с текущим временем

	if int(hour)<int(str_hn):
		sleeph_wak = 24-int(str_hn)+int(hour)-1
		sleepm_wak = (60-int(str_mn))+int(minutes)
	elif int(hour)>int(str_hn):
		sleeph_wak = int(hour)-int(str_hn)-1
		sleepm_wak = (60-int(str_mn))+int(minutes)
	else:
		if int(minutes)>int(str_mn):
			sleeph_wak = 0
			sleepm_wak = int(minutes)-int(str_mn)
		else:
			sleeph_wak = 24-int(str_hn)+int(hour)-1
			sleepm_wak = int(str_mn)-int(minutes)

	sleep_sec = ((sleeph_wak*60)+sleepm_wak)*60#время, через которое надо разбудить в секундах!!!!!!!!!!!!!!
	sleeph_wak_st = str(sleeph_wak)
	sleepm_wak_st = str(sleepm_wak)
	bud_time =  sleep_sec+now_time
	t_timet = time.ctime(bud_time)
	sleep_sec_st = '#'+str(t_timet)
	if sleep_sec > 300:
		f = open('wakie.ii','a', encoding = "utf-8")
		f.write('*'+user+'\n'+sleep_sec_st+'\n')
		f.close()
		bot.send_message(message.chat.id,'Хорошо, не выключайте Интернет. Я сообщу местным будистам о том, что Вас нужно разбудить!')
		wakie_time_bud()#(message)
	else:
		bot.send_message(message.chat.id,'Будильник нельзя завести менее чем на 5 минут.')

def wakie_time_bud():#(message):
	f = open('tempid.ii','r', encoding = "utf-8")#vusersm
	chatid = f.read()
	f.close()
	chatid = str(chatid)
	now_time = time.time()
	f = open('wakie.ii','r', encoding = "utf-8")#vusersm
	names = list(f)
	f.close()
	for w in names:
		w_resh=clean_resh (w)
		w_start = clean_tostart (w)
		if len(w) == len(w_start)+1:
			name_tw = clean_enter(w)
			name_tw = clean_tostart (name_tw)
			#bot.send_message(chatid,name_tw)#message.chat.id
		elif len(w)==len(w_resh)+1:
			slee_tw = clean_resh (w)
			#bot.send_message(chatid,slee_tw)#message.chat.id
			slee_tw = clean_enter(slee_tw)
			tttt = clean_qvadr (slee_tw)
			ttt=time.strptime(tttt)#переводит строку со временем во временной формат
			fl_tm = time.mktime(ttt)#превращаем время будильника в секунды
			if fl_tm > (now_time):#+3600
				sleep_twint = fl_tm - (now_time)#+3600
				sleep_tw = sleep_twint
				p = Process(target=budilnik, args=(chatid,name_tw,sleep_tw))#budilnik(message,name_tw,sleep_tw)
				p.start()
			else:
				bot.send_message(chatid,'Похоже связь была утеряна (Роскомнадзор, суки, опять со своими блокировками!) и я кого-то не разбудил! Соррьки(')
		else:
			pass

def budilnik(chatid,name_tw,sleep_tw):
	if int(sleep_tw) > 300:
		time.sleep(int(sleep_tw)-300) #таймер
		str_budil = 'Напоминаю. Тут один сонный человечик, просил разбудить! Дайте @'+name_tw+' поспать 5 минуточек и будите^^'
		bot.send_message(chatid,str_budil)
	else:
		pass
	time.sleep(int(sleep_tw))
	str_budil = 'Эй, будисты! Срочно будите @'+name_tw+'. Этому Соне уже давно пора вставать=)'
	bot.send_message(chatid,str_budil)
	name = '*'+name_tw+'\n'
	del_pidsS(name,'wakie.ii')
	rewrite_ftlist('wakie.ii')
'''
#_____________________antispam bot_________________
def antispam(message):
	bot.send_message(message.chat.id,'Antispam-bot is work!')
#Удаляем свой будильник
@bot.message_handler(commands=['delwakie'])
def handle_delwakie(message):
	user = message.from_user.username
	wake_io = 0
	f = open('wakie.ii','r', encoding = "utf-8")#vusersm
	spisokp = list(f)
	f.close()
	name = '*'+user+"\n"
	for w in spisokp:
		if w==name:
			wake_io = 0
			break
		else:
			wake_io = 1
	if wake_io == 1:
		bot.send_message(message.chat.id,'Вашего будильника нет в списке.')
	elif wake_io==0:
		bot.send_message(message.chat.id,'Удаляю будильник из спика...')
		name = '*'+user+'\n'
		del_pidsS(name,'wakie.ii')
		rewrite_ftlist('wakie.ii')

	else:
		pass

#Список слиперов
@bot.message_handler(commands=['sleepers'])
def handle_sleepers(message):
	f = open('wakie.ii','r', encoding = "utf-8")#vusersm
	names = list(f)
	f.close()
	bot.send_message(message.chat.id,'Список будильников для текущих Сонь:')
	for w in names:
		if len(names)==1:#('empty'+'\n'):
			bot.send_message(message.chat.id,'Некого будить! Все проснулись!')
		else:
			if str(w)==('empty'+'\n'):
				pass
			else:
				w=str(w)
				w=clean_enter(w)
				w=clean_resh(w)
				w=clean_tostart(w)
				bot.send_message(message.chat.id,w)

#__________восстановление баннов________________________
@bot.message_handler(commands=['returnme'])#вернуть меня
def handle_returnme(message):
	if rulles(message) == True:
		bot.restrict_chat_member(chat_idwork,user_admin,can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True,can_add_web_page_previews=True)
		bot.send_message(message.chat.id,'Xottabb14 is ok!',reply_to_message_id=message.message_id)
		bot.restrict_chat_member(chat_idwork,'1189995510',can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True,can_add_web_page_previews=True)
		bot.send_message(message.chat.id,'Shkerb14 is ok!',reply_to_message_id=message.message_id)
	else:
		bot.send_message(message.chat.id,'Не положено!',reply_to_message_id=message.message_id)

@bot.message_handler(commands=['return1189995510'])#вернуть id 1189995510
def handle_returned(message):
	if rulles(message) == True:
		bot.restrict_chat_member(chat_idwork,'1189995510',can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True,can_add_web_page_previews=True)
		bot.send_message(message.chat.id,'Edik is ok!',reply_to_message_id=message.message_id)
	else:
		bot.send_message(message.chat.id,'Не положено!',reply_to_message_id=message.message_id)

@bot.message_handler(commands=['returnboom'])#вернуть бума из бана
def handle_returnboom(message):
	if rulles(message) == True:
		bot.restrict_chat_member(chat_idwork,'593641534',can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True,can_add_web_page_previews=True)
		bot.send_message(message.chat.id,'Boom is ok!',reply_to_message_id=message.message_id)
	else:
		bot.send_message(message.chat.id,'Не положено!',reply_to_message_id=message.message_id)

@bot.message_handler(commands=['returnbot'])#вернуть бота из бана
def handle_returnbot(message):
	if rulles(message) == True:
		bot.restrict_chat_member(chat_idwork,'405960981',can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True, can_change_info=True, can_invite_users=True, can_pin_messages=True)
		bot.send_message(message.chat.id,'All premissions ok!',reply_to_message_id=message.message_id)
		bot.chat_member(chat_idwork,'405960981',can_be_edited=True, can_change_info=True, can_post_messages=True, can_edit_messages=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True, can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True)
		bot.send_message(message.chat.id,'All Rulles ok!',reply_to_message_id=message.message_id)
		pass
	else:
		bot.send_message(message.chat.id,'Не положено!',reply_to_message_id=message.message_id)
#__________конец восстановление баннов________________________



#__________reaction for stickers______
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
	try:	
		list_badst = readlistfile('badcontent.ii')
		for bad in list_badst:
			if bad.replace('\n','') in str(message.sticker.file_unique_id):
				bot.delete_message(message.chat.id,message.message_id)
	except Exception as e:
		print("DelSteckerReactionError: ", e)
	try:
		if '-484910233'	in str(message.chat.id):
			#bot.send_message('-484910233',message.text)#chat_idwork
			bot.send_sticker(chat_idwork,message.sticker.file_id)
		if rulles(message) == True:
			#print (str(message))
			mymessageid = str(message.message_id)+'\n'
			file_my_messageid = str(message.from_user.id)+'/'+str(message.chat.id)
			o = open(file_my_messageid,'a', encoding = "utf-8")
			o.write(mymessageid)
			o.close()
		if config.test_chat	in str(message.chat.id):
			#bot.send_message('-484910233',message.text)#chat_idwork
			bot.send_message(config.test_chat,message.sticker.file_id,reply_to_message_id=message.message_id)

	except Exception as e:
		print("ExceptionSteckerReactionError: ", e)
	try:
		if '👍' in str(message.sticker.emoji):
			reiting_go(message,"+")
		elif '👎' in str(message.sticker.emoji):
			reiting_go(message,"-")
		else:
			pass
	except:
		pass

	if user_admin in str(message.chat.id):
		print(str(message.sticker.file_id))
		logging("ID_STICKER",str(message.sticker.file_id))

	stick_list = open('stickers.id', "r", encoding = "utf-8") #открываем файл в режиме чтения
	file_sticks = list(stick_list)
	stick_list.close()
	stk_rand = randrange(0,(len(file_sticks)-1))
	sticker_id = str(file_sticks[stk_rand])
	sticker_id_g = clean_enter(sticker_id)
	#print(sticker_id_g)
	try:
		if str(message.reply_to_message.from_user.username) == "iishka_bot":
			#(str(message.reply_to_message))
			bot.send_sticker(message.chat.id,sticker_id_g,reply_to_message_id=message.message_id)
		else:
			pass
	except Exception as e:
		print("ExceptionSteckerReactionError: ", e)
		#logging("ERROR_REACTION",e)
	#bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAInfF8j0Ms_wKVYa7UHM3yl_VmX4C5pAAI0AANfxgEZGbHlUy5kC0kaBA')

#бот реагирует на left users
@bot.message_handler(content_types=["left_chat_member"])
def search_leftmemb(message):
	#bot.send_message(config.user_admin, str(message))
	rand_list_end = [' сваливает из чата. Дрянь.😈',' пытается по-тихому сбежать. Мы скучать не будем...😒',' хочет уйти по-аглиццки...😝']
	rand_end_str = str(rand_list_end[randrange(0,len(rand_list_end)-1)])
	try:
		str_leftmem = "Кто-то"+rand_end_str
		try:
			str_leftmem = '@'+str(message.left_chat_member.username)+rand_end_str
		except:
			try:
				str_leftmem = str(message.left_chat_member.first_name)+rand_end_str
			except:
				str_leftmem = str(message.left_chat_member.id)+rand_end_str
		bot.send_message(message.chat.id, str_leftmem)	
	except Exception as e:
		print("LEFT_USER_Error: ", e)
		logging("ERROR_LEFT_MEMB",e)

#бот реагирует на new users
@bot.message_handler(content_types=["new_chat_members"])
def search_newmemb(message):
	#print ("Members here!!! \n")#(str(message.new_chat_members))
	#ban user messages!!!!!!!!!
	id_new_member = str(message.from_user.id)
	if '1220643323' in id_new_member:
		bot.send_message(message.chat.id, 'Привет, Ильюха. Опять ты скачешь, как блоха по *опе гиппопотама?')
	else:
		chatidtp = str(message.chat.id)
		bot.restrict_chat_member(message.chat.id, message.from_user.id,can_send_messages=False)
		#known_fw(str(time.time()),'tempbanid.ii')
		name_new_user = str(message.from_user.first_name)
		if 'None' in str(message.from_user.first_name):
			name_new_user = str(message.from_user.username)
		else:
			name_new_user = str(message.from_user.first_name)
		privetnews = select_fr(privetnew) #random fraze privet
		bothello = clean_namename (privetnews,name_new_user)#"Приветствуем тебя "+name_new_user+". У тебя ровно 15 секунд чтобы нажать кнопку ниже, а иначе последует бан!"
		user_id_new = str(message.from_user.id)
		known_fw(user_id_new,'newuserk.ii')
		known_fw(chatidtp,'chatidtmp.ii')
		keyboard_new = types.InlineKeyboardMarkup()
		text_of_hotbutton = select_fr(config.buttontuk)
		currencypair = types.InlineKeyboardButton(text=text_of_hotbutton, callback_data='nospammer39')
		keyboard_new.add(currencypair)
		bot.send_message(message.chat.id, bothello, reply_markup=keyboard_new) #ilya 1220643323

#________________________meeting______________________________________
@bot.message_handler(commands=['meeting'])
def handle_meeting(message):
	mess_data = str(message)
	meeter = str(message.from_user.id)
	known_fw(meeter,'meeter.ii')
	keyboard_meet = types.InlineKeyboardMarkup()
	one_day = types.InlineKeyboardButton(text='Понедельник', callback_data='day_meeting1')
	two_day = types.InlineKeyboardButton(text='Вторник', callback_data='day_meeting2')
	three_day = types.InlineKeyboardButton(text='Среда', callback_data='day_meeting3')
	four_day = types.InlineKeyboardButton(text='Четверг', callback_data='day_meeting4')
	five_day = types.InlineKeyboardButton(text='Пятница', callback_data='day_meeting5')
	six_day = types.InlineKeyboardButton(text='Суббота', callback_data='day_meeting6')
	seven_day = types.InlineKeyboardButton(text='Воскресенье', callback_data='day_meeting7')
	keyboard_meet.add(one_day,two_day,three_day,four_day,five_day,six_day,seven_day)
	bot.send_message(message.chat.id,'Выберите день для встречи:', reply_markup=keyboard_meet)


def meet_func(call,dayseted):
	meeter = known_fw(dayseted,'daymeet.ii')
	keyboard_meet = types.InlineKeyboardMarkup()
	time0000 = types.InlineKeyboardButton(text='00:00', callback_data='00:00')
	time0030 = types.InlineKeyboardButton(text='00:30', callback_data='00:30')
	time0100 = types.InlineKeyboardButton(text='01:00', callback_data='01:00')
	time0130 = types.InlineKeyboardButton(text='01:30', callback_data='01:30')
	time0200 = types.InlineKeyboardButton(text='02:00', callback_data='02:00')
	time0230 = types.InlineKeyboardButton(text='02:30', callback_data='02:30')
	time0300 = types.InlineKeyboardButton(text='03:00', callback_data='03:00')
	time0330 = types.InlineKeyboardButton(text='03:30', callback_data='03:30')
	time0400 = types.InlineKeyboardButton(text='04:00', callback_data='04:00')
	time0430 = types.InlineKeyboardButton(text='04:30', callback_data='04:30')
	time0500 = types.InlineKeyboardButton(text='05:00', callback_data='05:00')
	time0530 = types.InlineKeyboardButton(text='05:30', callback_data='05:30')
	time0600 = types.InlineKeyboardButton(text='06:00', callback_data='06:00')
	time0630 = types.InlineKeyboardButton(text='06:30', callback_data='06:30')
	time0700 = types.InlineKeyboardButton(text='07:00', callback_data='07:00')
	time0730 = types.InlineKeyboardButton(text='07:30', callback_data='07:30')
	time0800 = types.InlineKeyboardButton(text='08:00', callback_data='08:00')
	time0830 = types.InlineKeyboardButton(text='08:30', callback_data='08:30')
	time0900 = types.InlineKeyboardButton(text='09:00', callback_data='09:00')
	time0930 = types.InlineKeyboardButton(text='09:30', callback_data='09:30')
	time1000 = types.InlineKeyboardButton(text='10:00', callback_data='10:00')
	time1030 = types.InlineKeyboardButton(text='10:30', callback_data='10:30')
	time1100 = types.InlineKeyboardButton(text='11:00', callback_data='11:00')
	time1130 = types.InlineKeyboardButton(text='11:30', callback_data='11:30')
	time1200 = types.InlineKeyboardButton(text='12:00', callback_data='12:00')
	time1230 = types.InlineKeyboardButton(text='12:30', callback_data='12:30')
	time1300 = types.InlineKeyboardButton(text='13:00', callback_data='13:00')
	time1330 = types.InlineKeyboardButton(text='13:30', callback_data='13:30')
	time1400 = types.InlineKeyboardButton(text='14:00', callback_data='14:00')
	time1430 = types.InlineKeyboardButton(text='14:30', callback_data='14:30')
	time1500 = types.InlineKeyboardButton(text='15:00', callback_data='15:00')
	time1530 = types.InlineKeyboardButton(text='15:30', callback_data='15:30')
	time1600 = types.InlineKeyboardButton(text='16:00', callback_data='16:00')
	time1630 = types.InlineKeyboardButton(text='16:30', callback_data='16:30')
	time1700 = types.InlineKeyboardButton(text='17:00', callback_data='17:00')
	time1730 = types.InlineKeyboardButton(text='17:30', callback_data='17:30')
	time1800 = types.InlineKeyboardButton(text='18:00', callback_data='18:00')
	time1830 = types.InlineKeyboardButton(text='18:30', callback_data='18:30')
	time1900 = types.InlineKeyboardButton(text='19:00', callback_data='19:00')
	time1930 = types.InlineKeyboardButton(text='19:30', callback_data='19:30')
	time2000 = types.InlineKeyboardButton(text='20:00', callback_data='20:00')
	time2030 = types.InlineKeyboardButton(text='20:30', callback_data='20:30')
	time2100 = types.InlineKeyboardButton(text='21:00', callback_data='21:00')
	time2130 = types.InlineKeyboardButton(text='21:30', callback_data='21:30')
	time2200 = types.InlineKeyboardButton(text='22:00', callback_data='22:00')
	time2230 = types.InlineKeyboardButton(text='22:30', callback_data='22:30')
	time2300 = types.InlineKeyboardButton(text='23:00', callback_data='23:00')
	time2330 = types.InlineKeyboardButton(text='23:30', callback_data='23:30')
	keyboard_meet.add(time0000,time0030,time0100,time0130,time0200,time0230,time0300,time0330,time0400,time0430,time0500,time0530,time0600,time0630,time0700,time0730,time0800,time0830,time0900,time0930,time1000,time1030,time1100,time1130,time1200,time1230,time1300,time1330,time1400,time1430,time1500,time1530,time1600,time1630,time1700,time1730,time1800,time1830,time1900,time1930,time2000,time2030,time2100,time2130,time2200,time2230,time2300,time2330)
	#bot.send_message(message.chat.id,'Время для встречи:', reply_markup=keyboard_meet)
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Время для встречи:', reply_markup=keyboard_meet)
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	id_now_user = known_fr('newuserk.ii')
	chatidtp = known_fr('chatidtmp.ii')
	meeter = known_fr('meeter.ii')
	id_clicker = call.from_user.id
	id_now_user = clean_enter (str(id_now_user))
	id_clicker = clean_enter (str(id_clicker))
	chatidtp = clean_enter (str(chatidtp))
	if call.data == "igomeet":
		if "None" in str(call.from_user.username):
			usermeetname = str(call.from_user.first_name)
			usermeetnamez = '@'+usermeetname
		else:
			usermeetname = str(call.from_user.username)
			usermeetnamez = '@'+usermeetname
		MSGfortextMeet = known_fr('MSGfortextMeet.ii')
		if usermeetname in MSGfortextMeet:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Ну и фиг с тобой.")
			str_del_meet = ', '+usermeetnamez
			MSGfortextMeetNew = MSGfortextMeet.replace(str_del_meet,'')
			known_fw(MSGfortextMeetNew,'MSGfortextMeet.ii')
			keyboard_igo = types.InlineKeyboardMarkup()
			igo_butt = types.InlineKeyboardButton(text='Я буду/Не буду👻', callback_data='igomeet')
			keyboard_igo.add(igo_butt)
			bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=MSGfortextMeetNew,reply_markup=keyboard_igo)
		else:
			MSGfortextMeetNew = MSGfortextMeet+", @"+usermeetname
			known_fw(MSGfortextMeetNew,'MSGfortextMeet.ii')
			keyboard_igo = types.InlineKeyboardMarkup()
			igo_butt = types.InlineKeyboardButton(text='Я буду/Не буду👻', callback_data='igomeet')
			keyboard_igo.add(igo_butt)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=MSGfortextMeetNew,reply_markup=keyboard_igo)

	if int(id_now_user) == int(id_clicker):
		if call.data == "nospammer39":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отлично! Проходи, располагайся!😎 Не забудь прочитать правила /ruleskld")
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Отлично! Проходи, располагайся!😎😎😎")
			bot.restrict_chat_member(chatidtp,id_now_user,can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True,can_add_web_page_previews=True)

	else:
		if int(meeter) == int(call.from_user.id):
			if call.data == 'day_meeting1':
				meet_func(call,'Понедельник')
			elif call.data == 'day_meeting2':
				meet_func(call,'Вторник')
			elif call.data == 'day_meeting3':
				meet_func(call,'Среда')
			elif call.data == 'day_meeting4':
				meet_func(call,'Четверг')
			elif call.data == 'day_meeting5':
				meet_func(call,'Пятница')
			elif call.data == 'day_meeting6':
				meet_func(call,'Суббота')
			elif call.data == 'day_meeting7':
				meet_func(call,'Воскресенье')
			else:
				tmeet_io = "None"
				for i in config.time_meet_choose:
					if call.data in i:
						#bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=i)
						tmeet_io = i
						break
					else:
						pass
				if tmeet_io == "None":
					bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Данные может вводить только назначивший встречу.")
				else:
					date_meet_now = known_fr('daymeet.ii')
					tmeet_ioo = date_meet_now+' в '+tmeet_io+' ч.'
					known_fw(tmeet_ioo,'daymeet.ii')
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите подробности встречи (например адрес и причину) или слово "отмена", если передумали. Аккуратней! Следующее ваше сообщение будет сохранено.')
					meeteng_io_meet = "ON"
					#print(meeteng_io_meet)
					known_fw(meeteng_io_meet,'meetIO.ii')
					#bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=tmeet_ioo)
		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="👻")

#___________meeting____END_______________________________

#_____________важные функции_________________
#отправка случайной фразы из файла
def sendregmes(message,fromfilelistfr):
	fraze_fromlist = select_fr(fromfilelistfr)
	bot.send_message(message.chat.id,fraze_fromlist,reply_to_message_id=message.message_id)

#кикнуть спамера
def kickspamer(message):
		bot.delete_message(message.chat.id,message.message_id)
		bot.kick_chat_member(message.chat.id, message.from_user.id)
		spam_fr_frazesreg = select_fr(regularfrazes.smapsvolochi)
		spam_kick_fraze = '@'+str(message.from_user.first_name)+spam_fr_frazesreg
		bot.send_message(message.chat.id,spam_kick_fraze)

#удалить сообщение
def delmessage(message):
		bot.delete_message(message.chat.id,message.reply_to_message.message_id)

#занесение гавноконтента в банлист
def badcontent(message):
	if rulles(message) == True:
		try:
			test_data = ["\'content_type\': \'photo\'","\'content_type\': \'sticker\'","\'content_type\': \'document\'","\'content_type\': \'video\'"]
			for td in test_data:
				if td in str(message):
					f_data = ''
					if 'photo' in td:
						f_data = str(message.reply_to_message.json['photo'][0]['file_unique_id'])+"\n"#.photo[0].file_id)
					elif 'video' in td:
						f_data = str(message.reply_to_message.json['video']['file_unique_id'])+"\n"
					elif 'sticker' in td:
						f_data = str(message.reply_to_message.json['sticker']['file_unique_id'])+"\n"#[0]['file_id'])+"\n"#.sticker.file_id)
					elif 'document' in td:
						f_data = str(message.reply_to_message.json['document']['file_unique_id'])+"\n"#[0]['file_id'])+"\n"
					else:
						pass
					#bot.send_message(message.chat.id,f_data)
					writetofile('badcontent.ii',f_data)
			delmessage(message)
		except Exception as e:
			print (e)
			bot.send_message(message.chat.id,'Согласен🤦‍♂️')
	if modrulles(message) == True:
		try:
			test_data = ["\'content_type\': \'photo\'","\'content_type\': \'sticker\'","\'content_type\': \'document\'","\'content_type\': \'video\'"]
			for td in test_data:
				if td in str(message):
					f_data = ''
					if 'photo' in td:
						f_data = str(message.reply_to_message.json['photo'][0]['file_unique_id'])+"\n"#.photo[0].file_id)
					elif 'video' in td:
						f_data = str(message.reply_to_message.json['video']['file_unique_id'])+"\n"
					elif 'sticker' in td:
						f_data = str(message.reply_to_message.json['sticker']['file_unique_id'])+"\n"#[0]['file_id'])+"\n"#.sticker.file_id)
					elif 'document' in td:
						f_data = str(message.reply_to_message.json['document']['file_unique_id'])+"\n"#[0]['file_id'])+"\n"
					else:
						pass
					#bot.send_message(message.chat.id,f_data)
					writetofile('badcontent.ii',f_data)
			delmessage(message)
		except Exception as e:
			print (e)
			bot.send_message(message.chat.id,'Согласен🤦‍♂️')

#бан пользователя
def xottabbmagic(message,kickmesmag,choosekik):
	if rulles(message) == True:
		try:
			idkicked = message.reply_to_message.from_user.id#.json#.from.id)
			print(str(idkicked))
			bot.send_message(message.chat.id,kickmesmag)
			bot.kick_chat_member(message.chat.id, idkicked)
			bot.delete_message(message.chat.id,message.reply_to_message.message_id)
		except:
			bot.send_message(message.chat.id,choosekik)
	else:
		pass

#__Обработка аудиосообщений__
@bot.message_handler(content_types= ['audio'])
def resend_audio(message):
	try:
		if '-484910233' in str(message.chat.id):
			#bot.send_message(chat_idwork,message.sticker.file_id)
			bot.send_message(chat_idwork,'Music time!💃🏻🕺')
			bot.send_audio(chat_idwork,str(message.audio.file_id))
		if test_chat in str(message.chat.id):
			#bot.send_message(chat_idwork,message.sticker.file_id)
			bot.send_message(test_chat,'FileID:')
			bot.send_message(test_chat,str(message.audio.file_id))
	except:
		pass

#________time_ban________________
def timeban(message,time_for_kick,min_time):
	try:
		if rulles(message) == True:
			time_fo_ban_bad = message.date+time_for_kick
			bot.restrict_chat_member(message.chat.id,message.reply_to_message.from_user.id,until_date=time_fo_ban_bad,can_send_messages=False)
			text_to_timeban = 'Так. В угол на '+min_time+' минут. Подумаешь, поплачешь, вернешься!'
			bot.send_message(message.chat.id,text_to_timeban,reply_to_message_id=message.message_id)
		elif '1189995510' in str(message.from_user.id):
			time_fo_ban_bad = message.date+time_for_kick
			bot.restrict_chat_member(message.chat.id,message.reply_to_message.from_user.id,until_date=time_fo_ban_bad,can_send_messages=False)
			text_to_timeban = 'Сходи, проветрись '+min_time+' минут.'
			bot.send_message(message.chat.id,text_to_timeban,reply_to_message_id=message.message_id)
		else:
			if "None" in str(message.reply_to_message.from_user.username):
				name_baduser = str(message.reply_to_message.from_user.firs_name)
			else:
				name_baduser = str(message.reply_to_message.from_user.username)
			str_tixo = "Bad USVER!______ "+name_baduser+": "+str(message.reply_to_message.text)
			bot.send_message(user_admin,str_tixo)
			bot.send_message(message.chat.id,'Сообщил куда-надо. Уже выехали!',reply_to_message_id=message.message_id)
	except Exception as e:
		print("ExceptionALL: ", e)
		logging("ERROR_ALL",e)

#_____фас____
def fas(message):
	omon_liststr1 = ['Всем оставаться на месте!👀','Никому не дигаться!','Все замерли!👀','Всем лежать!😼','Не двигаться!😼','Замерли!!!👮‍♀️']
	bot.send_message(message.chat.id,str(omon_liststr1[randrange(0,len(omon_liststr1)-1)]))
	omon_liststr2 = ['Работает спецгруппа!','Мордой в пол!👮‍♀️','Лежать, сцука!🤬','К стене!👊','Медленно пни клавиатуру сюда...','Без резких движений, сволочь!']
	xottabbmagic(message,str(omon_liststr2[randrange(0,len(omon_liststr2)-1)]),'База! Отбой! Ложный вызов!👀')
	#bot.send_message(message.chat.id,str(omon_liststr2[randrange(0,len(omon_liststr2)-1)]))
	omon_listgif = ['http://img0.reactor.cc/pics/post/гифки-омон-песочница-1002132.gif','https://otvet.imgsmail.ru/download/u_ea9187585412823d52546fa9814b393d_800.gif','http://img0.joyreactor.cc/pics/post/гифка-омон-задержание-шнурок-развязался-3675908.gif','https://static.life.ru/publications/2020/4/22/241200384572.67203.gif','https://zasmeshi.ru/data/gif/6645-korotko-o-tom-kakaya-u-menya-komanda-v-lyuboj-onlajn-igre.gif']
	nowgif = select_fr(omon_listgif)
	bot.send_animation(message.chat.id,nowgif)
	omon_liststr3 = ['💪Миссия выполнена!','Можете расслабиться. Мудак задержан!👌','Выдыхаем! Скоро приедет скорая с карвалолом.🚑','🤟Всем вольно! Уходим...']
	bot.send_message(message.chat.id,str(omon_liststr3[randrange(0,len(omon_liststr3)-1)]))

#______________конец важных функций______________


#__Обработка фото и видео__
@bot.message_handler(content_types= ['photo','video'])
def resend_photo(message):
	#print(str(message.message_id))
	try:	
		list_badst = readlistfile('badcontent.ii')
		for bad in list_badst:
			if bad.replace('\n','') in str(message.json['photo'][0]['file_unique_id']):
				bot.delete_message(message.chat.id,message.message_id)
	except Exception as e:
		print("DelPhotoError: ", e)
	try:	
		list_badst = readlistfile('badcontent.ii')
		for bad in list_badst:
			if bad.replace('\n','') in str(message.json['video']['file_unique_id']):
				bot.delete_message(message.chat.id,message.message_id)
	except Exception as e:
		print("DelVideoError: ", e)
	try:
		if rulles(message) == True:
			mymessageid = str(message.message_id)+'\n'
			file_my_messageid = str(message.from_user.id)+'/'+str(message.chat.id)
			o = open(file_my_messageid,'a', encoding = "utf-8")
			o.write(mymessageid)
			o.close()
	except Exception as e:
		print("ResendFVError: ", e)
		logging("ERROR_MEDIA",e)
	bot.forward_message('-442562860', message.chat.id,message.message_id)

#__Обработка типа документ__
@bot.message_handler(content_types= ['document'])
def re_gif(message):
	try:	
		list_badst = readlistfile('badcontent.ii')
		for bad in list_badst:
			if bad.replace('\n','') in str(message.json['document']['file_unique_id']):
				bot.delete_message(message.chat.id,message.message_id)
	except Exception as e:
		print("DelDOCReactionError: ", e)
	try:
		if rulles(message) == True:
			if user_admin in str(message.chat.id):
				bot.send_message(user_admin,str(message))
		if '1189995510' in str(message.from_user.id):
			pass#bot.send_message('1189995510',str(message))
	except Exception as e:
		print("ResendFVError: ", e)
		logging("ERROR_MEDIA",e)
	bot.forward_message('-442562860', message.chat.id,message.message_id)
	if 'aajioaacoh5kb33n7esaae8hbhse' in str(message.document.file_id).lower():
		iron_hat = select_fr(regularfrazes.iron_hat)
		bot.send_message(message.chat.id,iron_hat)

#_____________________Рейтинг__________________
#______reiting up
def lvlup(message,lvllist,lvl_user):
	rownum = 0
	for i in lvllist:
		if lvl_user in i:
			rownum = rownum+1
			new_lvl_set = str(int(lvllist[rownum])+1)
			lvllist[rownum] = new_lvl_set
			f = open( 'reiting.ii', 'w', encoding = "utf-8")
			for item in lvllist:
				item_en = clean_enter(item)
				f.write("%s\n" % item_en)
			f.close()
			if lvl_user != 'Xottabb14':
				if lvl_user != 'RussianSpirit39':
					str_new_lvl = 'Рейтинг пользователя @'+lvl_user+' повысился ('+new_lvl_set+')!'
				else:
					str_new_lvl = 'Рейтинг пользователя @'+lvl_user+' всегда ниже плинтуса ('+'#ОднимсловомГном'+')!'
			else:
				str_new_lvl = 'Рейтинг пользователя @'+lvl_user+' всегда высокий ('+'#Простокрасавчик'+')!'
			bot.send_message(message.chat.id,str_new_lvl)
			break
		else:
			rownum = rownum+1

#______reiting down
def lvldown(message,lvllist,lvl_user):
	rownum = 0
	for i in lvllist:
		if lvl_user in i:
			rownum = rownum+1
			new_lvl_set = str(int(lvllist[rownum])-1)
			lvllist[rownum] = new_lvl_set
			f = open( 'reiting.ii', 'w', encoding = "utf-8")
			for item in lvllist:
				item_en = clean_enter(item)
				f.write("%s\n" % item_en)
			f.close()
			if lvl_user != 'Xottabb14':
				if lvl_user != 'RussianSpirit39':
					str_new_lvl = 'Рейтинг пользователя @'+lvl_user+' понизился ('+new_lvl_set+')!'
				else:
					str_new_lvl = 'Рейтинг пользователя @'+lvl_user+' всегда ниже плинтуса ('+'#ОднимсловомГном'+')!'
			else:
				str_new_lvl = 'Рейтинг пользователя @'+lvl_user+' всегда высокий ('+'#Простокрасавчик'+')!'
			bot.send_message(message.chat.id,str_new_lvl)
			break
		else:
			rownum = rownum+1

#______reiting search______
def lvlsearch(message,znak):
	lvlfile = open('reiting.ii', "r", encoding = "utf-8") #открываем файл в режиме чтения
	lvllist = list(lvlfile)
	lvlfile.close()

	name_in = 0
	for i in lvllist:
		#print (i)
		lvl_user = ''
		if 'None' in str(message.reply_to_message.from_user.username):
			lvl_user = str(message.reply_to_message.from_user.first_name)
		else:
			lvl_user = str(message.reply_to_message.from_user.username)
		if lvl_user in i:
			if znak == '+':
				lvlup(message,lvllist,lvl_user)
			else:
				lvldown(message,lvllist,lvl_user)
			#__reaction fo name yes
			name_in = 1
			break
		else:
			name_in = 0
	if name_in == 0:
		if znak == '+':
			namelvl = lvl_user+'\n1\n'
			str_new_lvl = 'Рейтинг пользователя @'+lvl_user+' повысился (1)!'
		else:
			namelvl = lvl_user+'\n-1\n'
			str_new_lvl = 'Рейтинг пользователя @'+lvl_user+' понизился (-1)!'
		f = open('reiting.ii', "a", encoding = "utf-8") #открываем файл в режиме добавления в конец файла
		f.write(namelvl)
		f.close() #закрываем файл
		bot.send_message(message.chat.id,str_new_lvl)
	else:
		pass

def reiting_go(message,plusminus):
	if str(message.reply_to_message.from_user.username) != str(message.from_user.username):
		try:
			lvlsearch(message,plusminus)
		except Exception as e:
			print("RatingError: ", e)
			logging("ERROR_RATING",e)
	else:
		bot.send_message(message.chat.id,'На свой рейтинг влиять нельзя! Хитропопость здесь не приветствуется😈')

#_________________конец рейтинга___________________

#______________________регулярные выражения__________
@bot.message_handler(regexp="((Х|х)уютро?\D*?)|((Х|х)уютричко?\D*?)")
def search_regxp(message):
	sendregmes(message,xuutro)
	bot.send_sticker(message.chat.id,'CAACAgQAAxkBAAIvbF86W9SJhxxuTS02ytsRWvlHiPBfAAIiAANfxgEZ8_q_s-6jQF4aBA')
@bot.message_handler(regexp="(R|r)adio\s\D*?(T|t)ap")
def search_radiotapok(message):
	sendregmes(message,config.radioaimori)
	bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAIvbV86XB5dd7mY0pwcbrTDgvRK_CvoAAKMCAACCTs7E2Q79JtelJtvGgQ')
@bot.message_handler(regexp="(Р|р)адио\s\D*?(Т|т)ап")
def search_radiotapokrus(message):
	sendregmes(message,config.radioaimori)
	bot.send_sticker(message.chat.id,'CAACAgQAAxkBAAIvbl86XGps7ebIR2pWaPzJxeKTCY6xAAIBAQACS2nuEJv1aj-U7cz6GgQ')
@bot.message_handler(regexp="((Э|э)льфы\D*?\s\D*?и\D*?\s\D*?(Г|г)номы\D*?)|((Г|г)номы\D*?\s\D*?и\D*?\s\D*?(Э|э)льфы\D*?)")
def search_elfgnom(message):
	bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAIvb186XRW8oUgaHfYlMweeq3NHxwb1AAK0AwACxKtoC4EsZDYuxEEyGgQ')
	sendregmes(message,regularfrazes.elfgnoms)
@bot.message_handler(regexp="(((T|т)ян)|((Д|д)евушка*))\sв\s(Л|л)(С|с)")
def search_tyanvls(message):
	sendregmes(message,regularfrazes.tyan_ls)
@bot.message_handler(regexp="(В|в)осстани(е|я|ю|ем|ях|й)\s(М|м)ашин(а|у|ы|ам|ой)?")
def search_robokill(message):
	bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAIvcF86XUugnRJqu_QIPnjgQvBTPHWcAAIaAgADOKAK1Dm-NI6wbVIaBA')
	sendregmes(message,regularfrazes.robokill)

@bot.message_handler(regexp="((С|с)пасибо\D*?|(П|п)асиб\D*?|(Б|б)лагодарю\D*?)|(T|t)hank\D*?")
def search_spasibki(message):
	try:
		reiting_go(message,"+")
	except Exception as e:
		print("ThanksError: ", e)
		logging("ERROR_THANKS",e)
@bot.message_handler(regexp="((К|к)уда\D*?\s((С|с)ходить\D*?|(С|с)ездить\D*?))|((К|к)уда*\sв\s(К|к)алининграде\D*?\s((С|с)ходить\D*?|(С|с)ездить\D*?))|((Ч|ч)то\D*?\s(П|п)осмотреть\D*?\sв\s(К|к)алининграде\D*?)|((Ч|ч)то\D*?\sв\s(К|к)алининграде\D*?\s(П|п)осмотреть\D*?)")
def search_kudago(message):
	try:
		f = open('kudago.ii', "r", encoding = "utf-8") #открываем файл в режиме чтения
		kudago_string = f.read()+"\n"+config.str_covidparty
		f.close() #закрываем файл
		bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAIveV86YIkq9BrdGMYBkrEd37n10tQUAAKzAwACRvusBEGIhWrpbAKRGgQ')
		bot.send_message(message.chat.id,kudago_string,parse_mode="Markdown")
	except Exception as e:
		print("ExceptionKUDAGO: ", e)
		logging("ERROR_KUDAGO",e)

@bot.message_handler(regexp="((Д|д)обр\D*?|(Х|х)орош\D*?|(П|п)рекрас\D*?|(Ч|ч)удес\D*?|(К|к)ласс\D*?)\s((У|у)тр\D*?|(В|в)ечер\D*?|(Н|н)оч\D*?|(В|В)рем\D*?|(Д|д)е?н\D)(\s((В|в)се\D*?|(Ч|ч)ат\D*?|(Л|л)юд\D*?|(Д|д)жент\D*?|(Л|л)ед\D*?|(Г|г)оспод\D*?|(Д|д)ам\D*?))|((В|в)се\D*?|(Ч|ч)ат\D*?|(Л|л)юд\D*?|(Д|д)жент\D*?|(Л|л)ед\D*?|(Г|г)оспод\D*?|(Д|д)ам\D*?|(\D*?,))\s((Д|д)обр\D*?|(Х|х)орош\D*?|(П|п)рекрас\D*?|(Ч|ч)удес\D*?|(К|к)ласс\D*?)\s((У|у)тр\D*?|(В|в)ечер\D*?|(Н|н)оч\D*?|(В|В)рем\D*?|(Д|д)е?н\D)|((В|в)се\D*?|(Ч|ч)ат\D*?|(Л|л)юд\D*?|(Д|д)жент\D*?|(Л|л)ед\D*?|(Г|г)оспод\D*?|(Д|д)ам\D*?)\s((У|у)тр\D*?|(В|в)ечер\D*?|(Н|н)оч\D*?|(В|В)рем\D*?|(Д|д)е?н\D)\s((Д|д)обр\D*?|(Х|х)орош\D*?|(П|п)рекрас\D*?|(Ч|ч)удес\D*?|(К|к)ласс\D*?)|(((У|у)тр\D*?|(В|в)ечер\D*?|(Н|н)оч\D*?)|(В|В)рем\D*?|(Д|д)е?н\D)\s((В|в)се\D*?|(Ч|ч)ат\D*?|(Л|л)юд\D*?|(Д|д)жент\D*?|(Л|л)ед\D*?|(Г|г)оспод\D*?|(Д|д)ам\D*?|(\D*?,))\s((Д|д)обр\D*?|(Х|х)орош\D*?|(П|п)рекрас\D*?|(Ч|ч)удес\D*?|(К|к)ласс\D*?)|(((У|у)тр\D*?|(В|в)ечер\D*?|(Н|н)оч\D*?)|(В|В)рем\D*?|(Д|д)е?н\D)\s((Д|д)обр\D*?|(Х|х)орош\D*?|(П|п)рекрас\D*?|(Ч|ч)удес\D*?|(К|к)ласс\D*?)((\s((В|в)се\D*?|(Ч|ч)ат\D*?|(Л|л)юд\D*?|(Д|д)жент\D*?|(Л|л)ед\D*?|(Г|г)оспод\D*?|(Д|д)ам\D*?)))|(((П|п)ривет\D?|(З|з)д(о|а)ров\D|(Т|т)рям|(Х|х)ай|(З|з)дравс\D*?|(У|у)тр\D*?))((\s((В|в)се\D*?|(Ч|ч)ат\D*?|(Л|л)юд\D*?|(Д|д)жент\D*?|(Л|л)ед\D*?|(Г|г)оспод\D*?|(Д|д)ам\D*?))|,\s\D*?)|((В|в)се\D*?|(Ч|ч)ат\D*?|(Л|л)юд\D*?|(Д|д)жент\D*?|(Л|л)ед\D*?|(Г|г)оспод\D*?|(Д|д)ам\D*?|(\D*?,))\s((П|п)ривет\D?|(З|з)д(о|а)ров\D?|(Т|т)рям|(Х|х)ай|(З|з)драс\D*?|(У|у)тр\D|(В|в)ечер\D?|(Н|н)оч\D|(В|В)рем\D|(Д|д)е?н\D)|((В|в)ечер\sв\sхат\D)")
def search_helloall(message):
	stick_list = open('stickersHI.id', "r", encoding = "utf-8") #открываем файл в режиме чтения
	file_sticks = list(stick_list)
	stick_list.close()
	stk_rand = randrange(0,(len(file_sticks)-1))
	sticker_id = str(file_sticks[stk_rand])
	sticker_id_g = clean_enter(sticker_id)
	#bot.send_sticker(user_admin,sticker_id_g,reply_to_message_id=message.message_id)
	bot.send_sticker(message.chat.id,sticker_id_g,reply_to_message_id=message.message_id)





#______________________регулярные выражения (поиск в сообщении)__________
def regularfrazesdef(message):
	if message.text.lower() == "+":
		reiting_go(message,"+")
	if message.text.lower() == "👍":#👎
		reiting_go(message,"+")
	if message.text.lower() == "👎":
		reiting_go(message,"-")
	if message.text.lower() == "-":
		reiting_go(message,"-")
#__________actions in bot____________
	try:
		try:
			if 'None' in str(message.reply_to_message.from_user.username):
				reply_user = str(message.reply_to_message.from_user.first_name)
			else:
				reply_user = str(message.reply_to_message.from_user.username)
			if 'None' in str(message.from_user.username):
				main_user = str(message.from_user.first_name)
			else:
				main_user = str(message.from_user.username)
			namehere = 1
		except Exception as e:
			pass #print("ActionsError: ", e)
			namehere = 0
			reply_user = select_fr(regularfrazes.command_names)
			main_user = str(message.from_user.username)
		if '!обнять' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.obnimash)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user
			bot.send_sticker(message.chat.id,'CAACAgQAAxkBAAIvfV86YmNsab8IEqfVLyDduCrvhahoAAKxAANLae4Q2IJcTH-TNCYaBA')
			bot.send_message(message.chat.id,fraze_with_names)

		if '!поцеловать' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.kissing)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user
			bot.send_sticker(message.chat.id,'CAACAgQAAxkBAAIve186YchpJVen5labpfCsOAFS-BSBAAKjCQACS2nuEEf87XUP3NA4GgQ')
			bot.send_message(message.chat.id,fraze_with_names)
		if '!пожамкать' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.jamkat)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user
			bot.send_message(message.chat.id,fraze_with_names)
		if '!подмигнуть' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.eyedrift)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user
			bot.send_message(message.chat.id,fraze_with_names)
			bot.send_message(message.chat.id,'😉')
		if '!укусить' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.kuskusy)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user
			bot.send_message(message.chat.id,fraze_with_names)
		if '!команды' in message.text.lower():
			fraze_to_commands = known_fr('commands.ii')
			bot.send_message(message.chat.id,fraze_to_commands)
		if '!админкоманды' in message.text.lower():
			if rulles(message) == True:
				fraze_to_commands = known_fr('admcommands.ii')
				bot.send_message(message.chat.id,fraze_to_commands)
		if 'место встречи изменить нельзя' in message.text.lower():
			bot.send_message(message.chat.id,'Это точно. Легендарное место...')
			bot.send_venue(message.chat.id,54.711545, 20.512989,'Легендарные лавки на Нижке.','Historical Center, Калининград, Калининградская обл., 236006')
		if '!ковид' in message.text.lower():
			covidget(message.chat.id,"Данные по COVID-19\nв Калининградской области:")
		if '!covid' in message.text.lower():
			covidget(message.chat.id,"Данные по COVID-19\nв Калининградской области:")
		if '!мем' in message.text.lower():
			memasik(message)
		if '!vtv' in message.text.lower():
			memasik(message)
		if '!mem' in message.text.lower():
			memasik(message)
		if '!ьуь' in message.text.lower():
			memasik(message)
		if '!v\'v' in message.text.lower():
			memasik(message)
		if '!мэм' in message.text.lower():
			memasik(message)
		for hor in goroskop.hor_sign: #гороскоп
			if hor in message.text.lower():
				goroskop_find(message)
		#поиск хоттаба в сообщении
		for xott in config.xottabb_call:
			if xott.lower() in message.text.lower():
				url_xott = 'https://t.me/'+config.group_name+'/'+str(message.message_id)
				bot.send_message(config.user_admin,url_xott)
		kalicalls(message)
		if '!зачисти меня' in message.text.lower():
			if config.user_admin in str(message.from_user.id):
				file_my_messageid = str(message.from_user.id)+'/'+str(message.chat.id)
				o = open(file_my_messageid,'r', encoding = "utf-8")
				list_w_msgid = list(o)
				o.close()
				bot.send_message(message.chat.id,'В процессе...👌😎')

				bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAIvf186Y04jtQ5aLaTxk8pkr5jPUoF5AAL3AAOVyisJUbFxILdSrHsaBA')
				for i in list_w_msgid:
					current_id = clean_enter(i)
					try:
						bot.delete_message(message.chat.id,current_id)
						print ('Deleted message id:  ',current_id)
					except:
						pass
				o = open(file_my_messageid,'w+', encoding = "utf-8")
				o.write(file_my_messageid,'')
				o.close()

			pass
		if '!пнуть' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.pinaet)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user
			bot.send_message(message.chat.id,fraze_with_names)
		if '!прижаться' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.prijatsya)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user
			bot.send_message(message.chat.id,fraze_with_names)
		if '!шлепнуть' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.shlepok)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user
			bot.send_message(message.chat.id,fraze_with_names)
		if '!ливнуть' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.livnut)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user
			bot.send_message(message.chat.id,fraze_with_names)
		if '!обидеться' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.obidka)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user
			bot.send_message(message.chat.id,fraze_with_names)
		if '!выписать леща' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.leshadat)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user
			bot.send_sticker(message.chat.id,'CAACAgQAAxkBAAIvel86YUf7C7rp7XM6kF39l26vt0HYAAIiAANfxgEZ8_q_s-6jQF4aBA')
			bot.send_message(message.chat.id,fraze_with_names)
		if '!дать по ебалу' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.poibaly)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user+'☠️'
			bot.send_sticker(message.chat.id,'CAACAgQAAxkBAAIvfF86YhFVxd6dsxBZSM5wVMS6XpFWAAK6AANLae4QLyrtpzRxYGcaBA')
			bot.send_message(message.chat.id,fraze_with_names)
		if '!отпиздить' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.poibaly)
			fraze_with_names = '@'+main_user+fraze_to_action_one+'@'+reply_user+'☠️'
			bot.send_sticker(message.chat.id,'CAACAgQAAxkBAAIvfF86YhFVxd6dsxBZSM5wVMS6XpFWAAK6AANLae4QLyrtpzRxYGcaBA')
			bot.send_message(message.chat.id,fraze_with_names)
		if '!улыбнуться' in message.text.lower():
			if namehere == 1:
				reply_user = reply_user
			else:
				reply_user = select_fr(regularfrazes.command_names)
			fraze_to_action_one = select_fr(regularfrazes.ulybka)
			fraze_with_names = fraze_to_action_one
			bot.send_message(message.chat.id,fraze_with_names)
		if '!отжаться' in message.text.lower():
			bot.send_animation(message.chat.id,'https://i.gifer.com/1AnC.gif')
		if '???' in message.text.lower():
			bot.send_animation(message.chat.id,'http://hostsite.asuscomm.com/wp-content/uploads/2020/08/giphy.mp4')
		if '!психануть' in message.text.lower():
			bot.send_animation(message.chat.id,'https://i.gifer.com/MbE2.gif')
		if '!чай с мятой' in message.text.lower():
			bot.send_animation(message.chat.id,'https://sp.mycdn.me/image?id=873850158649&t=44&plc=WEB&tkn=*jLIdjG5_hOrmiQe-mhc8bZ-WhJ4')
		if '!по жопе' in message.text.lower():
			nowgif = select_fr(regularfrazes.pojope)
			bot.send_animation(message.chat.id,nowgif)
		if 'красивыедевушки' in message.text.lower():
			nowgifcoolgirls = select_fr(regularfrazes.hashcoolgirls)
			bot.send_animation(message.chat.id,nowgifcoolgirls)
		if 'девушкикрасивые' in message.text.lower():
			nowgifcoolgirls = select_fr(regularfrazes.hashcoolgirls)
			bot.send_animation(message.chat.id,nowgifcoolgirls)
		if 'красивыеунасдевушки' in message.text.lower():
			nowgifcoolgirls = select_fr(regularfrazes.hashcoolgirls)
			bot.send_animation(message.chat.id,nowgifcoolgirls)
		if 'девушкиунаскрасивые' in message.text.lower():
			nowgifcoolgirls = select_fr(regularfrazes.hashcoolgirls)
			bot.send_animation(message.chat.id,nowgifcoolgirls)
	except Exception as e:
		print("ActionsErrrror: ", e)
		logging("ERROR_ACTION",e)
		pass
#__________________погодно-температурные функции_______________
	try:
		if '!температура' in message.text.lower():
			url_temp = "http://narodmon.ru/api?cmd=sensorsValues&sensors=34535&uuid=6b490fc3b811077028515b8d1bf2ab63&api_key=f1t3tKsbNbxmZ&lang=ru"
			temp_ken = any_get_all(url_temp)
			#print(str(temp_ken))
			resp = json.loads(temp_ken)["sensors"][0]["value"]
			#print(str(resp))
			modtemp_all = int((str(resp).split("."))[1])
			#print(str(modtemp_all))
			if modtemp_all >= 50:
				temp_all = str(int((str(resp).split("."))[0])+1)
			else:
				temp_all = str((str(resp).split("."))[0])
			if int(temp_all) in [1,21,31,41,51,61,71,81,91]:
				unt_t = " градус"
			elif int (temp_all) in [2,3,4,22,23,24,32,33,34,42,43,44,52,53,54,62,63,64,72,73,74,82,83,84,92,93,94]:
				unt_t = " градуса"
			else:
				unt_t = " градусов"
			temp_all = "`В Калининграде` *"+str(temp_all)+"*`"+unt_t+' по Цельсию.`'
			#print(str(temp_all))
			bot.send_message(message.chat.id,temp_all,parse_mode="Markdown")

	except Exception as e:
		print("WeatherError: ", e)
		logging("ERROR_WEATHER",e)
		bot.send_message(message.chat.id,'`Не удалось запросить данные...`',parse_mode="Markdown")

	try:
		if '!погода' in message.text.lower():
			url_temp = "http://narodmon.ru/api?cmd=sensorsValues&sensors=34535&uuid=6b490fc3b811077028515b8d1bf2ab63&api_key=f1t3tKsbNbxmZ&lang=ru"
			temp_ken = any_get_all(url_temp)
			resp = json.loads(temp_ken)["sensors"][0]["value"]
			modtemp_all = int((str(resp).split("."))[1])
			if modtemp_all >= 50:
				temp_all = str(int((str(resp).split("."))[0])+1)
			else:
				temp_all = str((str(resp).split("."))[0])
			res = requests.get("http://api.openweathermap.org/data/2.5/weather",
						params={'id': '554234', 'units': 'metric', 'lang': 'ru', 'APPID':										 '698628cf3d7857768c93a777115bb876'})
			data = res.json()
			conditions = data['weather'][0]['description']
			temp_weath = temp_all#data['main']['temp']
			temp_min = data['main']['temp_min']
			temp_max = data['main']['temp_max']
			humidity = data['main']['humidity']
			wind = data['wind']['speed']
			pipinclothes = ""
			if int(temp_weath) >= 19 and wind <= 5:
				pipinclothes = '@pipinsorry`, сегодня можно и в футболке`👌'
			elif int(temp_weath) <= 18:
				pipinclothes = '@pipinsorry`, ну нафиг. Одевайся теплее! Пока бананчики не отмерзли.`'
			elif int(temp_weath) >= 28:
				pipinclothes = '@pipinsorry`, там пекло ипаное, можно вообще без футболки идти!`😝'
			elif int(temp_weath) >= 19 and wind >= 5:
				pipinclothes = '@pipinsorry`, сегодня наверное можно и в футболке`👌`, но ветерок сильный. В общем, я неуверен как 16-летняя девочка`🙊'
			elif int(temp_weath) >= 19 and wind >= 5:
				pipinclothes = '@pipinsorry`, сегодня наверное можно и в футболке`👌`, но ветерок сильный. В общем, я неуверен как 16-летняя девочка`🙊'
			else:
				pipinclothes = '@pipinsorry`, ну нафиг. Одевайся теплее! Пока бананчики не отмерзли.`👀'
			if 'дожд' in str(conditions):
				pipinclothes = pipinclothes+'` А еще зонтик возьми или капюшон. Сегодня кто-то промокнет.`😏'
			else:
				pipinclothes = pipinclothes
			str_weather = '_Погода в Калининграде (Сейчас):_\n🌡*Текущая температура: '+str(temp_weath)+'°C*\n🌡Температура (мин): '+str(temp_min)+' °C\n🌡Температура (макс): '+str(temp_max)+' °C\n💧Влажность: '+str(humidity)+' %\n💨Ветер: '+str(wind)+' м/с\n🌤'+str(conditions)+'\n'+pipinclothes
			bot.send_message(message.chat.id,str_weather,parse_mode="Markdown")
	except Exception as e:
		print("Exception (weather):", e)
		logging("ERROR_(WEATHER)",e)
		bot.send_message(message.chat.id,'Не удалось запросить данные...')

	try:
		if message.text.lower() == '!прогноз3':
			res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
						params={'id': '554234', 'units': 'metric', 'lang': 'ru', 'APPID':										 '698628cf3d7857768c93a777115bb876'})
			day=1
			bot.send_message(message.chat.id,'_Прогноз погоды на 3 дня:_',parse_mode="Markdown")
			while day < 21:
				data = res.json()
				date_weath = data['list'][day]['dt_txt']
				time_weather = date_weath.split(' ')[1]
				if '15:00:00' in time_weather:
					date_weather = date_weath.split(' ')[0]
					hour_weather = time_weather.split(':')[0]
					minut_weather = time_weather.split(':')[1]
					day_weater = date_weather.split('-')[2]
					month_weater = date_weather.split('-')[1]
					year_weater = date_weather.split('-')[0]
					conditions = data['list'][day]['weather'][0]['description']
					temp_weath = data['list'][day]['main']['temp']
					temp_min = data['list'][day]['main']['temp_min']
					temp_max = data['list'][day]['main']['temp_max']
					humidity = data['list'][day]['main']['humidity']
					wind = data['list'][day]['wind']['speed']
					str_weather = '⏳'+day_weater+'.'+month_weater+'.'+year_weater+':\n🌡*T°: '+str(temp_weath)+' °C*\n🌡T°(днём): '+str(temp_min)+' °C ... '+str(temp_max)+' °C\n💧Влажность: '+str(humidity)+' %   💨Ветер: '+str(wind)+' м/с\n🌤'+str(conditions)
					bot.send_message(message.chat.id,str_weather,parse_mode="Markdown")
				else:
					pass
				day=day+1#8
		if message.text.lower() == '!прогноз5':
			res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
						params={'id': '554234', 'units': 'metric', 'lang': 'ru', 'APPID':										 '698628cf3d7857768c93a777115bb876'})
			day=1
			bot.send_message(message.chat.id,'_Прогноз погоды на 5 дней:_',parse_mode="Markdown")
			while day < 37:
				data = res.json()
				date_weath = data['list'][day]['dt_txt']
				time_weather = date_weath.split(' ')[1]
				if '15:00:00' in time_weather:
					date_weather = date_weath.split(' ')[0]
					hour_weather = time_weather.split(':')[0]
					minut_weather = time_weather.split(':')[1]
					day_weater = date_weather.split('-')[2]
					month_weater = date_weather.split('-')[1]
					year_weater = date_weather.split('-')[0]
					conditions = data['list'][day]['weather'][0]['description']
					temp_weath = data['list'][day]['main']['temp']
					temp_min = data['list'][day]['main']['temp_min']
					temp_max = data['list'][day]['main']['temp_max']
					humidity = data['list'][day]['main']['humidity']
					wind = data['list'][day]['wind']['speed']
					str_weather = '⏳'+day_weater+'.'+month_weater+'.'+year_weater+':\n🌡*T°: '+str(temp_weath)+' °C*\n🌡T°(днём): '+str(temp_min)+' °C ... '+str(temp_max)+' °C\n💧Влажность: '+str(humidity)+' %   💨Ветер: '+str(wind)+' м/с\n🌤'+str(conditions)
					bot.send_message(message.chat.id,str_weather,parse_mode="Markdown")
				else:
					pass
				day=day+1
		if message.text.lower() == '!прогноз':
			res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
						params={'id': '554234', 'units': 'metric', 'lang': 'ru', 'APPID':										 '698628cf3d7857768c93a777115bb876'})
			day=1
			bot.send_message(message.chat.id,'_Прогноз погоды на сегодня:_',parse_mode="Markdown")
			while day < 8:
				data = res.json()
				date_weath = data['list'][day]['dt_txt']
				time_weather = date_weath.split(' ')[1]
				date_weather = date_weath.split(' ')[0]
				hour_weather = time_weather.split(':')[0]
				minut_weather = time_weather.split(':')[1]
				day_weater = date_weather.split('-')[2]
				month_weater = date_weather.split('-')[1]
				year_weater = date_weather.split('-')[0]
				conditions = data['list'][day]['weather'][0]['description']
				temp_weath = data['list'][day]['main']['temp']
				temp_min = data['list'][day]['main']['temp_min']
				temp_max = data['list'][day]['main']['temp_max']
				humidity = data['list'][day]['main']['humidity']
				wind = data['list'][day]['wind']['speed']
				str_weather = '⏳_'+hour_weather+'ч. '+minut_weather+'м. '+'  '+day_weater+'.'+month_weater+'.'+year_weater+':_\n🌡*T°: '+str(temp_weath)+' °C*\n🌡T°(мин): '+str(temp_min)+' °C   🌡T°(макс): '+str(temp_max)+' °C\n💧Влажность: '+str(humidity)+' %   💨Ветер: '+str(wind)+' м/с\n🌤'+str(conditions)
				bot.send_message(message.chat.id,str_weather,parse_mode="Markdown")
				day=day+2
	except Exception as e:
		print("Exception (weather):", e)
		logging("ERROR_(WEATHER)",e)
		bot.send_message(message.chat.id,'Не удалось запросить данные...')
#_____________конец погодно-температурных функций_____________

#______________убийца по команде__________________
	if '!pkill' in message.text.lower():
		str_pkill = 'Process named "User" with PID '+str(message.reply_to_message.from_user.id)+' is stopped.'
		xottabbmagic(message,str_pkill,'No processes for kill... Command failed.')
		pkill_list = ['CAACAgIAAx0CSiOOwwACCjdf4FjfxroGNSv2bwXr25PcP9Gb7wACSwIAAsG90QUkcrgqNtoWQR4E','CAACAgIAAx0CSiOOwwACCjVf4FjQy4IqXzL5ozCgfXRnDUHTmgACYAEAAsG90QXagUGr5nJAXR4E','CAACAgIAAx0CSiOOwwACCjNf4Fi_UOEDE4OKE8YpLZ-3rgABH1wAAlEBAALBvdEFfTkYXUspfzkeBA','CAACAgIAAx0CSiOOwwACCjFf4Fi6bgS35M7jP45SBaT5hF3DKwACNAADK-0ZAAGfgIlwL7eH0x4E','CAACAgIAAx0CSiOOwwACCjlf4Fjv0pkbE5mTqioJF6CXZcZVtQACKgADK-0ZAAHwqC4sEu9tlB4E']
		sticker_pkill = str(pkill_list[randrange(0,len(pkill_list)-1)])
		bot.send_sticker(message.chat.id,sticker_pkill)
	if '!фас' in message.text.lower():
		fas(message)
	if '!взять' in message.text.lower():
		fas(message)
	if '!захват' in message.text.lower():
		fas(message)
	if '!задержать' in message.text.lower():
		fas(message)
	if 'кикус мортале' in message.text.lower():
		xottabbmagic(message,'Слушаюсь и повинуюсь, господин Xottabb14!😇 Пшел нах отсюда!🤬 Кияк!','О, величайший джин, сначала выберите жертву!👀')
		bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAIval86WX27ZFNGCHWW5MFB3xHAup-cAAIwBQACH7sgB2q2aN7uN9b8GgQ')
	if 'авада кедавра' in message.text.lower():
		xottabbmagic(message,'Сдохни, жалкий магл!🤓 Кик!','Пожиратели смерти одобряют убийство.☠️ Только кого?')
		bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAIvZ186WB3w8dSd37p3Ox1dc5gQgTKkAALIAgACz1-LB0wuBy_XOD8bGgQ')
	if 'вспышкус гробулис' in message.text.lower():
		xottabbmagic(message,'Шмыгус сморкатис! Искрис фронтис! Короче, сдохни!💩','Колечко наготове. Осталось выбрать лопухоида для кика...👻')
		bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAIvaF86WMZjazj4JaO0jrRq4lT-9rkxAALYAQACygMGC4QG-q8znjA4GgQ')
	if 'переебус поебалус' in message.text.lower():
		xottabbmagic(message,'Нах#й отсюда!!!!🤬🤬🤬','Спокойствие. Заклинания надо юзать на ком то из этих мерзких людишек. Выбирайте, сэр!😏')
		bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAIvaV86WP6yH-QhtHBm6jEXIiASemiyAAJeAgACPnKoEbwfe6eMUUkyGgQ')
	if 'простоидинахуй' in message.text.lower():
		xottabbmagic(message,'Просто иди на хуй отсюда!!!! Заебали!!!🤬🤬🤬','На хуй надо слать кого-то, а не в пустоту писькой болтать!😏')
		bot.send_sticker(message.chat.id,'CAACAgIAAx0CSiOOwwACB3tfs8uL1l3iVxaFlmB1WY0aoPX9aQACxAIAAladvQotLPt8J_pZMR4E')
	if 'простонахуй' in message.text.lower():
		xottabbmagic(message,'Просто иди на хуй отсюда!!!! Заебали!!!🤬🤬🤬','На хуй надо слать кого-то, а не в пустоту писькой болтать!😏')
		bot.send_sticker(message.chat.id,'CAACAgIAAx0CSiOOwwACB3tfs8uL1l3iVxaFlmB1WY0aoPX9aQACxAIAAladvQotLPt8J_pZMR4E')
	if '!отвратительно' in message.text.lower():
		badcontent(message)
	if '!jndhfnbntkmyj' in message.text.lower():
		badcontent(message)
	if '!ufdyj' in message.text.lower():
		badcontent(message)
	if '!гавно' in message.text.lower():
		badcontent(message)
	if '!удоли' in message.text.lower():
		if rulles(message) == True:
			try:
				delmessage(message)
			except:
				bot.send_message(message.chat.id,'Что удОлять то?🤦‍♂️')
		else:
			pass
		if modrulles(message) == True:
			try:
				delmessage(message)
			except:
				bot.send_message(message.chat.id,'Что удОлять то?🤦‍♂️')
		else:
			pass
	if '!удали' in message.text.lower():
		if rulles(message) == True:
			try:
				delmessage(message)
			except:
				bot.send_message(message.chat.id,'Что удОлять то?🤦‍♂️')
		else:
			pass
		if modrulles(message) == True:
			try:
				delmessage(message)
			except:
				bot.send_message(message.chat.id,'Что удОлять то?🤦‍♂️')
		else:
			pass
	if '!del' in message.text.lower():
		if rulles(message) == True:
			try:
				delmessage(message)
			except:
				bot.send_message(message.chat.id,'Что удОлять то?🤦‍♂️')
		else:
			pass
		if modrulles(message) == True:
			try:
				delmessage(message)
			except:
				bot.send_message(message.chat.id,'Что удОлять то?🤦‍♂️')
		else:
			pass
	if '!delete' in message.text.lower():
		if rulles(message) == True:
			try:
				delmessage(message)
			except:
				bot.send_message(message.chat.id,'Что удОлять то?🤦‍♂️')
		else:
			pass
		if modrulles(message) == True:
			try:
				delmessage(message)
			except:
				bot.send_message(message.chat.id,'Что удОлять то?🤦‍♂️')
		else:
			pass

	#_____________________antispam!!!!!!!!!!!!!!!!!!!!!!!
	f_spam = open('spamtext.ii', "r", encoding = "utf-8") #открываем файл в режиме чтения
	spam_strings = list(f_spam)
	f_spam.close() #закрываем файл
	for spm in spam_strings:
		spm_noent = clean_enter(spm)
		if spm_noent.lower() in message.text.lower():#'нужны люди для переводов с бк и казино'
			try:
				kickspamer(message)
			except:
				pass
	f_porn = open('porntext.ii', "r", encoding = "utf-8")
	porn_strings = list(f_porn)
	f_porn.close() #закрываем файл
	for porn in porn_strings:
		porn_noent = clean_enter(porn)
		if porn_noent.lower() in message.text.lower():#'нужны люди для переводов с бк и казино'
			try:
				bot.delete_message(message.chat.id,message.message_id)
			except:
				pass
	if 'алиханов' in message.text.lower():
		alixanov_list = ['CAACAgIAAxkBAAI0G19JAAEx8-ydkd5JXg0_jJH_MBR5IQACSgUAAh-7IAdtSP_3sVw12BsE','CAACAgIAAxkBAAI0HF9JAAEzzzfKmlZRvmtNrqfbRoxq6QACTAUAAh-7IAc9yZxprfK3PxsE']
		alixanov_stckr = select_fr(alixanov_list)
		bot.send_sticker(message.chat.id,alixanov_stckr)
	if 'здрасте' in message.text.lower():
		bot.send_sticker(message.chat.id,'CAACAgIAAx0CSiOOwwACCc9f0kC7-QUgUPC7h4Xcq_u5hd9h7QACvQEAAodOegRZ-IPv6UwfFR4E',reply_to_message_id=message.message_id)
	if 'здрасти' in message.text.lower():
		bot.send_sticker(message.chat.id,'CAACAgIAAx0CSiOOwwACCc9f0kC7-QUgUPC7h4Xcq_u5hd9h7QACvQEAAodOegRZ-IPv6UwfFR4E',reply_to_message_id=message.message_id)
	try:
		if config.test_chat	in str(message.chat.id):
			if 'CAACAg' in str(message.text):
				try:
					list_idsh = str(message.text).split('\n')
					if len(list_idsh)>=1:
						for i in list_idsh:
							bot.send_sticker(config.test_chat,str(i))
							bot.send_message(config.test_chat,(i))
				except:
					idsh = str(message.text).replace('\n','')
					bot.send_sticker(config.test_chat,str(idsh),reply_to_message_id=message.message_id)
	except:
		pass
	if 'выходной' in message.text.lower():
		weekdayss = select_fr(regularfrazes.weekdays)
		if int(datetime.datetime.today().weekday()) < 5:
			#print (int(datetime.datetime.today().weekday()))
			bot.send_message(message.chat.id,weekdayss,reply_to_message_id=message.message_id)
			#bot.send_message(user_admin,weekdayss,reply_to_message_id=message.message_id)
		else:
			pass
	if '!утихомирить' in message.text.lower():
		timeban(message,1800,'30')
	if '!угомонить' in message.text.lower():
		timeban(message,1800,'30')
	if '!бесишь' in message.text.lower():
		timeban(message,300,'5')
	if '!нахуй' in message.text.lower():
		timeban(message,300,'5')
	if '!на хуй' in message.text.lower():
		timeban(message,300,'5')
	if '!заткнись' in message.text.lower():
		timeban(message,600,'10')
	if '!сладкихпупсик' in message.text.lower():
		timeban(message,28800,'480')
	if '!айдишник' in message.text.lower():
		try:
			if rulles(message) == True:
				bot.send_message(message.from_user.id,message.reply_to_message.from_user.id)
				bot.send_message(message.chat.id,'Ага, скинул. Глянь в личку...',reply_to_message_id=message.message_id)
		except:
			pass
	if '!верни' in message.text.lower():
		try:
			if rulles(message) == True:
				bot.restrict_chat_member(chat_idwork,message.reply_to_message.from_user.id,can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True,can_add_web_page_previews=True)
				bot.send_message(message.chat.id,'Пользователь разбанен...',reply_to_message_id=message.message_id)
			else:
				bot.send_message(message.chat.id,'Не положено!',reply_to_message_id=message.message_id)
		except:
			pass
	if '!разбань' in message.text.lower():
		try:
			if rulles(message) == True:
				bot.restrict_chat_member(chat_idwork,message.reply_to_message.from_user.id,can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True,can_add_web_page_previews=True)
				bot.send_message(message.chat.id,'Пользователь разбанен...',reply_to_message_id=message.message_id)
			else:
				bot.send_message(message.chat.id,'Не положено!',reply_to_message_id=message.message_id)
		except:
			pass
	meeteng_io_meet = known_fr('meetIO.ii')
	if meeteng_io_meet == "ON":
		meeterid = known_fr('meeter.ii')
		if int(meeterid) == int(message.from_user.id):
			if 'отмена' in message.text.lower():
				known_fw('OFF','meetIO.ii')
				bot.send_message(message.chat.id,"Ок. Встреча отменена")
			else:
				date_meet_now = known_fr('daymeet.ii')
				name_meeter = "Anonim"
				if "None" in str(message.from_user.username):
					name_meeter = '#'+str(message.from_user.first_name)
				else:
					name_meeter = '@'+str(message.from_user.username)
				location_meet = message.text
				message_meet_ended = message_meet_ended = 'Внимание! Объявлена сходка!\n😎Встречу назначил(а): '+name_meeter+'\n⏰Время встречи: '+date_meet_now+'\n📌Подробности: '+location_meet+'\n👌Пойти согласились:\n'+name_meeter
				keyboard_igo = types.InlineKeyboardMarkup()
				igo_butt = types.InlineKeyboardButton(text='Я буду👻', callback_data='igomeet')
				keyboard_igo.add(igo_butt)
				bot.send_message(message.chat.id,message_meet_ended,reply_markup=keyboard_igo)
				mse_id = str(int(message.message_id)+1)
				known_fw(mse_id,'MSGforEditMeet.ii')
				known_fw(message_meet_ended,'MSGfortextMeet.ii')
				known_fw('OFF','meetIO.ii')
				bot.pin_chat_message(message.chat.id, mse_id, disable_notification=True)
		else:
			pass#print ('notOK')
	else:
		pass
#main___reactions_____
def main_iishka_reaction(message):
		if 'или' in message.text.lower():
			or_text = clean_iishka (message.text)
			or_textSym = clean_text (or_text)
			or_textL = or_textSym.split(' или ')
			or_rand = randrange(0,2)
			or_startss = select_fr(regularfrazes.or_starts)
			or_fraze =or_startss+str(or_textL[or_rand])
			bot.send_message(message.chat.id,or_fraze,reply_to_message_id=message.message_id)
		elif 'or' in message.text.lower():
			or_text = clean_iishka (message.text)
			or_textSym = clean_text (or_text)
			or_textL = or_textSym.split(' or ')
			or_rand = randrange(0,2)
			or_startss = select_fr(regularfrazes.or_starts)
			or_fraze =or_startss+str(or_textL[or_rand])
			bot.send_message(message.chat.id,or_fraze,reply_to_message_id=message.message_id)
		elif 'запиши в памят' in message.text.lower():
			text_to_write = '>>>'+message.reply_to_message.text+'\n'
			f = open('memory.ii', "a", encoding = "utf-8") #открываем файл в режиме дозаписи
			f.write(text_to_write)
			f.close()
			text_to_writeN = '`Записал следующее: `'+clean_enter(text_to_write)
			bot.send_message(message.chat.id,text_to_writeN,reply_to_message_id=message.message_id,parse_mode="Markdown")
		elif 'память чата' in message.text.lower():
			f = open('memory.ii', "r", encoding = "utf-8") #открываем файл в режиме чтения
			mem_string = f.read()
			mem_stringpl = '`В памяти чата есть следующие записи:`\n'+mem_string
			f.close() #закрываем файл
			bot.send_message(message.chat.id,mem_stringpl,reply_to_message_id=message.message_id,parse_mode="Markdown")
		elif 'удали из памяти' in message.text:
			f = open('memory.ii', "r", encoding = "utf-8") #открываем файл в режиме чтения
			del_string = f.read()
			f.close() #закрываем файл
			rep_string = (message.text).replace('удали из памяти ', '')
			rep_stringg = '>>>'+clean_iishka(rep_string)+'\n'
			f = open('memory.ii', "w+", encoding = "utf-8") #открываем файл в режиме перезаписи
			wr_string = del_string.replace(rep_stringg, '')
			f.write(wr_string)
			f.close() #закрываем файл
			bot.send_message(message.chat.id,'Удалил начисто😎',reply_to_message_id=message.message_id)
		else:
			word_list(message)
#бот реагирует на все сообщения
@bot.message_handler(content_types=["text"])
def search_namebot(message):
	try:
		if '-484910233' in str(message.chat.id):
			bot.send_message(chat_idwork,message.text)
		#print (message.text,'   ',message.message_id)
		if user_admin in str(message.chat.id):
			print (message.text)
		if rulles(message) == True:
			mymessageid = str(message.message_id)+'\n'
			file_my_messageid = str(message.from_user.id)+'/'+str(message.chat.id)
			o = open(file_my_messageid,'a', encoding = "utf-8")
			o.write(mymessageid)
			o.close()
		
		if 'иишка' in message.text.lower(): #'ИИшка' in - добавить переде message, чтобы откликался только на имя
			main_iishka_reaction(message)
		else:
			try:
				#bot.send_message(user_admin,str(message.reply_to_message.from_user.username))
				if "iishka_bot" in str(message.reply_to_message.from_user.username):
					main_iishka_reaction(message)
				else:
					pass
			except Exception as e:
				pass#bot.send_message(user_admin,str(e))
		regularfrazesdef(message)
	except Exception as e:
		print("ExceptionALL: ", e)
		logging("ERROR_ALL",e)

#новогодний cron
def new_year_cron(chat_chron_id,timedate_tocron):
	while True:
		try:
			h_cron = int(time.strftime("%H", time.localtime()))+7 #текущий час
			m_cron = int(time.strftime("%M", time.localtime())) #текущая минута
			month_chrom = int(time.strftime("%m", time.localtime())) #текущий месяц
			day_chrom = int(time.strftime("%d", time.localtime())) #текущий день
					
			if h_cron == int(timedate_tocron[0]) and m_cron == int(timedate_tocron[1]):
				if month_chrom == int(timedate_tocron[3]) and day_chrom == int(timedate_tocron[2]):
					nowgif = 'BQACAgIAAxkBAAJlhF_jpdlutPJxspqoCIlhan_WgpKKAAIUCAAC6M4gS_k_eWC2OeGOHgQ'
					bot.send_animation(chat_chron_id,nowgif)
					ny_str = readfile('newyear.txt')
					bot.send_message(chat_chron_id,ny_str,parse_mode="Markdown")
					bot.send_audio(chat_chron_id,'CQACAgIAAxkBAAJlbF_jktCNw3XiT2bBNNqq-B7ZFBxDAAKnCgAC6M4YS_8oEh0Z2n98HgQ')
		except Exception as err:
			print ('CRON ERROR NY:>>>>>>>  ',str(err))
			logging("ERROR_CRON_NY",err)
		time.sleep(60)

def covid_cron(chat_chron_id,h_act,m_act):
	while True:
		try:
			h_cron = int(time.strftime("%H", time.localtime()))+7
			m_cron = int(time.strftime("%M", time.localtime()))
			
			if h_cron == h_act and m_cron == m_act:
				covid(chat_chron_id,"Ежедневные данные по COVID-19\nв Калининградской области:")
		except Exception as err:
			print ('CRON ERROR:>>>>>>>  ',str(err))
			logging("ERROR_CRON",err)
		time.sleep(60)
#Ковидный хрон на каждый день, выключается в конфиге
if config.covid_eday == 1:
	p = Process(target=covid_cron, args=(chat_idwork,15,10))
	p.start()
else:
	print('Cron Covid Stoped...')

timedate_tocron = ['00','00','01','01','2021'] #время сработки хрона для НГ ЧЧ,ММ,ДД,МС,ГГ
#timedate_tocron = ['20','59','23','12','2020'] #время сработки хрона для НГ
pny = Process(target=new_year_cron, args=(chat_idwork,timedate_tocron)) #args=(chat_idwork,15,10))
pny.start()

while True:
	try:
		if __name__ == '__main__':
			#wakie_time_bud()
			bot.polling(none_stop=True) #бесконечное получение новых записей от Телеграм
	except Exception as err:
		print ('Its bad moment with ERROR:>>>>>>>  ',str(err))
		logging("ERROR_CRITICAL",err)
