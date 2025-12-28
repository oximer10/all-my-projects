from random import choice
from time import time
from re import fullmatch

allcards = {}
users={}
ans=''
notes={}

def admin():
    print('Напишите что вы хотите сделать:')
    print('1-создать новый аккаунт(зарегистрироваться)')
    print('2-войти в аккаунт')
    a=int(input())
    while True:
        if a==1:
            registration(users)
            break
        elif a==2:
            login(users)
            break
        elif a=='' :
            print('Неверная команда!')
        else:
            print('Неверная команда!')
            continue



def newcard(allcards):
    question = input('Напишите вопрос: ')
    answer = input('Напишите ответ на вопрос: ')
    allcards[question]=(answer)
    print('Ваша карточка сохранена.')
    return allcards

def randomcard(allcards):
    if len(allcards)==0:
        print("Нет доступных карточек.")
        return
    question = choice(list(allcards.keys()))
    print("Вопрос:", question)
    print("Ответ:", allcards[question])


def quiz():
    if len(allcards) == 0:
        print("Нет доступных карточек.")
        return
    print('Чтобы начать викторину, введите "1"')
    d=input()
    if d!="1":
        print("Неверная команда!")
        return
    correct=0
    total=0
    while True:
        quizz = choice(list(allcards.keys()))
        print('Вопрос:', quizz)
        print("У вас есть 30 секунд на ответ!")
        start=time()
        try:
            ans=input()
        except:
            ans=""
        timer=time()-start
        if timer>30:
            print("Время вышло!")
            print(f"Правильный ответ: {allcards[quizz]}")
        else:
            if ans.lower().strip() == allcards[quizz].lower().strip():
                print("Правильно!")
                correct+=1
            else:
                print(f"Неправильно. Правильный ответ: {allcards[quizz]}")
        total+=1
        print('Хотите продолжить? Введите "1" — да, "2" — выйти в меню.')
        while True:
            l=input()
            if l=='1':
                break
            elif l=='2':
                print(f"Итог: правильно {correct} из {total}")
                return
            else:
                print('Неверная команда!')
                return




def mainmenu():
    while True:
        print('Напишите что вы хотите сделать:')
        print('1-добавить новую карточку с вопросом и ответом')
        print('2-получить случайную карточку из своей коллекций')
        print('3-запустить викторину')
        print('4-заметки')
        print('5-выйти из аккаунта')
        b=input()
        if b=='1':
            newcard(allcards)
        elif b=='2':
            randomcard(allcards)
        elif b=='3':
            quiz()
        elif b=='4':
            note()
        elif b=='5':
            break
        else:
            print('Неверная команда!')


def checking(password):
    return fullmatch(r'[A-Za-z0-9]+', password) is not None


def registration(users):
    while True:
        person=input('Придумайте имя пользователя:')
        if person in users:
            print('Это имя пользователя уже занято!!!,придумайте другое:')
            continue
        elif person=='':
            print('Имя пользователя не может быть пустым! ,придумайте другое:')
        else:
            while True:
                password = input('Создайте пароль для аккаунта:')
                if len(password)<=5:
                    print('пароль слишком короткий')
                    continue
                elif not checking(password):
                    print('Пароль должен содержать только латинские буквы и цифры!')
                    continue
                else:
                    print('Ваш аккаунт успешно зарегистрирован!')
                    users[person]=password
                    mainmenu()
                    return


def login(users):
    while True:
        person=input('Введите имя пользователя:')
        password = input('Введите пароль:')
        if person in users and users[person] == password:
            print('Вход успешно выполнен!')
            mainmenu()
            break
        else:
            print('Неверное имя пользователя или пароль.')
        continue

def note():
    while True:
        print("1 - создать заметку")
        print("2 - просмотреть заметки")
        print("3 - удалить заметку")
        print("4 - назад")
        p=input("Выберите действие: ")
        if p=='1':
            title = input("Название заметки: ")
            text = input("Текст заметки: ")
            notes[title] = text
        elif p=='2':
            for title, text in notes.items():
                print(f"{title}: {text}")
        elif p=='3':
            title = input("Название заметки для удаления: ")
            if title in notes:
                del notes[title]
                print("Заметка удалена")
            else:
                print("Нет такой заметки.")
        elif p=='4':
            break
        else:
            print("Неверная команда!")



print('Добро пожаловать в Study App!')
while True:
    admin()