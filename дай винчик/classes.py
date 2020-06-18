from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
token = "token"
vk_session = vk_api.VkApi(token=token)
from random import randint
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
import sqlite3
conn = sqlite3.connect("db.db")
cursor = conn.cursor()
#Создадим класс для отправки сообщения
class Send:
    def __init__(self, peer_id):
         self.peer_id = peer_id

    def sending(self, message,  attachment=None, intent=None, disable_mentions=None, dont_parse_links=None, forward_messages=None, keyboard=None, payload=None, sticker_id=None, domain=None, lat=None, long=None, reply_to=None): #Метод отправки сообщения
        result = vk.messages.send(message=message, peer_id=self.peer_id, random_id=randint(1, 489324892), reply_to=reply_to, forward_messages=forward_messages, attachment=attachment)
        return result

class User:
    def __init__(self, user_id):
        self.info = vk.users.get(user_ids=user_id, fields="sex")
        
    def last_name(self):
        last_name = self.info[0]['last_name']
        return last_name

    def first_name(self):
        first_name = self.info[0]['first_name']
        return first_name
    
    def sex(self):
        sex = self.info[0]['sex']
        return sex
    
    def user_id(self):
        user_id = self.info[0]['id']
        return user_id

#print(send.sending(message="Мое сообщение")) #Отправляем сообщение, возвращая id сообщения

class Guard:
    def __init__(self, message):
        self.message = message
    
    def guard(self):
        text = list(self.message)
        k = 0
        array_k = []
        count = 0 #Счетчик совпадений с матом
        for i in text:
            three_symbols = text[k:k+3] #Выводит по 3 символа массив
            string = "".join(three_symbols)
            array_three_symbols = ['бля', 'хуй', 'нах', 'еба', 'ебу', 'ебе', 'ебё', 'пиз', 'пид', 'ебо', 'хуи', 'хуе', 'хуё', 'ебл', 'уеб', 'уёб', 'дальше идуи с одной буквой латинской', 'бля', 'xуй', 'нaх', 'eба', 'eбу', 'eбе', 'eбё', 'пиз', 'пид', 'eбо', 'xуи', 'xуе', 'xуё', 'eбл', 'yеб', 'yёб', 'дальше со второй буквой латинской', 'бля', 'хуй', 'наx', 'ебa', 'ебy', 'ебe', 'ебё', 'пиз', 'пид', 'ебo', 'хyи', 'хyе', 'хyё', 'ебл', 'уeб', 'уёб', 'дальше полность. английские корни', 'бля', 'xyй', 'нax', 'eбa', 'eбy', 'eбe', 'eбё', 'пиз', 'пид', 'eбo', 'xyи', 'xye', 'xyё', 'eбл', 'yeб', 'yёб', 'hax', 'hах', 'hах']
            for j in array_three_symbols:
                if string.lower() == j.lower():
                    array_k.append(k)
                else:
                    continue
            k+=1
        #Чтобы удалять более точно, перевернем массив
        array_k.reverse()
        for number in array_k:
            text.pop(int(number))
            text.pop(int(number))
            text.pop(int(number))
            text.insert(number, "*")
            text.insert(int(number)+1, "*")
            text.insert(int(number)+2, "*")
        result = "".join(text)
        print(result)
        return result

class GetMessage:
    """
    КЛАСС ДЛЯ РАБОТЫ С СОБЩЕНИЯМИ

    Получаем основные данные(отправитель, id диалога, текст, дата отправленного сообщения)

    """
    def __init__(self, user_id):
        self.info = vk.messages.getById(message_ids=user_id, extended=1)

    def user_id(self):
        return self.info['items'][0]['from_id']

class Check:
    """Проверяем есть ли пользователь в бд
    Есть - True
    Нет - False
     """
    def __init__(self, user_id):
        self.user_id = user_id
    
    def check(self):
        #Обращаемся к базе данных
        row = cursor.execute(f"SELECT * FROM users WHERE user_id = '{self.user_id}'")
        #Получаем первую запись с id пользователя
        row = cursor.fetchone()
        #Если строки не существует, если ее не нашли
        if row is None: 
            return False
        else: #Иначе возвращаем тру
            return True

