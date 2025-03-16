from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter, ImageEnhance
import math

def create_infographic(infographic_type, team_logo_file, team_name, championship_name, stage_number,
                       pilot1_photo, pilot1_name, pilot2_photo, pilot2_name, pilot3_photo, pilot3_name,
                       manager_name, date_group, pilots_count, stages_count,
                       pilot1_krugi, pilot1_luchshee, pilot1_srednee,
                       pilot2_krugi, pilot2_luchshee, pilot2_srednee,
                       pilot3_krugi, pilot3_luchshee, pilot3_srednee,
                       race_results=None):  # Добавляем race_results
    """
    Создает инфографику в зависимости от выбранного типа.
    """

    # 1. Выбрать фон в зависимости от типа инфографики
    background_image_path = "assets/background.png"
    try:
        # Создаем непрозрачный базовый слой с цветом #848484
        base_layer = Image.new('RGB', (1000, 1400), (132, 132, 132))  # #848484 в RGB, фиксированный размер
        
        # Загружаем фоновое изображение
        background = Image.open(background_image_path).convert("RGBA")
        
        # Накладываем фоновое изображение на базовый слой
        # Создаем новый RGB-образ для наложения RGBA на RGB
        final_background = Image.new('RGB', base_layer.size, (132, 132, 132))
        final_background.paste(base_layer, (0, 0))
        final_background.paste(background, (0, 0), background)
        
        background = final_background
    except FileNotFoundError:
        print(f"Error: Background image not found at {background_image_path}")
        return None

    draw = ImageDraw.Draw(background)

    # Функция для отрисовки текста с обводкой и свечением
    def draw_text_with_effects(x, y, text, font, fill_color):
        # Создаем временное изображение для текста с обводкой и свечением
        # Делаем его больше на размер свечения с каждой стороны
        glow_size = 50 
        padding = glow_size * 2
        
        # Получаем размеры текста
        text_width = draw.textlength(text, font=font)
        text_height = font.size
        
        # Создаем временное изображение с альфа-каналом
        temp_img = Image.new('RGBA', (int(text_width + padding * 2), int(text_height + padding * 2)), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        
        # Рисуем текст с черной обводкой (смещая его на 1-2 пикселя в разные стороны)
        outline_thickness = 1  
        for offset_x in range(-outline_thickness, outline_thickness + 1):
            for offset_y in range(-outline_thickness, outline_thickness + 1):
                if offset_x == 0 and offset_y == 0:
                    continue  
                temp_draw.text((padding + offset_x, padding + offset_y), text, font=font, fill=(0, 0, 0, 255))
        
        # Рисуем основной текст
        temp_draw.text((padding, padding), text, font=font, fill=fill_color)
        
        # Создаем копию для свечения
        glow_img = temp_img.copy()
        
        # Применяем размытие для создания свечения
        glow_img = glow_img.filter(ImageFilter.GaussianBlur(glow_size))
        
        # Усиливаем яркость свечения
        enhancer = ImageEnhance.Brightness(glow_img)
        glow_img = enhancer.enhance(100)  # Значительно увеличиваем яркость свечения
        
        # Создаем маску для свечения только вокруг текста
        mask = Image.new('L', temp_img.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.text((padding, padding), text, font=font, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(glow_size/2))
        
        # Применяем цвет свечения
        r, g, b = fill_color[0], fill_color[1], fill_color[2]
        glow_color = Image.new('RGBA', glow_img.size, (r, g, b, 255))  # Увеличиваем непрозрачность до максимума
        
        # Комбинируем свечение с маской
        glow_applied = Image.composite(glow_color, Image.new('RGBA', glow_img.size, (0, 0, 0, 0)), mask)
        
        # Создаем финальное изображение с эффектами
        result_img = Image.new('RGBA', temp_img.size, (0, 0, 0, 0))
        
        # Сначала накладываем свечение
        result_img = Image.alpha_composite(result_img, glow_applied)
        
        # Затем накладываем текст с обводкой
        result_img = Image.alpha_composite(result_img, temp_img)
        
        # Накладываем результат на фон (без использования альфа-канала)
        background.paste(result_img, (int(x - padding), int(y - padding)), result_img)

    # 2. Загрузить шрифт
    font_path = "assets/BuyanBold.ttf"
    font_path_thin = "assets/BuyanThin.ttf"
    font_size = 75
    font_size_small = 50
    font_size_date = 33
    font_size_very_small = 25  # Новый размер шрифта для мелких подписей
    font_pilots = ImageFont.truetype(font_path, font_size_small)
    font_date = ImageFont.truetype(font_path, font_size_date)
    try:
        font = ImageFont.truetype(font_path, font_size)
        font_small = ImageFont.truetype(font_path, font_size_small)
        font_date = ImageFont.truetype(font_path, font_size_date)
        font_thin = ImageFont.truetype(font_path_thin, font_size_small)
        font_very_small = ImageFont.truetype(font_path_thin, font_size_very_small)  # Тонкий шрифт для мелких подписей
    except IOError:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_date = ImageFont.load_default()
        font_thin = ImageFont.load_default()
        font_very_small = ImageFont.load_default()  # Новый шрифт для мелких подписей

    text_color = (255, 255, 255)
    pilot_name_color = (255, 193, 15)
    manager_name_color = (255, 0, 0)

    if infographic_type == "Состав пилотов":
        # Добавляем определение font_manager
        font_manager = ImageFont.truetype(font_path, font_size)
        # 3. Разместить логотип команды
        # Загрузить дефолтный логотип
        default_logo_path = "assets/logo.png"
        try:
            default_logo = Image.open(default_logo_path).convert("RGBA")
            default_logo = default_logo.resize((200, 200))
        except FileNotFoundError:
            print(f"Error: Default logo not found at {default_logo_path}")
            default_logo = None

        if team_logo_file:
            try:
                logo = Image.open(team_logo_file).convert("RGBA")  # Открываем логотип
                logo = logo.resize((200, 200))  # Уменьшаем размер
                background.paste(logo, (400, 35), logo)  # Координаты и маска
            except Exception as e:
                print(f"Error loading logo: {e}")
        elif default_logo: # Если логотип не выбран
            background.paste(default_logo, (400, 35), default_logo)

        # 4. Разместить текст
        # Значения по умолчанию
        default_team_name = "Название команды"
        default_championship_name = "Название чемпионата"
        default_pilot1_name = "Пилот 1"
        default_pilot2_name = "Пилот 2"
        default_pilot3_name = "Пилот 3"
        default_manager_name = "Имя менеджера"
        default_date_group = "Дата     |     Группа"

        # Используем значения по умолчанию, если поля пустые
        team_name = team_name or default_team_name
        championship_name = championship_name or default_championship_name
        pilot1_name = pilot1_name or default_pilot1_name
        pilot2_name = pilot2_name or default_pilot2_name
        pilot3_name = pilot3_name or default_pilot3_name
        manager_name = manager_name or default_manager_name
        date_group = date_group or default_date_group

        # Фрейм для выбора логотипа и ввода данных команды
        team_name_width = draw.textlength(team_name, font=font)
        championship_name_width = draw.textlength(championship_name, font=font_small)
        stage_number_width = draw.textlength(f"Этап {stage_number}", font=font_small)

        draw_text_with_effects((1000 - team_name_width) / 2, 240, team_name, font, text_color)
        draw_text_with_effects((1000 - championship_name_width) / 2, 335, championship_name, font_small, text_color)
        draw_text_with_effects((1000 - stage_number_width) / 2, 395, f"Этап {stage_number}", font_small, text_color)

        # 5. Разместить фото и имена пилотов
        pilot_photo_size = (500, 500)  # Размер для фотографий

        # Загрузить дефолтное фото пилота
        default_pilot_photo_path = "assets/pilot.png"
        try:
            default_pilot_photo = Image.open(default_pilot_photo_path).convert("RGBA")
            default_pilot_photo = default_pilot_photo.resize(pilot_photo_size)
        except FileNotFoundError:
            print(f"Error: Default pilot photo not found at {default_pilot_photo_path}")
            default_pilot_photo = None

        # Pilot 1
        try:
            if pilot1_photo:
                photo1 = Image.open(pilot1_photo).convert("RGBA")
                photo1 = photo1.resize(pilot_photo_size)
                background.paste(photo1, (-80, 480), photo1)  # пример координат
            elif default_pilot_photo:
                background.paste(default_pilot_photo, (-80, 480), default_pilot_photo)
            pilot1_name_width = draw.textlength(pilot1_name, font=font_pilots)
            draw_text_with_effects((330 - pilot1_name_width) / 2, 990, pilot1_name, font_pilots, pilot_name_color)
        except Exception as e:
            print(f"Error loading pilot 1 photo: {e}")

        # Pilot 2
        try:
            if pilot2_photo:
                photo2 = Image.open(pilot2_photo).convert("RGBA")
                photo2 = photo2.resize(pilot_photo_size)
                background.paste(photo2, (246, 480), photo2)
            elif default_pilot_photo:
                background.paste(default_pilot_photo, (246, 480), default_pilot_photo)
            pilot2_name_width = draw.textlength(pilot2_name, font=font_pilots)
            draw_text_with_effects((1000 - pilot2_name_width) / 2, 990, pilot2_name, font_pilots, pilot_name_color)
        except Exception as e:
            print(f"Error loading pilot 2 photo: {e}")

        # Pilot 3
        try:
            if pilot3_photo:
                photo3 = Image.open(pilot3_photo).convert("RGBA")
                photo3 = photo3.resize(pilot_photo_size)
                background.paste(photo3, (575, 480), photo3)
            elif default_pilot_photo:
                background.paste(default_pilot_photo, (575, 480), default_pilot_photo)
            pilot3_name_width = draw.textlength(pilot3_name, font=font_pilots)
            draw_text_with_effects((1670 - pilot3_name_width) / 2, 990, pilot3_name, font_pilots, pilot_name_color)
        except Exception as e:
            print(f"Error loading pilot 3 photo: {e}")

        # 6. Разместить имя менеджера и дату
        manager_text = "Менеджер"
        manager_width = draw.textlength(manager_text, font=font_small)
        draw_text_with_effects((1000 - manager_width) / 2, 1154, manager_text, font_small, text_color)

        manager_name_width = draw.textlength(manager_name, font=font_manager)
        draw_text_with_effects((1000 - manager_name_width) / 2, 1084, manager_name, font_manager, manager_name_color)

        date = draw.textlength(date_group, font=font_date)
        draw_text_with_effects((1000 - date) / 2, 1320, date_group, font_date, text_color)

    elif infographic_type == "Результаты гонок":
        # Логотип
        default_logo_path = "assets/logo.png"
        try:
            default_logo = Image.open(default_logo_path).convert("RGBA")
            default_logo = default_logo.resize((200, 200))
        except FileNotFoundError:
            print(f"Error: Default logo not found at {default_logo_path}")
            default_logo = None

        if team_logo_file:
            try:
                logo = Image.open(team_logo_file).convert("RGBA")
                logo = logo.resize((200, 200))
                background.paste(logo, (400, 35), logo)
            except Exception as e:
                print(f"Error loading logo: {e}")
                logo = default_logo  # Используем дефолтный
        elif default_logo:
            background.paste(default_logo, (400, 35), default_logo)

        # Текст
        team_name_width = draw.textlength(team_name, font=font)
        championship_name_width = draw.textlength(championship_name, font=font_small)
        results_text_width = draw.textlength("РЕЗУЛЬТАТЫ ГОНОК", font=font_small)
        legend_text_width = draw.textlength("ОБОЗНАЧЕНИЯ", font=font_very_small)

        draw_text_with_effects((1000 - team_name_width) / 2, 225, team_name, font, text_color)
        draw_text_with_effects((1000 - championship_name_width) / 2, 300, championship_name, font_small, text_color)
        draw_text_with_effects((1000 - results_text_width) / 2, 385, "РЕЗУЛЬТАТЫ ГОНОК", font_small, text_color)
        draw.text(((1000 - legend_text_width) / 2, 1330), "ОБОЗНАЧЕНИЯ", font=font_very_small, fill=text_color)

        # Шрифт для менеджера (в блоке "Результаты гонок")
        font_manager = ImageFont.truetype(font_path, font_size)


        # Диаграмма
        diagram_top = 470
        diagram_bottom = 1150
        diagram_height = diagram_bottom - diagram_top
        diagram_left = 90
        diagram_right = 965
        diagram_width = diagram_right - diagram_left

        try:
            num_stages = int(stages_count)
            num_pilots = int(pilots_count)
            if num_stages <= 0:
                raise ValueError("Количество этапов должно быть больше нуля")
            if num_pilots <= 0:
                raise ValueError("Количество пилотов должно быть больше нуля")
        except (ValueError, TypeError) as e:
            print(f"Error parsing stages or pilots count: {e}")
            return None

        bar_spacing = 20
        bar_height = (diagram_height - (num_stages - 1) * bar_spacing) / num_stages
        bar_color = ImageColor.getrgb("#ffc10f")
        outline_color = ImageColor.getrgb("#ff0000")
        unfilled_color = ImageColor.getrgb("#1f1f1f")

        for i in range(num_stages):
            bar_top = diagram_top + i * (bar_height + bar_spacing)
            bar_bottom = bar_top + bar_height

            # Сначала рисуем незаполненную часть полосы
            draw.rounded_rectangle(
                (diagram_left, bar_top, diagram_right, bar_bottom),
                radius=20,
                fill=unfilled_color,
                outline=None, # Контур пока не рисуем
                width=0
            )

            # Заполнение полосы (если есть данные)
            if race_results and i < len(race_results):
                try:
                    place = int(race_results[i]["place"]) if race_results[i]["place"] is not None else None
                    if place is not None:
                        if not 1 <= place <= num_pilots:
                            raise ValueError("Неверное место")
                        fill_width = (diagram_width * (num_pilots - place + 1)) / num_pilots

                        # Рисуем заполненную часть
                        draw.rounded_rectangle(
                            (diagram_left, bar_top, diagram_left + fill_width, bar_bottom),
                            radius=20,
                            fill=bar_color,
                            outline=None,  # Контур пока не рисуем
                            width=0
                        )
                except (ValueError, TypeError) as e:
                    print(f"Error processing result for stage {i+1}: {e}")

            # Рисуем контур *после* заполнения, чтобы он был сверху
            draw.rounded_rectangle(
                (diagram_left, bar_top, diagram_right, bar_bottom),
                radius=20,
                outline=outline_color,
                width=5
            )

            # Номер этапа
            stage_number_text = str(i + 1)
            stage_number_width = draw.textlength(stage_number_text, font=font_small)
            stage_number_x = 35 + (25 - stage_number_width) / 2
            stage_number_y = bar_top + (bar_height - font_small.size) / 2
            draw_text_with_effects(stage_number_x, stage_number_y, stage_number_text, font_small, ImageColor.getrgb("#ff0000"))

        # Подписи к шкале
        draw_text_with_effects(diagram_left + 90, 1265, "ЭТАП ЧЕМПИОНАТА", font_small, ImageColor.getrgb("#ff0000"))
        draw_text_with_effects(diagram_right - draw.textlength("ПОЗИЦИЯ НА ФИНИШЕ", font=font_small) - 90, 1265, "ПОЗИЦИЯ НА ФИНИШЕ", font_small, ImageColor.getrgb("#00ff00"))

        for i in range(num_pilots):
            pil_number_text = str(num_pilots - i)
            pil_number_width = draw.textlength(pil_number_text, font=font_small)
            pil_number_x = diagram_left + (diagram_width / num_pilots) * i + (diagram_width / (num_pilots * 2)) - (pil_number_width / 2) + 25
            pil_number_y = 1165
            draw_text_with_effects(pil_number_x, pil_number_y, pil_number_text, font_small, ImageColor.getrgb("#00ff00"))

    elif infographic_type == "Статистика":
        # Логотип
        default_logo_path = "assets/logo.png"
        try:
            default_logo = Image.open(default_logo_path).convert("RGBA")
            default_logo = default_logo.resize((200, 200))
        except FileNotFoundError:
            print(f"Error: Default logo not found at {default_logo_path}")
            default_logo = None

        if team_logo_file:
            try:
                logo = Image.open(team_logo_file).convert("RGBA")
                logo = logo.resize((200, 200))
                background.paste(logo, (400, 35), logo)
            except Exception as e:
                print(f"Error loading logo: {e}")
                logo = default_logo  # Используем дефолтный
        elif default_logo:
            background.paste(default_logo, (400, 35), default_logo)

        # Загружаем дефолтное фото пилота
        default_pilot_photo_path = "assets/pilot.png"
        try:
            default_pilot_photo = Image.open(default_pilot_photo_path).convert("RGBA")
            default_pilot_photo = default_pilot_photo.resize((350, 350))  # Размер для фото в блоке пилота
        except FileNotFoundError:
            print(f"Error: Default pilot photo not found at {default_pilot_photo_path}")
            default_pilot_photo = None

        # Заголовки
        team_name_width = draw.textlength(team_name, font=font)
        championship_name_width = draw.textlength(championship_name, font=font_small)
        stats_text_width = draw.textlength("СТАТИСТИКА ПИЛОТОВ", font=font_small)

        draw_text_with_effects((1000 - team_name_width) / 2, 225, team_name, font, text_color)
        draw_text_with_effects((1000 - championship_name_width) / 2, 300, championship_name, font_small, text_color)
        draw_text_with_effects((1000 - stats_text_width) / 2, 385, "СТАТИСТИКА ПИЛОТОВ", font_small, text_color)

        # Определяем цвета для диаграмм и таблиц
        pilot1_color = ImageColor.getrgb("#d72132")  # Красный
        pilot2_color = ImageColor.getrgb("#da9027")  # Оранжевый
        pilot3_color = ImageColor.getrgb("#0065dc")  # Синий
        
        # Функция для рисования круговой диаграммы
        def draw_pie_chart(center_x, center_y, radius, values, colors, labels, title):
            
            
            # Проверяем, что у нас есть данные для диаграммы
            if not values or sum(values) == 0:
                # Если нет данных, рисуем пустой круг
                draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), 
                             outline=ImageColor.getrgb("#ffffff"), width=4)
                no_data_text = "Нет данных"
                no_data_width = draw.textlength(no_data_text, font=font_small)
                draw_text_with_effects(center_x - no_data_width / 2, center_y - font_small.size / 2, 
                                      no_data_text, font_small, text_color)
                return
            
            # Рисуем круговую диаграмму
            total = sum(values)
            start_angle = 0
            
            for i, value in enumerate(values):
                if value <= 0:
                    continue
                    
                angle = 360 * value / total
                end_angle = start_angle + angle
                
                # Рисуем сектор
                draw.pieslice((center_x - radius, center_y - radius, center_x + radius, center_y + radius), 
                              start=start_angle, end=end_angle, fill=colors[i], outline=ImageColor.getrgb("#1f1f1f"), width=4)
                
                start_angle = end_angle
        
        # Функция для отображения блока пилота
        def draw_pilot_block(x, y, photo_path, name, krugi, luchshee, srednee, color):
            # Размер фото пилота 
            photo_size = (350, 350)
            
            # Загружаем фото пилота
            try:
                if photo_path:
                    photo = Image.open(photo_path).convert("RGBA")
                    photo = photo.resize(photo_size)
                    background.paste(photo, (x, y), photo)
                elif default_pilot_photo:  # Используем дефолтное фото, если фото не выбрано
                    background.paste(default_pilot_photo, (x, y), default_pilot_photo)
                else:
                    # Если дефолтное фото недоступно, рисуем пустой прямоугольник
                    draw.rectangle((x, y, x + photo_size[0], y + photo_size[1]), 
                                  outline=color, width=2)
            except Exception as e:
                print(f"Error loading pilot photo: {e}")
                # Если ошибка при загрузке фото, пробуем использовать дефолтное
                if default_pilot_photo:
                    background.paste(default_pilot_photo, (x, y), default_pilot_photo)
                else:
                    # Если дефолтное фото недоступно, рисуем пустой прямоугольник
                    draw.rectangle((x, y, x + photo_size[0], y + photo_size[1]), 
                                  outline=color, width=2)
            
            # Отображаем имя пилота (цвет пилота)
            name_width = draw.textlength(name, font=font_small)
            draw_text_with_effects(x + (photo_size[0] - name_width) / 2, y + photo_size[1] + 10, 
                     name, font_small, color)
            
            # Отображаем количество кругов (белый цвет, жирный шрифт)
            krugi_text = f"кругов: {krugi}"
            krugi_width = draw.textlength(krugi_text, font=font_small)
            draw_text_with_effects(x + (photo_size[0] - krugi_width) / 2, y + photo_size[1] + 60, 
                     krugi_text, font_small, text_color)  # Белый цвет, жирный шрифт
            
            # Отображаем лучшее и среднее время
            luchshee_width = draw.textlength(luchshee, font=font_thin)
            srednee_width = draw.textlength(srednee, font=font_thin)
            
            # Расстояние между показателями времени
            time_spacing = 20
            
            # Общая ширина блока с временем
            total_time_width = luchshee_width + srednee_width + time_spacing
            
            # Координаты для лучшего времени
            luchshee_x = x + (photo_size[0] - total_time_width) / 2
            luchshee_y = y + photo_size[1] + 110
            
            # Координаты для среднего времени
            srednee_x = luchshee_x + luchshee_width + time_spacing
            srednee_y = luchshee_y
            
            # Отображаем лучшее время (зеленый цвет)
            draw.text((luchshee_x, luchshee_y), luchshee, font=font_thin, fill=ImageColor.getrgb("#00ff00"))
            
            # Отображаем среднее время (голубой цвет)
            draw.text((srednee_x, srednee_y), srednee, font=font_thin, fill=ImageColor.getrgb("#00ffff"))
            
            # Отображаем подписи "best" и "avg"
            best_text = "best"
            avg_text = "avg"
            
            best_width = draw.textlength(best_text, font=font_very_small)
            avg_width = draw.textlength(avg_text, font=font_very_small)
            
            # Координаты для подписей
            best_x = luchshee_x + (luchshee_width - best_width) / 2
            best_y = luchshee_y + 50
            
            avg_x = srednee_x + (srednee_width - avg_width) / 2
            avg_y = srednee_y + 50
            
            # Отображаем подписи (зеленый и голубой)
            draw.text((best_x, best_y), best_text, font=font_very_small, fill=ImageColor.getrgb("#00ff00"))
            draw.text((avg_x, avg_y), avg_text, font=font_very_small, fill=ImageColor.getrgb("#00ffff"))
        
        # Получаем данные пилотов
        pilot_names = [pilot1_name, pilot2_name, pilot3_name]
        pilot_colors = [pilot1_color, pilot2_color, pilot3_color]
        
        # Преобразуем данные о кругах в числа
        try:
            pilot1_krugi_val = int(pilot1_krugi) if pilot1_krugi else 0
        except ValueError:
            pilot1_krugi_val = 0
            
        try:
            pilot2_krugi_val = int(pilot2_krugi) if pilot2_krugi else 0
        except ValueError:
            pilot2_krugi_val = 0
            
        try:
            pilot3_krugi_val = int(pilot3_krugi) if pilot3_krugi else 0
        except ValueError:
            pilot3_krugi_val = 0
        
        # Данные для круговой диаграммы кругов
        krugi_values = [pilot1_krugi_val, pilot2_krugi_val, pilot3_krugi_val]
        
        # Рисуем круговую диаграмму (центр по x, центр по y, радиус)
        # Размер диаграммы 380 пикселей, значит радиус 190
        draw_pie_chart(500, 590, 130, krugi_values, pilot_colors, pilot_names, "")
        
        # Добавляем круг поверх диаграммы для отображения общего количества кругов
        center_x, center_y = 500, 590  # Те же координаты, что и у диаграммы
        inner_circle_radius = 100
        
        # Рисуем внутренний круг
        draw.ellipse(
            (center_x - inner_circle_radius, center_y - inner_circle_radius, 
             center_x + inner_circle_radius, center_y + inner_circle_radius),
            fill=ImageColor.getrgb("#1f1f1f"),
            outline=None
        )
        
        # Вычисляем общее количество кругов
        total_krugi = pilot1_krugi_val + pilot2_krugi_val + pilot3_krugi_val
        
        # Отображаем общее количество кругов
        total_krugi_text = str(total_krugi)
        total_krugi_width = draw.textlength(total_krugi_text, font=font)
        draw_text_with_effects(
            (center_x - total_krugi_width / 2), (center_y - font.size / 2 - 10),
            total_krugi_text,
            font,
            text_color
        )
        
        # Добавляем подпись "кругов"
        krugi_label = "кругов"
        krugi_label_width = draw.textlength(krugi_label, font=font_very_small)
        draw.text(
            ((center_x - krugi_label_width / 2), (center_y + 30)),
            krugi_label,
            font=font_very_small,
            fill=text_color
        )
        
        # Рисуем блоки пилотов
        # Пилот 1 - слева от диаграммы
        draw_pilot_block(-25, 550, pilot1_photo, pilot1_name, pilot1_krugi_val, 
                        pilot1_luchshee or "—", pilot1_srednee or "—", pilot1_color)
        
        # Пилот 2 - справа от диаграммы
        draw_pilot_block(665, 550, pilot2_photo, pilot2_name, pilot2_krugi_val, 
                        pilot2_luchshee or "—", pilot2_srednee or "—", pilot2_color)
        
        # Пилот 3 - снизу от диаграммы
        draw_pilot_block(325, 750, pilot3_photo, pilot3_name, pilot3_krugi_val, 
                        pilot3_luchshee or "—", pilot3_srednee or "—", pilot3_color)
        
        # Рисуем информацию о дате и этапе
        date = draw.textlength(date_group, font=font_date)
        draw_text_with_effects((1000 - date) / 2, 1320, date_group, font_date, text_color)

    else:
        draw_text_with_effects(100, 100, "Другие типы инфографики пока не реализованы", font, text_color)

    return background