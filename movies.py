import tkinter as tk
from tkinter import ttk
import json
import os

# Файл для сохранения данных
DATA_FILE = "movies.json"

# Список фильмов (хранится как список словарей)
movies = []

# Загрузка данных из JSON при запуске
def load_data():
    global movies
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                movies = json.load(f)
        except:
            movies = []
    update_table()

# Сохранение данных в JSON
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

# Обновление таблицы
def update_table(filtered_movies=None):
    # Очищаем таблицу
    for item in tree.get_children():
        tree.delete(item)
    
    # Если есть отфильтрованные данные — показываем их, иначе все фильмы
    data_to_show = filtered_movies if filtered_movies is not None else movies
    
    for movie in data_to_show:
        tree.insert("", "end", values=(
            movie["title"],
            movie["genre"],
            movie["year"],
            movie["rating"]
        ))

# Добавление фильма
def add_movie():
    title = entry_title.get().strip()
    genre = entry_genre.get().strip()
    year_str = entry_year.get().strip()
    rating_str = entry_rating.get().strip()
    
    # Проверка корректности ввода
    if not title or not genre:
        status_label.config(text="Заполните название и жанр!")
        return
    
    try:
        year = int(year_str)
        if year < 1800 or year > 2100:  
            status_label.config(text="Год должен быть от 1800 до 2100!")
            return
    except ValueError:
        status_label.config(text="Год должен быть числом!")
        return
    
    try:
        rating = float(rating_str)
        if rating < 0 or rating > 10:
            status_label.config(text="Рейтинг должен быть от 0 до 10!")
            return
    except ValueError:
        status_label.config(text="Рейтинг должен быть числом от 0 до 10!")
        return
    
    # Добавление фильм в список
    movie = {
        "title": title,
        "genre": genre,
        "year": year,
        "rating": rating
    }
    movies.append(movie)
    
    # Сохранение данные
    save_data()
    
    # Обновление таблицу
    update_table()
    
    # Очищаем поля ввода
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)
    
    status_label.config(text="Фильм добавлен!")

# Фильтрация по жанру
def filter_by_genre():
    genre_filter = genre_filter_entry.get().strip().lower()
    if not genre_filter:
        update_table()  # Показываем все, если фильтр пуст
        return
    
    filtered = [m for m in movies if genre_filter in m["genre"].lower()]
    update_table(filtered)

# Фильтрация по году
def filter_by_year():
    year_filter_str = year_filter_entry.get().strip()
    if not year_filter_str:
        update_table()
        return
    
    try:
        year_filter = int(year_filter_str)
        filtered = [m for m in movies if m["year"] == year_filter]
        update_table(filtered)
    except ValueError:
        status_label.config(text="Год для фильтрации должен быть числом!")

# Создание главного окна
root = tk.Tk()
root.title("Movie Library — Личная кинотека")
root.geometry("700x500")

# Поля ввода
tk.Label(root, text="Название фильма:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
entry_title = tk.Entry(root, width=30)
entry_title.grid(row=0, column=1, padx=5, pady=2)

tk.Label(root, text="Жанр:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
entry_genre = tk.Entry(root, width=30)
entry_genre.grid(row=1, column=1, padx=5, pady=2)

tk.Label(root, text="Год выпуска:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
entry_year = tk.Entry(root, width=30)
entry_year.grid(row=2, column=1, padx=5, pady=2)

tk.Label(root, text="Рейтинг (0–10):").grid(row=3, column=0, sticky="w", padx=5, pady=2)
entry_rating = tk.Entry(root, width=30)
entry_rating.grid(row=3, column=1, padx=5, pady=2)

# Кнопка добавления
tk.Button(root, text="Добавить фильм", command=add_movie).grid(row=4, column=0, columnspan=2, pady=10)

# Фильтры
tk.Label(root, text="Фильтр по жанру:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
genre_filter_entry = tk.Entry(root, width=30)
genre_filter_entry.grid(row=5, column=1, padx=5, pady=2)
tk.Button(root, text="Применить фильтр по жанру", command=filter_by_genre).grid(row=6, column=0, columnspan=2, pady=5)

tk.Label(root, text="Фильтр по году:").grid(row=7, column=0, sticky="w", padx=5, pady=2)
year_filter_entry = tk.Entry(root, width=30)
year_filter_entry.grid(row=7, column=1, padx=5, pady=2)
tk.Button(root, text="Применить фильтр по году", command=filter_by_year).grid(row=8, column=0, columnspan=2, pady=5)

# Таблица (Treeview)
columns = ("title", "genre", "year", "rating")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
tree.heading("title", text="Название")
tree.heading("genre", text="Жанр")
tree.heading("year", text="Год")
tree.heading("rating", text="Рейтинг")
tree.column("title", width=200)
tree.column("genre", width=150)
tree.column("year", width=80)
tree.column("rating", width=80)
tree.grid(row=9, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

# Статус-метка
status_label = tk.Label(root, text="Готов к работе", fg="blue")
status_label.grid(row=10, column=0, columnspan=2, pady=5)

# Загрузка данных при запуске
load_data()

# Запуск приложения
root.mainloop()
