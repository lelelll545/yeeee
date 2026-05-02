import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("800x500")

        # Файл для хранения данных
        self.data_file = "movies.json"
        self.movies = []          # список всех фильмов (словарей)
        self.filter_genre = ""    # текущий фильтр по жанру (точное совпадение)
        self.filter_year = ""     # текущий фильтр по году (точное совпадение)

        # Создание интерфейса
        self.create_input_frame()
        self.create_filter_frame()
        self.create_table()
        self.create_buttons()

        # Загрузка данных и обновление таблицы
        self.load_data()
        self.update_table()
        self.update_genre_list()

    # ---------- Фрейм ввода нового фильма ----------
    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.root, text="Добавить новый фильм", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Название
        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        # Жанр
        ttk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.genre_entry = ttk.Entry(input_frame, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=2)

        # Год выпуска
        ttk.Label(input_frame, text="Год:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.year_entry = ttk.Entry(input_frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Рейтинг (0-10)
        ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.rating_entry = ttk.Entry(input_frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        # Кнопка добавления
        self.add_btn = ttk.Button(input_frame, text="Добавить фильм", command=self.add_movie)
        self.add_btn.grid(row=1, column=4, padx=10, pady=2)

    # ---------- Фрейм фильтрации ----------
    def create_filter_frame(self):
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="w", padx=5)
        self.filter_genre_combo = ttk.Combobox(filter_frame, width=20, state="readonly")
        self.filter_genre_combo.grid(row=0, column=1, padx=5)
        self.filter_genre_combo.set("")  # пустое значение = без фильтра

        ttk.Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2, sticky="w", padx=5)
        self.filter_year_entry = ttk.Entry(filter_frame, width=10)
        self.filter_year_entry.grid(row=0, column=3, padx=5)

        self.filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=0, column=4, padx=5)

        self.clear_filter_btn = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        self.clear_filter_btn.grid(row=0, column=5, padx=5)

    # ---------- Таблица с фильмами ----------
    def create_table(self):
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Создаём скроллбары
        scroll_y = ttk.Scrollbar(self.tree_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(self.tree_frame, orient="horizontal")

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("title", "genre", "year", "rating"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Определяем заголовки
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")

        # Ширина колонок
        self.tree.column("title", width=250)
        self.tree.column("genre", width=150)
        self.tree.column("year", width=80, anchor="center")
        self.tree.column("rating", width=80, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

    # ---------- Нижние кнопки (удаление) ----------
    def create_buttons(self):
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        self.delete_btn = ttk.Button(btn_frame, text="Удалить выбранный фильм", command=self.delete_movie)
        self.delete_btn.pack(side="left", padx=5)

    # ---------- Логика работы с данными ----------
    def load_data(self):
        """Загружает список фильмов из JSON-файла."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.movies = []
        else:
            self.movies = []

    def save_data(self):
        """Сохраняет текущий список фильмов в JSON-файл."""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def update_genre_list(self):
        """Обновляет выпадающий список жанров для фильтра (уникальные значения)."""
        genres = sorted(set(m["genre"] for m in self.movies if m["genre"].strip()))
        self.filter_genre_combo["values"] = [""] + genres

    def add_movie(self):
        """Добавляет новый фильм после проверки полей."""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        # Проверка на заполненность
        if not title or not genre or not year_str or not rating_str:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        # Проверка года
        try:
            year = int(year_str)
            if year < 1888 or year > 2100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть целым числом (например, 1994).")
            return

        # Проверка рейтинга
        try:
            rating = float(rating_str)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
            return

        # Добавляем фильм
        new_movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        self.movies.append(new_movie)
        self.save_data()
        self.update_genre_list()
        self.update_table()   # обновляем отображение с учётом текущих фильтров

        # Очищаем поля ввода
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Фильм добавлен!")

    def delete_movie(self):
        """Удаляет выбранный в таблице фильм."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите фильм для удаления.")
            return

        # Получаем индекс фильма в отфильтрованном списке
        filtered_movies = self.get_filtered_movies()
        for item in selected:
            # item — это IID строки в Treeview, мы храним в нём порядковый номер в отфильтрованном списке
            index = int(item)
            if 0 <= index < len(filtered_movies):
                movie_to_delete = filtered_movies[index]
                # Удаляем из общего списка (по совпадению всех полей, но проще по названию и году)
                # Для надёжности удалим первый совпадающий элемент
                for i, m in enumerate(self.movies):
                    if (m["title"] == movie_to_delete["title"] and
                        m["genre"] == movie_to_delete["genre"] and
                        m["year"] == movie_to_delete["year"] and
                        m["rating"] == movie_to_delete["rating"]):
                        del self.movies[i]
                        break

        self.save_data()
        self.update_genre_list()
        self.update_table()
        messagebox.showinfo("Успех", "Фильм(ы) удалён(ы).")

    def get_filtered_movies(self):
        """Возвращает список фильмов, отфильтрованных по текущим критериям."""
        result = self.movies
        if self.filter_genre:
            result = [m for m in result if m["genre"] == self.filter_genre]
        if self.filter_year:
            try:
                year_int = int(self.filter_year)
                result = [m for m in result if m["year"] == year_int]
            except ValueError:
                pass  # если в фильтре года не число, игнорируем
        return result

    def update_table(self):
        """Обновляет таблицу на основе текущих фильтров."""
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        filtered = self.get_filtered_movies()
        for idx, movie in enumerate(filtered):
            self.tree.insert("", tk.END, iid=str(idx), values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))

    def apply_filter(self):
        """Устанавливает фильтры из полей ввода и обновляет таблицу."""
        self.filter_genre = self.filter_genre_combo.get().strip()
        self.filter_year = self.filter_year_entry.get().strip()
        self.update_table()

    def reset_filter(self):
        """Сбрасывает фильтры и обновляет таблицу."""
        self.filter_genre = ""
        self.filter_year = ""
        self.filter_genre_combo.set("")
        self.filter_year_entry.delete(0, tk.END)
        self.update_table()


# ---------- Запуск приложения ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()