class WhatIsMissing:
    def __init__(self, user_id):
        #Получаем id пользователя для выборки из базы данных
        self.user_id = user_id
        #Выносим данные из базы
        self.row = cursor.execute(f"SELECT * FROM users WHERE user_id = '{self.user_id}'")
        #Берем первую попавшуюся нужную запись
        self.row = cursor.fetchone()

    #Проверяем, указан ли город
    def city(self):
        #Город не указан
        if self.row[9] == None:
            return False #Возвращаем False если не указан
        else: #Если указан
            return True #Возвращаем истину
    
    #Если город не указан, то будем вызывать этот метод, заносящий город в БД
    def updateCity(self, text):
        #Вносим изменения в столбец города
        cursor.execute(f"UPDATE users SET real_city = '{text}' WHERE user_id = '{self.user_id}'")
        #Сохраняем изменения
        conn.commit()

    #Проверяем указан ли возраст
    def age(self):
        #Возраст не указан
        if self.row[4] == None: #Если его не существует
            return False #Возвращаем False, если не указан
        else: #Если указан
            return True #Возвращаем истину
    
    #Если возраст не указан, то будем вызывать этот метод, заносящий возраст в БД
    
    def updateAge(self, text, user_id):
        #Если нам дали цифру
        if text.isnumeric() == True:
            #Обновляем столбик возраста базы данных на этот текст
            cursor.execute(f"UPDATE users SET age = '{text}' WHERE user_id = '{self.user_id}'")
            #Сохраняем изменения
            conn.commit()
            #Инициализируем класс отправки сообщени
            send = Send(user_id)
            #Отправляем сообщение с просьбой описать анкету
            send.sending(message = "Принято. Опиши, пожалуйста, свою анкету. Напиши что-нибудь о себе.")
        #Если нам дали не цифру
        else:
            #Инициализируем класс отправки сообщения
            send = Send(user_id)
            #Отправляем сообщение с просьбой написать число
            send.sending(message = "Пожалуйста, введите число")
    
    #Проверяем, указано ли описание анкеты
    def description(self):
        #Если не указано описание
        if self.row[5] == None:
            #Возвращаем False
            return False
        #Иначе
        else:
        #Возвращаем тру
            return True

    #Если описание не указано, будем вызывать этот метод, меняющий описание с None на текст 
    def updateDescription(self, text):
        #Вносим изменения в базу данных
        cursor.execute(f"UPDATE users SET description = '{text}' WHERE user_id = '{self.user_id}'")
        #Сохраняем изменения
        conn.commit()

    #Проверяем, указаны ли половые предпочтения
    def sex_search(self):
        #Если не существует
        if self.row[7] == None:
            #Возвращаем False
            return False
            #Иначе
        else:
            #Возвращаем True
            return True

    #Если половые предпочтения не указаны, вызываем эту функцию
    def updateSex_search(self, text):
        #Если выдали цифру 
        if text == '1' or text == '2' or text == '3':
            #Обновляем половые предпочтения в БД на нужные
            cursor.execute(f"UPDATE users SET sex_search = '{text}' WHERE user_id = '{self.user_id}'")
            #Сохраняем данные в базе
            conn.commit()
            #Инциализируем класс отправки сообщения
            send = Send(self.user_id)
            #Отправляем сообщение, что приняли данные
            send.sending(message = "Данные принял! Это был последний вопрос! Вот твоя анкета: ")
            #Получаем данные из базы, для вывода своей анкеты
            self.row = cursor.execute(f"SELECT * FROM users WHERE user_id = '{self.user_id}'") 
            #Получаем первую попавшуюся строчку
            self.row = cursor.fetchone()
            #Выводим сообщение с полученными данными
            if self.row[11] != "None": #Если есть аватар
                send.sending(message=f"{self.row[2]}, {self.row[4]}, {self.row[9]}\n{self.row[5]}", attachment = self.row[11])
                send.sending(message="Жми 1, чтобы начать просматривать анкеты!")
                print("attachments")
            else: #Если аватарки нет
                send.sending(message=f"{self.row[2]}, {self.row[4]}, {self.row[9]}\n{self.row[5]}")
                send.sending(message="Жми 1, чтобы начать просматривать анкеты!")
                print("no attachments")
        #Если выдали текст, не цифру
        else:
            send = Send(self.user_id)
            send.sending(message="Пожалуйста, отправь только цифру")

