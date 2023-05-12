# В данном документе представлено соглашение о терминах, используемых в проекте "Школьная лаборатория"
* ***Мультисенсор*** - главное устройство, обеспечивающее опрос датчиков и отправку данных в приложении через Bluetooth
* ***Команда*** - инструкция для выполнения каких-либо действий
* ***Ответ*** - отклик устройства, получившего определённую команду
* ***Параметр*** - характеристика, определяющая поведение какого-либо объекта (например - датчика), которую можно прочитать и изменить
* ***Данные*** - результат измерения датчика - физические единицы измеренной величины, представленные в виде числа с плавающей точкой
* ***Датчик*** - сущность, преобразующая определённые внешние воздействия в значения физических величин в виде чисел с плавающей точкой
* ***Канал датчика*** - часть датчика, отвечающая за измерение конкретного физического воздействия (например, ускорение по оси Х, ускорение по оси У и т.д.). У одного датчика может быть от одного до N каналов
* ***MASTER*** - ведущее устройство, обеспечивающее взаимодействие с приложением по Bluetooth и считывание данных с датчиков, а также фильтрацию и калибровку данных
* ***MODULE*** - ведомое устройство, обеспечивающее работу с реальным физическим датчиком (датчиками) и нормирование "сырых" величин к виду данных  