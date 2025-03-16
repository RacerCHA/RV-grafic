import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk  # Пока не используем, но скоро понадобится
import image_processor  # Пока не используем, но скоро понадобится
import json
import os
import subprocess  # Для открытия папки в проводнике

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор гоночной инфографики")

        # Создаем директорию render, если она не существует
        if not os.path.exists("render"):
            os.makedirs("render")

        # Переменные для хранения данных
        self.infographic_type = tk.StringVar()
        self.team_logo_path = tk.StringVar()
        self.team_name = tk.StringVar()
        self.championship_name = tk.StringVar()
        self.stage_number = tk.StringVar()
        
        # Фотографии для раздела "Состав пилотов"
        self.pilot1_photo_path = tk.StringVar()
        self.pilot1_name = tk.StringVar()
        self.pilot2_photo_path = tk.StringVar()
        self.pilot2_name = tk.StringVar()
        self.pilot3_photo_path = tk.StringVar()
        self.pilot3_name = tk.StringVar()
        
        # Фотографии для раздела "Статистика"
        self.pilot1_stats_photo_path = tk.StringVar()
        self.pilot2_stats_photo_path = tk.StringVar()
        self.pilot3_stats_photo_path = tk.StringVar()
        
        self.manager_name = tk.StringVar()
        self.date_group = tk.StringVar()
        self.pilots_count = tk.StringVar(value="3")  # Значение по умолчанию
        self.stages_count = tk.StringVar(value="5")  # Значение по умолчанию
        self.race_results = []  # Список для хранения результатов гонок
        self.save_folder_path = tk.StringVar(value="render")  # Папка для сохранения изображений по умолчанию

        # Статистика пилотов
        self.pilot1_krugi = tk.StringVar()
        self.pilot1_luchshee = tk.StringVar()
        self.pilot1_srednee = tk.StringVar()
        self.pilot2_krugi = tk.StringVar()
        self.pilot2_luchshee = tk.StringVar()
        self.pilot2_srednee = tk.StringVar()
        self.pilot3_krugi = tk.StringVar()
        self.pilot3_luchshee = tk.StringVar()
        self.pilot3_srednee = tk.StringVar()

        # Элементы интерфейса
        self.create_widgets()
        self.update_ui()  # Добавляем вызов функции update_ui
        self.setup_results_table() # Инициализация таблицы результатов

    def load_data_from_file(self, filename):
        """
        Загружает данные из текстового файла.
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = [line.strip() for line in f.readlines()]
            return data
        except FileNotFoundError:
            print(f"Error: File not found: {filename}")
            return []

    def load_pilots(self):
        """
        Загружает список пилотов из файла pilots.txt.
        """
        return self.load_data_from_file("assets/pilots.txt")

    def load_managers(self):
        """
        Загружает список менеджеров из файла manager.txt.
        """
        return self.load_data_from_file("assets/manager.txt")

    def load_races(self):
        """
        Загружает список названий чемпионатов из файла race.txt.
        """
        return self.load_data_from_file("assets/race.txt")

    def load_teams(self):
        """
        Загружает список названий команд из файла team.txt.
        """
        return self.load_data_from_file("assets/team.txt")

    def update_ui(self):
        infographic_type = self.infographic_type.get()
        if infographic_type == "Состав пилотов":
            self.team_frame.pack(padx=10, pady=10, fill="x")
            self.pilots_frame.pack(padx=10, pady=10, fill="x")
            # Скрываем frames для других типов инфографики
            self.results_frame.pack_forget()
            self.stats_frame.pack_forget()
        elif infographic_type == "Результаты гонок":
            self.team_frame.pack(padx=10, pady=10, fill="x")
            self.results_frame.pack(padx=10, pady=10, fill="x")
            # Скрываем frames для других типов инфографики
            self.pilots_frame.pack_forget()
            self.stats_frame.pack_forget()
            self.update_results_table() # Обновляем таблицу при переключении
        elif infographic_type == "Статистика":
            self.team_frame.pack(padx=10, pady=10, fill="x")
            self.stats_frame.pack(padx=10, pady=10, fill="x")
            # Скрываем frames для других типов инфографики
            self.results_frame.pack_forget()
            self.pilots_frame.pack_forget()
        else:
            # Если тип не выбран, скрываем все
            self.team_frame.pack_forget()
            self.pilots_frame.pack_forget()
            self.results_frame.pack_forget()
            self.stats_frame.pack_forget()

    def create_widgets(self):
        # Фрейм для выбора типа инфографики
        infotype_frame = ttk.LabelFrame(self.root, text="Выберите тип инфографики")
        infotype_frame.pack(padx=10, pady=10, fill="x")

        infotype_label = ttk.Label(infotype_frame, text="Тип инфографики:")
        infotype_label.pack(side="left", padx=5, pady=5)

        self.infotype_combobox = ttk.Combobox(infotype_frame, textvariable=self.infographic_type,
                                                values=["Состав пилотов", "Результаты гонок", "Статистика"])  # Заменить на реальные имена файлов
        self.infotype_combobox.bind("<<ComboboxSelected>>",
                                   lambda event: self.update_ui())  # При выборе элемента в Combobox вызываем функцию update_ui
        self.infotype_combobox.pack(side="left", padx=5, pady=5)

        # Создание стиля для кнопки "Создать инфографику"
        style = ttk.Style()
        style.configure("GreenButton.TButton", foreground="green", background="green", font=("Arial", 12)) #Задаем параметры для кнопки

        # Фрейм для шаблонов
        template_frame = ttk.LabelFrame(self.root, text="Шаблоны")
        template_frame.pack(padx=10, pady=10, fill="x")

        # Добавляем метку для отображения текущего шаблона
        template_label = ttk.Label(template_frame, text="Текущий шаблон:")
        template_label.pack(side="left", padx=5, pady=5)
        
        self.current_template_label = ttk.Label(template_frame, text="Шаблон не выбран")
        self.current_template_label.pack(side="left", padx=5, pady=5)

        save_template_button = ttk.Button(template_frame, text="Сохранить шаблон", command=self.save_template)
        save_template_button.pack(side="left", padx=5, pady=5)

        open_template_button = ttk.Button(template_frame, text="Открыть шаблон", command=self.load_template)
        open_template_button.pack(side="left", padx=5, pady=5)

        # Добавляем элементы для выбора папки сохранения
        save_folder_label = ttk.Label(template_frame, text="Папка сохранения:")
        save_folder_label.pack(side="left", padx=5, pady=5)
        
        self.save_folder_display = ttk.Label(template_frame, text=self.save_folder_path.get())
        self.save_folder_display.pack(side="left", padx=5, pady=5)
        
        save_folder_button = ttk.Button(template_frame, text="Выбрать папку", command=self.select_save_folder)
        save_folder_button.pack(side="left", padx=5, pady=5)
        
        # Добавляем кнопку для открытия папки сохранения в проводнике
        open_folder_button = ttk.Button(template_frame, text="Открыть папку", command=self.open_save_folder)
        open_folder_button.pack(side="left", padx=5, pady=5)

        # Фрейм для выбора логотипа и ввода данных команды
        self.team_frame = ttk.LabelFrame(self.root, text="Данные команды")
        #self.team_frame.pack(padx=10, pady=10, fill="x")

        team_logo_label = ttk.Label(self.team_frame, text="Логотип команды:")
        team_logo_label.pack(side="left", padx=5, pady=5)
        team_logo_button = ttk.Button(self.team_frame, text="Выбрать логотип", command=self.select_team_logo)
        team_logo_button.pack(side="left", padx=5, pady=5)

        # Название команды
        team_name_label = ttk.Label(self.team_frame, text="Название команды:")
        team_name_label.pack(side="left", padx=5, pady=5)
        self.team_name_values = self.load_teams()  # Загружаем названия команд из файла
        self.team_name_combobox = ttk.Combobox(self.team_frame, textvariable=self.team_name,
                                                 values=self.team_name_values)
        self.team_name_combobox.pack(side="left", padx=5, pady=5)

        # Название чемпионата
        championship_name_label = ttk.Label(self.team_frame, text="Название чемпионата:")
        championship_name_label.pack(side="left", padx=5, pady=5)
        self.championship_name_values = self.load_races()  # Загружаем названия чемпионатов из файла
        self.championship_name_combobox = ttk.Combobox(self.team_frame, textvariable=self.championship_name,
                                                          values=self.championship_name_values)
        self.championship_name_combobox.pack(side="left", padx=5, pady=5)

        stage_number_label = ttk.Label(self.team_frame, text="Номер этапа:")
        stage_number_label.pack(side="left", padx=5, pady=5)
        self.stage_number_entry = ttk.Entry(self.team_frame, textvariable=self.stage_number)
        self.stage_number_entry.pack(side="left", padx=5, pady=5)

        # Фрейм для данных пилотов
        self.pilots_frame = ttk.LabelFrame(self.root, text="Данные пилотов")
        #self.pilots_frame.pack(padx=10, pady=10, fill="x")

        # Пилот 1
        pilot1_frame = ttk.LabelFrame(self.pilots_frame, text="Пилот 1")
        pilot1_frame.pack(side="top", padx=5, pady=5, fill="x")
        
        # Добавляем выбор фото пилота 1
        pilot1_photo_label = ttk.Label(pilot1_frame, text="Фото пилота:")
        pilot1_photo_label.pack(side="left", padx=5, pady=5)
        pilot1_photo_button = ttk.Button(pilot1_frame, text="Выбрать фото", command=self.select_pilot1_photo)
        pilot1_photo_button.pack(side="left", padx=5, pady=5)
        self.pilot1_photo_name_label = ttk.Label(pilot1_frame, text="Фото не выбрано")
        self.pilot1_photo_name_label.pack(side="left", padx=5, pady=5)
        
        # Добавляем выбор имени пилота 1
        pilot1_name_label = ttk.Label(pilot1_frame, text="Имя пилота:")
        pilot1_name_label.pack(side="left", padx=5, pady=5)
        self.pilot1_name_values = self.load_pilots()
        self.pilot1_name_combobox = ttk.Combobox(pilot1_frame, textvariable=self.pilot1_name, values=self.pilot1_name_values)
        self.pilot1_name_combobox.pack(side="left", padx=5, pady=5)

        # Пилот 2
        pilot2_frame = ttk.LabelFrame(self.pilots_frame, text="Пилот 2")
        pilot2_frame.pack(side="top", padx=5, pady=5, fill="x")
        
        # Добавляем выбор фото пилота 2
        pilot2_photo_label = ttk.Label(pilot2_frame, text="Фото пилота:")
        pilot2_photo_label.pack(side="left", padx=5, pady=5)
        pilot2_photo_button = ttk.Button(pilot2_frame, text="Выбрать фото", command=self.select_pilot2_photo)
        pilot2_photo_button.pack(side="left", padx=5, pady=5)
        self.pilot2_photo_name_label = ttk.Label(pilot2_frame, text="Фото не выбрано")
        self.pilot2_photo_name_label.pack(side="left", padx=5, pady=5)
        
        # Добавляем выбор имени пилота 2
        pilot2_name_label = ttk.Label(pilot2_frame, text="Имя пилота:")
        pilot2_name_label.pack(side="left", padx=5, pady=5)
        self.pilot2_name_values = self.load_pilots()
        self.pilot2_name_combobox = ttk.Combobox(pilot2_frame, textvariable=self.pilot2_name, values=self.pilot2_name_values)
        self.pilot2_name_combobox.pack(side="left", padx=5, pady=5)

        # Пилот 3
        pilot3_frame = ttk.LabelFrame(self.pilots_frame, text="Пилот 3")
        pilot3_frame.pack(side="top", padx=5, pady=5, fill="x")
        
        # Добавляем выбор фото пилота 3
        pilot3_photo_label = ttk.Label(pilot3_frame, text="Фото пилота:")
        pilot3_photo_label.pack(side="left", padx=5, pady=5)
        pilot3_photo_button = ttk.Button(pilot3_frame, text="Выбрать фото", command=self.select_pilot3_photo)
        pilot3_photo_button.pack(side="left", padx=5, pady=5)
        self.pilot3_photo_name_label = ttk.Label(pilot3_frame, text="Фото не выбрано")
        self.pilot3_photo_name_label.pack(side="left", padx=5, pady=5)
        
        # Добавляем выбор имени пилота 3
        pilot3_name_label = ttk.Label(pilot3_frame, text="Имя пилота:")
        pilot3_name_label.pack(side="left", padx=5, pady=5)
        self.pilot3_name_values = self.load_pilots()
        self.pilot3_name_combobox = ttk.Combobox(pilot3_frame, textvariable=self.pilot3_name, values=self.pilot3_name_values)
        self.pilot3_name_combobox.pack(side="left", padx=5, pady=5)

        # Фрейм для данных результатов гонок
        self.results_frame = ttk.LabelFrame(self.root, text="Данные результатов гонок")
        #self.results_frame.pack(padx=10, pady=10, fill="x") #Пока не показываем

        # Количество пилотов в гонке
        pilots_count_label = ttk.Label(self.results_frame, text="Количество пилотов в гонке:")
        pilots_count_label.pack(side="left", padx=5, pady=5)
        self.pilots_count_entry = ttk.Entry(self.results_frame, textvariable=self.pilots_count)
        self.pilots_count_entry.pack(side="left", padx=5, pady=5)

        # Количество этапов в чемпионате
        stages_count_label = ttk.Label(self.results_frame, text="Количество этапов в чемпионате:")
        stages_count_label.pack(side="left", padx=5, pady=5)
        self.stages_count_entry = ttk.Entry(self.results_frame, textvariable=self.stages_count)
        self.stages_count_entry.pack(side="left", padx=5, pady=5)
        self.stages_count_entry.bind("<Return>", self.update_results_table) # Обновляем таблицу при изменении

        # Таблица с результатами
        self.results_table = ttk.Treeview(self.results_frame, columns=("stage", "place"), show="headings")
        self.results_table.heading("stage", text="Этап")
        self.results_table.heading("place", text="Место")
        self.results_table.column("stage", width=100, anchor="center")
        self.results_table.column("place", width=100, anchor="center")
        self.results_table.pack(padx=5, pady=5)
        self.results_table.bind("<Double-1>", self.edit_place) # Дабл-клик для редактирования

        # Кнопка "Обновить таблицу"
        update_table_button = ttk.Button(self.results_frame, text="Обновить таблицу", command=self.update_results_table)
        update_table_button.pack(pady=5)

        # Фрейм для данных статистики
        self.stats_frame = ttk.LabelFrame(self.root, text="Данные статистики")
        #self.stats_frame.pack(padx=10, pady=10, fill="x") #Пока не показываем

        # Статистика для пилота 1
        self.pilot1_stats_frame = ttk.LabelFrame(self.stats_frame, text="Статистика для пилота 1")
        self.pilot1_stats_frame.pack(side="top", padx=5, pady=5, fill="x")

        # Добавляем выбор фото пилота 1
        pilot1_stats_photo_label = ttk.Label(self.pilot1_stats_frame, text="Фото пилота:")
        pilot1_stats_photo_label.pack(side="left", padx=5, pady=5)
        pilot1_stats_photo_button = ttk.Button(self.pilot1_stats_frame, text="Выбрать фото", command=self.select_pilot1_stats_photo)
        pilot1_stats_photo_button.pack(side="left", padx=5, pady=5)
        self.pilot1_stats_photo_name_label = ttk.Label(self.pilot1_stats_frame, text="Фото не выбрано")
        self.pilot1_stats_photo_name_label.pack(side="left", padx=5, pady=5)
        
        # Добавляем выбор имени пилота 1
        pilot1_stats_name_label = ttk.Label(self.pilot1_stats_frame, text="Имя пилота:")
        pilot1_stats_name_label.pack(side="left", padx=5, pady=5)
        self.pilot1_stats_name_combobox = ttk.Combobox(self.pilot1_stats_frame, textvariable=self.pilot1_name, values=self.load_pilots())
        self.pilot1_stats_name_combobox.pack(side="left", padx=5, pady=5)

        pilot1_krugi_label = ttk.Label(self.pilot1_stats_frame, text="Круги")
        pilot1_krugi_label.pack(side="left", padx=5, pady=5)
        self.pilot1_krugi_entry = ttk.Entry(self.pilot1_stats_frame, textvariable=self.pilot1_krugi)
        self.pilot1_krugi_entry.pack(side="left", padx=5, pady=5)

        pilot1_luchshee_label = ttk.Label(self.pilot1_stats_frame, text="Лучшее время")
        pilot1_luchshee_label.pack(side="left", padx=5, pady=5)
        self.pilot1_luchshee_entry = ttk.Entry(self.pilot1_stats_frame, textvariable=self.pilot1_luchshee)
        self.pilot1_luchshee_entry.pack(side="left", padx=5, pady=5)

        pilot1_srednee_label = ttk.Label(self.pilot1_stats_frame, text="Среднее время")
        pilot1_srednee_label.pack(side="left", padx=5, pady=5)
        self.pilot1_srednee_entry = ttk.Entry(self.pilot1_stats_frame, textvariable=self.pilot1_srednee)
        self.pilot1_srednee_entry.pack(side="left", padx=5, pady=5)

        #Статистика для пилота 2
        pilot2_stats_frame = ttk.LabelFrame(self.stats_frame, text = "Статистика для пилота 2")
        pilot2_stats_frame.pack(side = "top", padx = 5, pady = 5, fill = "x")

        # Добавляем выбор фото пилота 2
        pilot2_stats_photo_label = ttk.Label(pilot2_stats_frame, text="Фото пилота:")
        pilot2_stats_photo_label.pack(side="left", padx=5, pady=5)
        pilot2_stats_photo_button = ttk.Button(pilot2_stats_frame, text="Выбрать фото", command=self.select_pilot2_stats_photo)
        pilot2_stats_photo_button.pack(side="left", padx=5, pady=5)
        self.pilot2_stats_photo_name_label = ttk.Label(pilot2_stats_frame, text="Фото не выбрано")
        self.pilot2_stats_photo_name_label.pack(side="left", padx=5, pady=5)
        
        # Добавляем выбор имени пилота 2
        pilot2_stats_name_label = ttk.Label(pilot2_stats_frame, text="Имя пилота:")
        pilot2_stats_name_label.pack(side="left", padx=5, pady=5)
        self.pilot2_stats_name_combobox = ttk.Combobox(pilot2_stats_frame, textvariable=self.pilot2_name, values=self.load_pilots())
        self.pilot2_stats_name_combobox.pack(side="left", padx=5, pady=5)

        pilot2_krugi_label = ttk.Label(pilot2_stats_frame, text = "Круги")
        pilot2_krugi_label.pack(side="left", padx = 5, pady = 5)
        self.pilot2_krugi_entry = ttk.Entry(pilot2_stats_frame, textvariable=self.pilot2_krugi)
        self.pilot2_krugi_entry.pack(side="left", padx = 5, pady = 5)

        pilot2_luchshee_label = ttk.Label(pilot2_stats_frame, text = "Лучшее время")
        pilot2_luchshee_label.pack(side="left", padx = 5, pady = 5)
        self.pilot2_luchshee_entry = ttk.Entry(pilot2_stats_frame, textvariable=self.pilot2_luchshee)
        self.pilot2_luchshee_entry.pack(side="left", padx = 5, pady = 5)

        pilot2_srednee_label = ttk.Label(pilot2_stats_frame, text = "Среднее время")
        pilot2_srednee_label.pack(side="left", padx = 5, pady = 5)
        self.pilot2_srednee_entry = ttk.Entry(pilot2_stats_frame, textvariable=self.pilot2_srednee)
        self.pilot2_srednee_entry.pack(side="left", padx = 5, pady = 5)

        #Статистика для пилота 3
        pilot3_stats_frame = ttk.LabelFrame(self.stats_frame, text = "Статистика для пилота 3")
        pilot3_stats_frame.pack(side = "top", padx = 5, pady = 5, fill = "x")

        # Добавляем выбор фото пилота 3
        pilot3_stats_photo_label = ttk.Label(pilot3_stats_frame, text="Фото пилота:")
        pilot3_stats_photo_label.pack(side="left", padx=5, pady=5)
        pilot3_stats_photo_button = ttk.Button(pilot3_stats_frame, text="Выбрать фото", command=self.select_pilot3_stats_photo)
        pilot3_stats_photo_button.pack(side="left", padx=5, pady=5)
        self.pilot3_stats_photo_name_label = ttk.Label(pilot3_stats_frame, text="Фото не выбрано")
        self.pilot3_stats_photo_name_label.pack(side="left", padx=5, pady=5)
        
        # Добавляем выбор имени пилота 3
        pilot3_stats_name_label = ttk.Label(pilot3_stats_frame, text="Имя пилота:")
        pilot3_stats_name_label.pack(side="left", padx=5, pady=5)
        self.pilot3_stats_name_combobox = ttk.Combobox(pilot3_stats_frame, textvariable=self.pilot3_name, values=self.load_pilots())
        self.pilot3_stats_name_combobox.pack(side="left", padx=5, pady=5)

        pilot3_krugi_label = ttk.Label(pilot3_stats_frame, text = "Круги")
        pilot3_krugi_label.pack(side="left", padx = 5, pady = 5)
        self.pilot3_krugi_entry = ttk.Entry(pilot3_stats_frame, textvariable=self.pilot3_krugi)
        self.pilot3_krugi_entry.pack(side="left", padx = 5, pady = 5)

        pilot3_luchshee_label = ttk.Label(pilot3_stats_frame, text = "Лучшее время")
        pilot3_luchshee_label.pack(side="left", padx = 5, pady = 5)
        self.pilot3_luchshee_entry = ttk.Entry(pilot3_stats_frame, textvariable=self.pilot3_luchshee)
        self.pilot3_luchshee_entry.pack(side="left", padx = 5, pady = 5)

        pilot3_srednee_label = ttk.Label(pilot3_stats_frame, text = "Среднее время")
        pilot3_srednee_label.pack(side="left", padx = 5, pady = 5)
        self.pilot3_srednee_entry = ttk.Entry(pilot3_stats_frame, textvariable=self.pilot3_srednee)
        self.pilot3_srednee_entry.pack(side="left", padx = 5, pady = 5)

        # Фрейм для данных менеджера и даты
        manager_frame = ttk.LabelFrame(self.root, text="Данные менеджера и даты")
        manager_frame.pack(padx=10, pady=10, fill="x")

        # Имя менеджера
        manager_name_label = ttk.Label(manager_frame, text="Имя менеджера:")
        manager_name_label.pack(side="left", padx=5, pady=5)
        self.manager_name_values = self.load_managers() # Загружаем имена менеджеров из файла
        self.manager_name_combobox = ttk.Combobox(manager_frame, textvariable=self.manager_name, values=self.manager_name_values)
        self.manager_name_combobox.pack(side="left", padx=5, pady=5)

        # ввод даты
        date_group_label = ttk.Label(manager_frame, text="Дата и группа:")
        date_group_label.pack(side="left", padx=5, pady=5)
        self.date_group_entry = ttk.Entry(manager_frame, textvariable=self.date_group)
        self.date_group_entry.pack(side="left", padx=5, pady=5)

        # Кнопка "Создать"
        generate_button = ttk.Button(self.root, text="Создать инфографику", command=self.generate_infographic, style="GreenButton.TButton") # Применяем стиль
        generate_button.pack(side="bottom", fill="x", pady=10) # Располагаем внизу и растягиваем по ширине

        # Предварительный просмотр (если нужно)
        self.preview_label = ttk.Label(self.root)  # Здесь будет отображаться картинка
        self.preview_label.pack()

    def select_team_logo(self):
        filename = filedialog.askopenfilename(initialdir="assets/logo", title="Выберите логотип команды", filetypes=(("Файлы изображений", "*.png;*.jpg;*.jpeg"), ("Все файлы", "*.*")))
        if filename:
            self.team_logo_path.set(filename)

    def select_pilot1_photo(self):
        filename = filedialog.askopenfilename(initialdir="assets/pilot", title="Выберите фото пилота 1", filetypes=(("Файлы изображений", "*.png;*.jpg;*.jpeg"), ("Все файлы", "*.*")))
        if filename:
            self.pilot1_photo_path.set(filename)
            # Обновляем текст в метке
            filename_short = filename.split("/")[-1]  # Получаем только имя файла
            self.pilot1_photo_name_label.config(text=filename_short)
        else:
            #Если файл не выбран возвращаем текст по умолчанию
            self.pilot1_photo_name_label.config(text="Фото не выбрано")

    def select_pilot2_photo(self):
        filename = filedialog.askopenfilename(initialdir="assets/pilot", title="Выберите фото пилота 2", filetypes=(("Файлы изображений", "*.png;*.jpg;*.jpeg"), ("Все файлы", "*.*")))
        if filename:
            self.pilot2_photo_path.set(filename)
            # Обновляем текст в метке
            filename_short = filename.split("/")[-1]  # Получаем только имя файла
            self.pilot2_photo_name_label.config(text=filename_short)
        else:
            #Если файл не выбран возвращаем текст по умолчанию
            self.pilot2_photo_name_label.config(text="Фото не выбрано")

    def select_pilot3_photo(self):
        filename = filedialog.askopenfilename(initialdir="assets/pilot", title="Выберите фото пилота 3", filetypes=(("Файлы изображений", "*.png;*.jpg;*.jpeg"), ("Все файлы", "*.*")))
        if filename:
            self.pilot3_photo_path.set(filename)
            # Обновляем текст в метке
            filename_short = filename.split("/")[-1]  # Получаем только имя файла
            self.pilot3_photo_name_label.config(text=filename_short)
        else:
            #Если файл не выбран возвращаем текст по умолчанию
            self.pilot3_photo_name_label.config(text="Фото не выбрано")

    def select_save_folder(self):
        """Выбор папки для сохранения изображений."""
        folder_path = filedialog.askdirectory(initialdir=self.save_folder_path.get(), title="Выберите папку для сохранения изображений")
        if folder_path:
            self.save_folder_path.set(folder_path)
            self.save_folder_display.config(text=folder_path)
            
    def open_save_folder(self):
        """Открывает папку сохранения в проводнике."""
        folder_path = self.save_folder_path.get()
        if os.path.exists(folder_path):
            # Открываем папку в проводнике Windows
            try:
                os.startfile(folder_path)  # Для Windows
            except AttributeError:
                # Для других ОС
                try:
                    subprocess.Popen(['xdg-open', folder_path])  # Linux
                except:
                    try:
                        subprocess.Popen(['open', folder_path])  # macOS
                    except:
                        messagebox.showerror("Ошибка", "Не удалось открыть папку в проводнике.")
        else:
            messagebox.showerror("Ошибка", f"Папка {folder_path} не существует.")
            # Создаем папку, если она не существует
            try:
                os.makedirs(folder_path)
                messagebox.showinfo("Информация", f"Папка {folder_path} была создана.")
                self.open_save_folder()  # Пробуем открыть снова
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать папку: {e}")

    def generate_infographic(self):
        # 1. Получить данные из полей ввода
        infographic_type = self.infographic_type.get()
        team_logo_file = self.team_logo_path.get()
        team_name = self.team_name.get()
        championship_name = self.championship_name.get()
        stage_number = self.stage_number.get()
        
        # Выбираем фотографии в зависимости от типа инфографики
        if infographic_type == "Статистика":
            pilot1_photo = self.pilot1_stats_photo_path.get()
            pilot2_photo = self.pilot2_stats_photo_path.get()
            pilot3_photo = self.pilot3_stats_photo_path.get()
        else:
            pilot1_photo = self.pilot1_photo_path.get()
            pilot2_photo = self.pilot2_photo_path.get()
            pilot3_photo = self.pilot3_photo_path.get()
            
        pilot1_name = self.pilot1_name.get()
        pilot2_name = self.pilot2_name.get()
        pilot3_name = self.pilot3_name.get()
        manager_name = self.manager_name.get()
        date_group = self.date_group.get()
        pilots_count = self.pilots_count.get()  # Получаем значение количества пилотов в гонке
        stages_count = self.stages_count.get() # Получаем количество этапов гонки
        pilot1_krugi = self.pilot1_krugi.get() # круги пилота 1
        pilot1_luchshee = self.pilot1_luchshee.get() # лучшее время пилота 1
        pilot1_srednee = self.pilot1_srednee.get() # среднее время пилота 1
        pilot2_krugi = self.pilot2_krugi.get() # круги пилота 2
        pilot2_luchshee = self.pilot2_luchshee.get() # лучшее время пилота 2
        pilot2_srednee = self.pilot2_srednee.get() # среднее время пилота 2
        pilot3_krugi = self.pilot3_krugi.get() # круги пилота 3
        pilot3_luchshee = self.pilot3_luchshee.get() # лучшее время пилота 3
        pilot3_srednee = self.pilot3_srednee.get() # среднее время пилота 3

        # 2. Проверить, что тип инфографики выбран
        if not infographic_type:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите тип инфографики.")
            return

         # 3. Вызвать функцию для генерации инфографики (из image_processor.py)
        try:
            #  ПЕРЕДАЁМ race_results!
            output_image = image_processor.create_infographic(infographic_type, team_logo_file, team_name, championship_name, stage_number, pilot1_photo, pilot1_name, pilot2_photo, pilot2_name, pilot3_photo, pilot3_name, manager_name, date_group, pilots_count, stages_count, pilot1_krugi, pilot1_luchshee, pilot1_srednee, pilot2_krugi, pilot2_luchshee, pilot2_srednee, pilot3_krugi, pilot3_luchshee, pilot3_srednee, self.race_results)
            # 4. Сохранить изображение
            self.save_image(output_image)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def save_image(self, image):
        """Сохраняет изображение в выбранную папку."""
        # Используем выбранную папку как начальную директорию
        filename = filedialog.asksaveasfilename(
            initialdir=self.save_folder_path.get(), 
            title="Сохранить инфографику", 
            defaultextension=".png", 
            filetypes=(("PNG файлы", "*.png"), ("JPEG файлы", "*.jpg;*.jpeg"), ("Все файлы", "*.*"))
        )
        if filename:
            try:
                image.save(filename)
                messagebox.showinfo("Успех", "Инфографика успешно сохранена!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении изображения: {e}")

    def save_template(self):
        """Сохраняет текущие значения полей в файл шаблона."""

        # Формируем имя файла по умолчанию
        default_filename = f"{self.team_name.get()} - {self.championship_name.get()}".replace(" ", "_")
        for char in r'\/:*?"<>|':  # Заменяем недопустимые символы
            default_filename = default_filename.replace(char, "_")
        default_filename += ".json"

        filename = filedialog.asksaveasfilename(
            initialdir="templates",
            title="Сохранить шаблон",
            initialfile=default_filename,
            defaultextension=".json",
            filetypes=(("JSON файлы", "*.json"), ("Все файлы", "*.*"))
        )

        if filename:
            try:
                # Собираем данные в словарь
                template_data = {
                    "infographic_type": self.infographic_type.get(),
                    "team_logo_path": self.team_logo_path.get(),
                    "team_name": self.team_name.get(),
                    "championship_name": self.championship_name.get(),
                    "stage_number": self.stage_number.get(),
                    "pilot1_photo_path": self.pilot1_photo_path.get(),
                    "pilot1_name": self.pilot1_name.get(),
                    "pilot2_photo_path": self.pilot2_photo_path.get(),
                    "pilot2_name": self.pilot2_name.get(),
                    "pilot3_photo_path": self.pilot3_photo_path.get(),
                    "pilot3_name": self.pilot3_name.get(),
                    "pilot1_stats_photo_path": self.pilot1_stats_photo_path.get(),
                    "pilot2_stats_photo_path": self.pilot2_stats_photo_path.get(),
                    "pilot3_stats_photo_path": self.pilot3_stats_photo_path.get(),
                    "manager_name": self.manager_name.get(),
                    "date_group": self.date_group.get(),
                    "pilots_count": self.pilots_count.get(),
                    "stages_count": self.stages_count.get(),
                    "pilot1_krugi": self.pilot1_krugi.get(),
                    "pilot1_luchshee": self.pilot1_luchshee.get(),
                    "pilot1_srednee": self.pilot1_srednee.get(),
                    "pilot2_krugi": self.pilot2_krugi.get(),
                    "pilot2_luchshee": self.pilot2_luchshee.get(),
                    "pilot2_srednee": self.pilot2_srednee.get(),
                    "pilot3_krugi": self.pilot3_krugi.get(),
                    "pilot3_luchshee": self.pilot3_luchshee.get(),
                    "pilot3_srednee": self.pilot3_srednee.get(),
                    "race_results": self.race_results,  # Добавляем результаты гонок
                    "save_folder_path": self.save_folder_path.get()  # Добавляем путь к папке сохранения
                }

                # Записываем в файл
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(template_data, f, indent=4, ensure_ascii=False)  # ensure_ascii=False для поддержки кириллицы

                # Обновляем метку с именем текущего шаблона
                template_name = os.path.basename(filename)
                self.current_template_label.config(text=template_name)

                messagebox.showinfo("Успех", "Шаблон успешно сохранен!")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении шаблона: {e}")

    def load_template(self):
        """Загружает данные из файла шаблона и применяет их к полям."""

        filename = filedialog.askopenfilename(
            initialdir="templates",
            title="Открыть шаблон",
            filetypes=(("JSON файлы", "*.json"), ("Все файлы", "*.*"))
        )

        if filename:
            # Спрашиваем подтверждение
            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите загрузить шаблон?\nВсе несохраненные данные будут потеряны."):
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        template_data = json.load(f)

                    # Обновляем метку с именем текущего шаблона
                    template_name = os.path.basename(filename)
                    self.current_template_label.config(text=template_name)

                    # Обновляем значения переменных и виджетов
                    for key, value in template_data.items():
                        if key == "infographic":
                            if key == "infographic_type":
                                self.infographic_type.set(value)
                        elif key == "team_logo_path":
                            self.team_logo_path.set(value)
                        elif key == "team_name":
                            self.team_name.set(value)
                            # Обновляем и список возможных значений
                            if value not in self.team_name_values:
                                self.team_name_values.append(value)
                            self.team_name_combobox["values"] = self.team_name_values
                        elif key == "championship_name":
                            self.championship_name.set(value)
                            if value not in self.championship_name_values:
                                self.championship_name_values.append(value)
                            self.championship_name_combobox["values"] = self.championship_name_values
                        elif key == "stage_number":
                            self.stage_number.set(value)
                        elif key == "pilot1_photo_path":
                            self.pilot1_photo_path.set(value)
                            # Обновляем имя файла в метке
                            if value:
                                filename_short = value.split("/")[-1]
                                self.pilot1_photo_name_label.config(text=filename_short)
                            else:
                                self.pilot1_photo_name_label.config(text="Фото не выбрано")
                        elif key == "pilot1_name":
                            self.pilot1_name.set(value)
                            if value not in self.pilot1_name_values:
                                self.pilot1_name_values.append(value)
                            self.pilot1_name_combobox["values"] = self.pilot1_name_values
                        elif key == "pilot2_photo_path":
                            self.pilot2_photo_path.set(value)
                            if value:
                                filename_short = value.split("/")[-1]
                                self.pilot2_photo_name_label.config(text=filename_short)
                            else:
                                self.pilot2_photo_name_label.config(text="Фото не выбрано")
                        elif key == "pilot2_name":
                            self.pilot2_name.set(value)
                            if value not in self.pilot2_name_values:
                                self.pilot2_name_values.append(value)
                            self.pilot2_name_combobox["values"] = self.pilot2_name_values
                        elif key == "pilot3_photo_path":
                            self.pilot3_photo_path.set(value)
                            if value:
                                filename_short = value.split("/")[-1]
                                self.pilot3_photo_name_label.config(text=filename_short)
                            else:
                                self.pilot3_photo_name_label.config(text="Фото не выбрано")
                        elif key == "pilot3_name":
                            self.pilot3_name.set(value)
                            if value not in self.pilot3_name_values:
                                 self.pilot3_name_values.append(value)
                            self.pilot3_name_combobox["values"] = self.pilot3_name_values
                        # Добавляем обработку новых полей для фотографий в разделе "Статистика"
                        elif key == "pilot1_stats_photo_path":
                            self.pilot1_stats_photo_path.set(value)
                            if value and hasattr(self, 'pilot1_stats_photo_name_label'):
                                filename_short = value.split("/")[-1]
                                self.pilot1_stats_photo_name_label.config(text=filename_short)
                            elif hasattr(self, 'pilot1_stats_photo_name_label'):
                                self.pilot1_stats_photo_name_label.config(text="Фото не выбрано")
                        elif key == "pilot2_stats_photo_path":
                            self.pilot2_stats_photo_path.set(value)
                            if value and hasattr(self, 'pilot2_stats_photo_name_label'):
                                filename_short = value.split("/")[-1]
                                self.pilot2_stats_photo_name_label.config(text=filename_short)
                            elif hasattr(self, 'pilot2_stats_photo_name_label'):
                                self.pilot2_stats_photo_name_label.config(text="Фото не выбрано")
                        elif key == "pilot3_stats_photo_path":
                            self.pilot3_stats_photo_path.set(value)
                            if value and hasattr(self, 'pilot3_stats_photo_name_label'):
                                filename_short = value.split("/")[-1]
                                self.pilot3_stats_photo_name_label.config(text=filename_short)
                            elif hasattr(self, 'pilot3_stats_photo_name_label'):
                                self.pilot3_stats_photo_name_label.config(text="Фото не выбрано")
                        elif key == "manager_name":
                            self.manager_name.set(value)
                            if value not in self.manager_name_values:
                                self.manager_name_values.append(value)
                            self.manager_name_combobox["values"] = self.manager_name_values
                        elif key == "date_group":
                            self.date_group.set(value)
                        elif key == "pilots_count":
                            self.pilots_count.set(value)
                        elif key == "stages_count":
                            self.stages_count.set(value)
                        elif key == "pilot1_krugi":
                            self.pilot1_krugi.set(value)
                        elif key == "pilot1_luchshee":
                            self.pilot1_luchshee.set(value)
                        elif key == "pilot1_srednee":
                            self.pilot1_srednee.set(value)
                        elif key == "pilot2_krugi":
                            self.pilot2_krugi.set(value)
                        elif key == "pilot2_luchshee":
                            self.pilot2_luchshee.set(value)
                        elif key == "pilot2_srednee":
                            self.pilot2_srednee.set(value)
                        elif key == "pilot3_krugi":
                            self.pilot3_krugi.set(value)
                        elif key == "pilot3_luchshee":
                            self.pilot3_luchshee.set(value)
                        elif key == "pilot3_srednee":
                            self.pilot3_srednee.set(value)
                        elif key == "race_results":
                            self.race_results = value # Загружаем результаты
                            self.update_results_table()
                        elif key == "save_folder_path":
                            self.save_folder_path.set(value)
                            self.save_folder_display.config(text=value)

                    self.update_ui()  # Важно! Обновляем интерфейс после загрузки
                    messagebox.showinfo("Успех", "Шаблон успешно загружен!")

                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при загрузке шаблона: {e}")

    def setup_results_table(self):
        """Настраивает таблицу результатов (начальное состояние)."""
        for item in self.results_table.get_children():  # Очищаем таблицу
            self.results_table.delete(item)

        try:
            num_stages = int(self.stages_count.get())
            for i in range(1, num_stages + 1):
                # Ищем результат для этапа i
                result = next((r for r in self.race_results if r["stage"] == i), None)
                place = result["place"] if result and result["place"] is not None else ""  # Если результат есть и не None, берем место, иначе пусто
                self.results_table.insert("", "end", values=(i, place))
        except ValueError:
            pass  # Обработка ошибки, если введено не число

    def update_results_table(self, event=None):
        """Обновляет таблицу результатов при изменении количества этапов."""
        # Запоминаем текущие результаты (какие смогли получить из таблицы)
        current_results = []
        for item_id in self.results_table.get_children():
            item = self.results_table.item(item_id)
            try:
                stage = int(item["values"][0])
                place = int(item["values"][1]) if item["values"][1] else None
                if place is not None: # Добавляем только если место указано
                    current_results.append({"stage": stage, "place": place})
            except ValueError:
                pass # Если не смогли преобразовать в числа - пропускаем

        # Очищаем таблицу
        for item in self.results_table.get_children():
            self.results_table.delete(item)

        # Заполняем заново, пытаясь сохранить данные
        try:
            num_stages = int(self.stages_count.get())
            
            # Сначала обновляем self.race_results, сохраняя существующие данные
            # Создаем временную копию для работы
            updated_results = []
            
            # Добавляем существующие результаты, которые не превышают текущее количество этапов
            for result in self.race_results:
                if result["stage"] <= num_stages:
                    updated_results.append(result)
            
            # Добавляем результаты из текущей таблицы, если их нет в обновленных результатах
            for result in current_results:
                if result["stage"] <= num_stages and not any(r["stage"] == result["stage"] for r in updated_results):
                    updated_results.append(result)
            
            # Добавляем пустые записи для отсутствующих этапов
            for i in range(1, num_stages + 1):
                if not any(r["stage"] == i for r in updated_results):
                    updated_results.append({"stage": i, "place": None})
            
            # Обновляем self.race_results
            self.race_results = updated_results
            
            # Заполняем таблицу данными из обновленного self.race_results
            for i in range(1, num_stages + 1):
                # Ищем результат для этапа i
                result = next((r for r in self.race_results if r["stage"] == i), None)
                place = result["place"] if result and result["place"] is not None else ""
                self.results_table.insert("", "end", values=(i, place))

        except ValueError:
            pass  # Обработка ошибки, если введено не число

    def edit_place(self, event):
        """Редактирование места в таблице."""
        item_id = self.results_table.focus()  # Получаем ID строки
        if item_id:
            column = self.results_table.identify_column(event.x) # Получаем ID столбца
            if column == "#2":  # Если кликнули по столбцу "Место"
                x, y, width, height = self.results_table.bbox(item_id, column)
                item = self.results_table.item(item_id)
                stage = item['values'][0]  # Номер этапа
                current_place = item['values'][1] # Текущее место

                # Создаем поле ввода
                entry = ttk.Entry(self.results_table, width=width)
                entry.place(x=x, y=y, width=width, height=height)
                entry.insert(0, current_place)  # Вставляем текущее значение
                entry.focus_set()

                def save_edit(event=None):
                    """Сохраняет изменения."""
                    try:
                        new_place = int(entry.get())
                        pilots_count = int(self.pilots_count.get())
                        if 1 <= new_place <= pilots_count:
                            # Обновляем данные в таблице
                            self.results_table.item(item_id, values=(stage, new_place))

                            # Обновляем данные в self.race_results
                            for result in self.race_results:
                                if result["stage"] == stage:
                                    result["place"] = new_place
                                    break
                            else:  # Если не нашли результат для этого этапа (такого быть не должно)
                                self.race_results.append({"stage": stage, "place": new_place})
                            entry.destroy()
                        else:
                            messagebox.showerror("Ошибка", f"Место должно быть целым числом от 1 до {pilots_count}.")
                    except ValueError:
                        messagebox.showerror("Ошибка", "Введите целое число.")

                entry.bind("<Return>", save_edit)  # Сохраняем по Enter
                entry.bind("<FocusOut>", lambda e: entry.destroy())  # Закрываем поле, если потерян фокус

    # Добавляем новые методы для выбора фотографий для раздела "Статистика"
    def select_pilot1_stats_photo(self):
        filename = filedialog.askopenfilename(initialdir="assets/pilot", title="Выберите фото пилота 1 для статистики", filetypes=(("Файлы изображений", "*.png;*.jpg;*.jpeg"), ("Все файлы", "*.*")))
        if filename:
            self.pilot1_stats_photo_path.set(filename)
            # Обновляем текст в метке
            filename_short = filename.split("/")[-1]  # Получаем только имя файла
            self.pilot1_stats_photo_name_label.config(text=filename_short)
        else:
            #Если файл не выбран возвращаем текст по умолчанию
            self.pilot1_stats_photo_name_label.config(text="Фото не выбрано")
            
    def select_pilot2_stats_photo(self):
        filename = filedialog.askopenfilename(initialdir="assets/pilot", title="Выберите фото пилота 2 для статистики", filetypes=(("Файлы изображений", "*.png;*.jpg;*.jpeg"), ("Все файлы", "*.*")))
        if filename:
            self.pilot2_stats_photo_path.set(filename)
            # Обновляем текст в метке
            filename_short = filename.split("/")[-1]  # Получаем только имя файла
            self.pilot2_stats_photo_name_label.config(text=filename_short)
        else:
            #Если файл не выбран возвращаем текст по умолчанию
            self.pilot2_stats_photo_name_label.config(text="Фото не выбрано")
            
    def select_pilot3_stats_photo(self):
        filename = filedialog.askopenfilename(initialdir="assets/pilot", title="Выберите фото пилота 3 для статистики", filetypes=(("Файлы изображений", "*.png;*.jpg;*.jpeg"), ("Все файлы", "*.*")))
        if filename:
            self.pilot3_stats_photo_path.set(filename)
            # Обновляем текст в метке
            filename_short = filename.split("/")[-1]  # Получаем только имя файла
            self.pilot3_stats_photo_name_label.config(text=filename_short)
        else:
            #Если файл не выбран возвращаем текст по умолчанию
            self.pilot3_stats_photo_name_label.config(text="Фото не выбрано")