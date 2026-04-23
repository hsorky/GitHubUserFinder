import tkinter as tk
from tkinter.messagebox import showerror, showinfo
import requests
import json

window = tk.Tk()
window.title("GitHub users finder")
window.geometry("600x500")

#Вывод списка избранных
def show_faves():
    faves = load_fav() #Выгрузка избранных
    if faves == []: #Проверка на то, является ли список пустым
        showinfo(title="Избранное", message="Список избранных пуст")
        return
    user_listbox.delete(0, tk.END) #Удаление предыдущих данных
    for fave in faves: #Добавление в listbox
        user_listbox.insert(tk.END, fave)

#Кнопка для показа списка избранных
favorit_btn = tk.Button(window, text="Избранное", command=show_faves)
favorit_btn.place(x=260, y=30)

#Frame для поиска
search_frame = tk.Frame(window, width=100)
search_frame.place(x=10, y=60)

#label сообщение
start_label = tk.Label(search_frame, text="Введите имя пользователя")
start_label.pack()

#entry для ввода на поиск
user_entry = tk.Entry(search_frame)
user_entry.pack(pady=5)
#функция поиска пользователя
def search_users():
    query = user_entry.get().strip() #получение запроса
    if not query: #проверка на пустое поле
        showerror(title="Ошибка", message="Пустое поле поиска")
        return
    #Получение ответа
    try:
        response = requests.get("https://api.github.com/search/users", params={"q": query, "per_page": 18}) #Запрос 18 позиций       
        data = response.json()
        items = data.get("items", [])
            #Очстка таблицы
        user_listbox.delete(0, tk.END)
            #Ввод в таблицу значений поиска
        for user in items:
            user_listbox.insert(tk.END, user["login"])
            #Обработка ошибок
    except requests.exceptions.RequestException as e:
        showerror("Ошибка сети", f"Не удалось выполнить запрос:\n{e}")           
    except Exception as e:
        showerror("Ошибка", f"Неизвестная ошибка:\n{e}")

#Кнопка поиска
search_btn = tk.Button(search_frame, text="Поиск", width=15, command=search_users)
search_btn.pack(pady=5)

#функция добавления в избранные
def add_fave():
    faves = load_fav() #Выгрузка избранных
    new_fave_indx = user_listbox.curselection()
    if not new_fave_indx: #Проверка на пустое добавление
        showerror(title="Ошибка", message="Не выбран пользователь для добавления")
        return
    new_fave = user_listbox.get(new_fave_indx[0])
    if new_fave in faves: #Проверка на повтор в избранных
        showerror(title="Ошибка", message="Такой пользователь уже находится в списке избранных")
        return
    faves.append(new_fave)
    save_fave(faves)
    showinfo(title="Избранное", message="Пользователь успешно добавлен в избранное")

#Кнопка добавления в избранное
favor_btn = tk.Button(search_frame, text="В избранное", width=15, command=add_fave)
favor_btn.pack(pady=5)

#listbox для вывода списка пользователей
user_listbox = tk.Listbox(search_frame, width=95, height=18)
user_listbox.pack()
    #Загрузка списка избранных
def load_fav():
    try:
        with open("favorits.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        return []
    #Сохранение списка избранных
def save_fave(faves):
    with open("favorits.json", "w", encoding="utf-8") as file:
        json.dump(faves, file)

window.mainloop() #запуск прогграммы