#Класс вывода анкет
class Output:
    def __init__(self, user_id):
        #Получаем id пользователя, чтобы получить данные из БД
        self.user_id = user_id 
        #Берем строку со своими данными
        self.myRow = cursor.execute(f"SELECT * FROM users WHERE user_id = '{self.user_id}'")
        #Берем первую попавшуюся
        self.myRow = cursor.fetchone()
    
    #Получаем список подходящих мне людей
    def selectAll(self, sex):
        #Объявляем массив, в котором будут храниться id подходящих пользователей
        array_ids = []
        #Если мне не важен пол
        print("Мои половые предпочтения - ", self.myRow[7])
        if self.myRow[7] == int(3):
            #Берем тех, кому он тоже не важен
            for row in cursor.execute(f"SELECT user_id FROM users WHERE sex_search = 3 AND user_id != '{self.user_id}'"):
                #Циклом добавляем в массив все id таких людей
                array_ids.append(row[0])
        
        if self.myRow[7] == int(1):
            #Если мне нравится женский пол
            for row in cursor.execute(f"SELECT user_id FROM users WHERE (sex = 1) AND (sex_search = '{sex}' OR sex_search = 3)"):
                #Заносим в массив всех девушек, которые хотят мой пол или им пол не важен
                array_ids.append(row[0])

        if self.myRow[7] == int(2):
            #Если мне нравится мужской пол
            for row in cursor.execute(f"SELECT user_id FROM users WHERE (sex = 2) AND (sex_search = '{sex}')"):
                #Выбираем всех мужчин которые хотят мой пол или им пол не важен
                array_ids.append(row[0])
        #Возвращаем массив с id нужных пользователей
        return array_ids
        
    #Получаем случайный id
    def getRandomId(self, sex):
        #Забираем массив людей 
        array = self.selectAll(sex)
        #Если в массиве 0 элементов
        if len(array) == 0:
            #Возвращаем строку, что люди пока не найдены
            return "Увы"
        
        #Если в массиве 1 элемент
        if len(array) == 1:
            #Возвращаем этот 1 элемент
            return array[0]
        
        #Если в массиве 2 элемента
        elif len(array) == 2:
            #Возвращаем или первый или последний элемент массива
            return array[randint(0,1)]
        
        #Если элементов больше
        else:
            #Возвращаем случайный элемент
            return array[randint(0, len(array)-1)]

    
class Like:
    def __init__(self, myId):
        #Первым параметром получаем свой id
        self.myId = myId

    #Получаем последний элемент массива
    def __getLastId(self, array):
        #Если количество элементов в массиве равно 0(такого не может быть)
        if len(array) == 0:
            #Возвращаем 0
            return 0
            #Если количество элементов в массиве равно 1
        elif len(array) == 1:
            #Возвращаем единственный элемент
            return array[0]
        #Иначе
        else:
            #Возвращаем последний
            return array[len(array)-2]

    def inquiry(self, array):
        #Вызываем в перемнную функцию, которая вернет нам id понравившегося человека
        hisId = self.__getLastId(array)
        #Вносим данные в базу
        #Статус 1 - Отправлен запрос
        #Статус 2 - Ожидание
        #Статус 3 - Готово
        cursor.execute(f"INSERT INTO inquiries (user_1, user_2, status) VALUES('{self.myId}', '{hisId}', '1')")
        #Сохраняем изменения
        conn.commit()

#Класс проверки что я кому-то нравлюсь
class SomeoneLikesMe:
    def __init__(self, from_id):
        self.from_id = from_id
    
    def __search(self):
        #Массив с пользователями, которым я понравился
        self.array = []
        #Берем запрос из базы данных, узнаем, нравлюсь ли я кому-то
        for row in cursor.execute(f"SELECT * FROM inquiries WHERE user_2 = '{self.from_id}' AND status = 1"):
            #Если строка существует
            if row is None:
                #Если строки не существует - возвращаем False
                return False
            else:
                #Добавляем в массив с пользователями, которым я понравился, id этих пользователей
                print(row[1])
                self.array.append(row[1])
        #Ну и возвращаем True
        return True
    #Метод для вывода массива пользователей 
    def returnArray(self, from_id):
        #Если строки существуют, где я кому-то нравлюсь
        if self.__search() == True:
            return self.array
            #Возвращаем массив
        else:
            #Иначе возвращаем False
            return False
    
    #Проверяем, массив ли это
    def checkIsArray(self, from_id):
        #Если функция возвращает False
        if self.returnArray(from_id) == False:
            #Возвращаем False
            return False
        #Иначе
        else:
            #Возвращаем тру
            return True

