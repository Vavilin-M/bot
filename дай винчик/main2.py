from classes import *

import vk_api
token = "token"
from vk_api.longpoll import VkLongPoll, VkEventType
vk_session = vk_api.VkApi(token=token)
from random import randint
import sqlite3
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

conn = sqlite3.connect("db.db")
cursor = conn.cursor()
# Получаем первоначальные данные отправителя сообщения
# Заносим первоначальные данные в базу данных
# Если такое данное есть - пропускаем
# Если нет - просим заполнить
# Когда пришло данное - редактируем строку данных пользователя в базе данных

array_likes = []
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:	
        count_likes_me = 0
        #Инциализируем класс для получения данных о сообщении
        id_sender = GetMessage(event.message_id)
        #from_id - id пользователя, с которым работаем
        from_id = id_sender.user_id()
        #Инициализируем класс для отправки сообщений пользователю
        send = Send(from_id)
        
        #Инициализируем класс для проверки, создан ли аккаунт пользователя. 
        check_db = Check(from_id)
        
        #Если анкета не создана, check_db.check() вернет False
        if check_db.check() == False:
            #Получаем имя пользователя, пол
            user = User(from_id)
            #Имя пользователя:
            first_name = user.first_name()
            #Пол пользователя
            sex = user.sex()
            #Класс для получения фотографии
            userPhoto = UserPhoto(from_id)
            #Здесь возвращаем строку с аттачмент
            user_avatar = userPhoto.result()
            #Вносим данные в базу
            cursor.execute(f"INSERT INTO users (user_id, bot_user_name, sex, activate, avatar) VALUES ('{from_id}', '{first_name}', '{sex}', '1', '{user_avatar}')")
            #Сохраняем изменения в базе
            conn.commit()
            #Отправляем первое сообщение
            send.sending(message="Привет! Начало твоей анкеты положено! Давай начнем заполнять анкету? Напиши свой город, в котором будем искать тебе друзей!")
        else:
            #Если пользователь создан или если check_db.check() == True
            #Проверяем каких данных у пользователя не хватает
            #Проверяем, есть ли город

            #Инициализируем проверку на нехватку данных
            missing = WhatIsMissing(from_id)
            #Если города нет - city() = False
            if missing.city() == False:
                #Вызываем метод добавления города в БД
                missing.updateCity(event.text)
                #Отправляем сообщение с просьбой написать возраст
                send.sending(message="Принял! Напиши, пожалуйста, свой возраст!")
            
            #elif, потому что нужно идти последовательно
            
            #Если не указан возраст
            elif missing.age() == False:
                #Пытаемся обновить возраст
                missing.updateAge(event.text, from_id)
                #Дополнение: если обновить не удалось, отправляем сообщение, с просьбой написать число
            
            #Если описание отсутствует
            elif missing.description() == False:
            	#Добавляем в описание отправленный текст
                missing.updateDescription(event.text)
                #Отправляем сообщение для выбора парня или девушки
                send.sending(message = "Принял, осталось понять, кого ищем:\n 1.Девушку \n2.Парня\n3.Всё равно")

            #Если половые предпочтения отсутствуют
            elif missing.sex_search() == False:
        	    #Обновляем данные в базе
                missing.updateSex_search(event.text)
                #Дополнение: если там не цифры, то будем просить ввести цифры        
            elif event.text == '1' or event.text == '2' or event.text == '❤' or event.text == '👎🏻':
                #Инициализируем класс вывода анкет
                output = Output(from_id)
                #Получаем данные о пользователе
                user = User(from_id)
                #Получаем свой пол
                sex = user.sex()
                #Объявляем метод получения id нужных пользователей
                output.selectAll(sex)
                #Если id получено
                get_id = output.getRandomId(sex)
                #Класс для проверки, есть ли люди, которые меня лайкнули
                someoneLikesMe = SomeoneLikesMe(from_id)
                #Запускаем проверку. Должны вернуть массив
                array = (someoneLikesMe.returnArray(from_id))
                #Если нам действительно вернули массив
                print(someoneLikesMe.returnArray(from_id))
                if someoneLikesMe.returnArray(from_id) != False and someoneLikesMe.returnArray(from_id) != []:
                    #Проходимся по массиву
                    for i in array:
                        #Присваиваем get_id последующий элемент массива
                        get_id = array[count_likes_me]
                        #На следующий раз уже будет брать следующий элемент
                        count_likes_me += 1
                        #Обновляем статус в базе данных на 3
                        cursor.execute(f"UPDATE inquiries SET 'status' = '3' WHERE user_2 = '{from_id}' AND user_1 = '{get_id}'")
                        #Сохраняем
                        conn.commit()
                    #Берем даные из базы с полученным id
                    row = cursor.execute(f"SELECT * FROM users WHERE user_id = '{get_id}'")
                    #Оставляем первую попавшуюся
                    row = cursor.fetchone()
                    #Отправляем сообщение
                    if row[11] != "None" or row[11] != None: 
                    	#Если фотография есть, то отправляем сообщение с фотографией
                        send.sending(message=f"Ахринеть, ты кому-то понравился, смотри:\n {row[2]}, {row[4]}, {row[9]}.\n {row[5]}\n 1. Нравится\n 2.Не нравится" , attachment = row[11])
                    else:
                    	#Если фотографии нет, то отправляем сообщение без фотографии
                        send.sending(message=f"Ахринеть, ты кому-то понравился, смотри:\n {row[2]}, {row[4]}, {row[9]}.\n {row[5]}\n 1. Нравится\n 2.Не нравится")
                else:
                    #Берем даные из базы с полученным id
                    row = cursor.execute(f"SELECT * FROM users WHERE user_id = '{get_id}'")
                    #Оставляем первую попавшуюся
                    row = cursor.fetchone()
                    #Отправляем сообщение
                    if row[11] != "None" or row[11] != None: #Если фото есть, то отправляем с фото
                        send.sending(message=f"Hашел кое-кого для тебя, смотри:\n {row[2]}, {row[4]}, {row[9]}.\n {row[5]}\n 1. Нравится\n 2.Не нравится", attachment = row[11])
                    else: #Если фото нет, то отправляем без фото
                        send.sending(message=f"Hашел кое-кого для тебя, смотри:\n {row[2]}, {row[4]}, {row[9]}.\n {row[5]}\n 1. Нравится\n 2.Не нравится")

                if get_id != "Увы" and event.text == '1' or event.text == '2' or event.text == '❤' or event.text == '👎🏻':
                    #Добавляем в массив с id лайкнутых пользователей id лайкнутого пользователя
                    array_likes.append(get_id)
                    print(array_likes)
                    #Если нажата 1, значит наверное человек понравился
                    if get_id != "Увы" and (event.text == '1' or event.text == '❤'):
                        #Инициализируем класс понравившегося человека    
                        like = Like(from_id)
                        #Добавляем в базу человека, который нам понравился
                        like.inquiry(array_likes)
                        #Инициализация класса отправки сообщения обоим пользователям
                        sympathy = MutualSympathy(from_id)
                        sympathy.selectSympathy()
            else:
                send.sending(message="Пожалуйста, сообщи нам цифру или смайлик")