#Проходимся по людям, которые меня лайкают
class WhoLikedMe(SomeoneLikesMe):
    #Создаем функцию
    def cycle(self):
        cursor.execute(f"SELECT * FROM inquiries WHERE user_2 = '{self.from_id}' AND status = 1")    

#Класс для проверки взаимной симпатии
class MutualSympathy:
    def __init__(self, user_id):
        self.user_id = user_id

    def selectSympathy(self):
        #Достаем все возможные строки, где все хорошо
        for row in cursor.execute(f"SELECT * FROM inquiries WHERE user_1 = '{self.user_id}' AND status = 3 OR user_2 = '{self.user_id}' AND status = 3"):
            #Получаем user_1
            self.from_id = row[1]
            self.hisId = row[2]           
            #Берем данные из бд
            first_row = cursor.execute(f"SELECT * FROM users WHERE user_id = '{self.from_id}'")
            first_row = cursor.fetchone()
            second_row = cursor.execute(f"SELECT * FROM users WHERE user_id = '{self.hisId}'")
            second_row = cursor.fetchone()
            #Готовимся отправлять сообщения
            #Отправляем первому пользователю данные второго
            send_user1 = Send(self.hisId)
            if first_row[11] != None or first_row[11] != "None":
                send_user1.sending(message=f"Есть взаимная симпатия! Держи ссылку: https://vk.com/id{self.from_id}\n {first_row[2]}, {first_row[4]}, {first_row[9]}\n {first_row[5]},", attachment=first_row[11])
            else:
                send_user1.sending(message=f"Есть взаимная симпатия! Держи ссылку: https://vk.com/id{self.from_id}\n {first_row[2]}, {first_row[4]}, {first_row[9]}\n {first_row[5]}")               
            #Отправляем второму пользователю данные первого
            send_user2 = Send(self.from_id)
            if second_row[11] != None or second_row[11] != 'None':
                send_user2.sending(message=f"Есть взаимная симпатия! Держи ссылку: https://vk.com/id{self.hisId}\n {second_row[2]}, {second_row[4]}, {second_row[9]}\n {second_row[5]}", attachment=second_row[11])
            else:
                send_user2.sending(message=f"Есть взаимная симпатия! Держи ссылку: https://vk.com/id{self.hisId}\n {second_row[2]}, {second_row[4]}, {second_row[9]}\n {second_row[5]}")
            cursor.execute(f"DELETE FROM inquiries WHERE user_1 = '{self.from_id}' AND user_2 = '{self.hisId}' AND status = 3")
            cursor.execute(f"DELETE FROM inquiries WHERE user_2 = '{self.from_id}' AND user_1 = '{self.hisId}' AND status = 3")
            cursor.execute(f"DELETE FROM inquiries WHERE user_1 = '{self.from_id}' AND user_2 = '{self.hisId}' AND status = 1")
            cursor.execute(f"DELETE FROM inquiries WHERE user_2 = '{self.from_id}' AND user_1 = '{self.hisId}' AND status = 1")

#Класс для получения фотографии пользователя, берем аватарку
class UserPhoto:
    def __init__(self, user_id):
        self.user_id = user_id

    def getPhoto(self):
        #Отправляем запрос с методом вк_апи users.get
        self.photo_id = vk.users.get(user_ids=self.user_id, fields="photo_id")
        print(self.photo_id[0])
        return self.photo_id

    #Проверим еесть ли аватарка
    def checkAvatar(self):
        #Оставляем только словарь
        self.dictionary = self.getPhoto()[0]
        #Если есть такой ключ
        if 'photo_id' in self.dictionary.keys():
            print("Словарь True")
            #Возвращаем True
            return True
        #Иначе
        else:
            print("Словарь False")
            #Возвращаем False
            return False
    
    #Берем id
    def getId(self):
        #Если проверка аватарки вернула True
        if self.checkAvatar() == True:
            print(self.dictionary)
            #Забираем id
            return self.dictionary['photo_id']
        else:
            #Иначе возвращаем ничего
            print("None") 
            return None
    
    #Добавляем в базу данных полученное значение
    def result(self):
        if self.getId() != None:
            #Приводим к этому виду photo100172_166443618
            self.prefix = "photo"
            #Складываем строки
            attachment = str(self.prefix) + str(self.getId())
            return attachment
        else:
            return None
            
