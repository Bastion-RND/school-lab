# Настоящий документ предназначен для внешних разработчиков и содержит описание протокола связи между блоком MASTER и блоком SENSORS
***
## [Соглашение о терминах](/terms-convention.md)
***
## Содержание
1. [Соглашение о параметрах](#соглашение-о-параметрах)
2. [Про датчики с точки зрение блока SENSORS](#про-датчики-с-точки-зрения-блока-sensors)
3. [Протокол команд/ответов](#протокол-командответов)
4. [Протокол данных](#протокол-данных)
5. [О режиме непрерывного опроса](#о-режиме-непрерывного-опроса)
6. [О управлении потоком BREAKFLOW](#о-управлении-потоком-breakflow)
7. [О сигнале RESET](#о-сигнале-reset)
8. [Типичный порядок работы](#типичный-порядок-работы)
***
## Соглашение о параметрах
* Допустимые типы параметров - строка, целочисленное число, число с плавающей точкой
* Числовые параметры с плавающей точкой используют в качестве разделителя между целочисленной и дробной частями точку. Пример: ***3.14***
* Строковые параметры должны быть заключены в двойные кавычки. Пример: ***"string"***
* В описании форматов сообщений символы ***{}<>[]*** НЕ являются отображаемыми ASCII-символами, это просто границы placeholder-а, если явно не указано иное. Пример: ***{COMAND}{SUFFIX}\<PARAM\>[PARAMS]***
* ***{placeholder}*** - служебная часть сообщения, команда, суффикс и т.д. Пример: ***AT{COMMAND}***
* ***\<sensor_param\>*** - одиночный параметр, НЕ содержащий запятые. Пример: ***5***. Пример: ***3.14***. Пример: ***"text"***
* ***\[sensor_params\]*** - список из одного и более параметров, в случае двух и более - разделённых запятой. Пример: ***5,3.14,"text"***  

[К содержанию](#содержание)
***
## Про датчики с точки зрения блока SENSORS
Все датчики с точки зрения блока SENSORS должны быть представлены в виде ассоциированных пар ***\<index\>,\<uuid\>*** для однозначной идентификации датчика по индексу. Индекс предствляет собой целочисленное значение от 0 и выше. Этот словарь вычитывается блоком MASTER в начале работы и все дальнейшие обращения к датчикам происходят по индексу для уменьшения количества траффика через интерфейс.  
[К содержанию](#содержание)
***
## Протокол команд/ответов
Блок MASTER отправляет в сторону блока SENSORS команды и получает ответы в формате протокола АТ. Протокол AT предполагает связь "точка-точка", одно устройство формирует запросы (ведущий, в нашем случае это блок MASTER), второе устройство отвечает (ведомый, в нашем случае это блок SENSORS). Рассмотрим более подробно синтаксис АТ-команд  
### Команды  
АТ-команда представляет собой строку ASCII-символов в формате  
> AT\{COMMAND\}\{SUFFIX\}\[PARAMS\]\r\n  

В начале всегда идёт префикс ***AT***, затем команда, далее - суффикс, определяющий тип команды, после - параметры, в самом конце - завершающая последовательность ***\r\n***.  

**ВНИМАНИЕ!** - далее, для упрощения, завершающая последовательность ***\r\n*** в описаниях не показывается (кроме примеров). Но она есть)  

В широком смысле, AT-команды можно разделить на два формата: ***Basic Commands*** и ***Extended Commands***.
* ***Basic Commands*** - эти команды не начинаются с ***+***. Пример: ***CFG***. 
* ***Extended commands*** - эти команды начинаются с ***+***. Пример: ***+CFG***.
В настоящем протоколе все команды в формате Extended для упрощения парсинга.  

Кроме того, все АТ-команды делятся на 4 типа. Тип определяется суффиксом, согласно следующей таблице:  
|Type      |Suffix | Назначение                               |
|----------|:-----:|------------------------------------------|
|Test      |=?     |Проверка поддержки ведомым данной команды |
|Read      |?      |Получение от ведомого параметров          |
|Write     |=      |Установка на ведомом параметров           |
|Execution |       |Запуск определённого действия             |
  
* ***Test Commands*** - эти команды позволяют узнать, поддерживает ли ведомый данную команду или нет. Синтаксис: ***AT\<COMMAND\>=?***. Пример: ***AT+CFG=?***
* ***Read Commands*** - эти команды служат для получения параметров от ведомого. Синтаксис: ***AT\<COMMAND\>?***. Пример: ***AT+CFG?***
* ***Write Commands*** - эти команды служат для установки параметров ведомого. Синтаксис: ***AT\<COMMAND\>=\<par1\>,\<par2\>,...,\<parN\>***. Пример: ***AT+CFG=1,"ON",9***
* ***Execution Commands*** - эти команды запускают на ведомом определённые действия. Синтаксис: ***AT\<COMMAND\>***. Пример: ***AT+CFG***  
Особняком стоит специализированная пустая команда, состоящая только из префикса ***AT***. Формально - это пустая команда с типом EXECUTION. Это команда для проверки связи с ведомым.

### Ответы
Ответ на команду также представляет собой строку ASCII-символов возвращаемых параметров в формате
> \{COMMAND\}:\[PARAMS\]\r\n  
> OK\r\n  

Если ответ не предполагает возврата каких-либо параметров, то сразу возвращается статус ***OK\r\n***. Если возврат параметров невозможен (был получен некорректный запрос от ведущего) или сама команда ошибочна, то сразу возвращается статус ***ERROR\r\n***  
  
**ВНИМАНИЕ!** - далее, для упрощения, завершающая последовательность ***\r\n*** в описаниях не показывается (кроме примеров). Но она есть)  
  
Ниже приведён список команд настоящего протокола:
|№ |Prefix&Command               |Supported types   |Description                                      |
|--|:---------------------:|------------------|:-----------------------------------------------:|
|1 |[AT](#at)              |Execution         |Проверка связи                                   |
|2 |[AT+STATUS](#atstatus) |Test, Read        |Проверка готовности ведомого к работе           |
|3 |[AT+LIST](#atlist)     |Test, Read        |Чтение пар \<index\>,\<UUID\> доступных датчиков |
|4 |[AT+CFG](#atcfg)       |Test, Read, Write |Чтение/установка параметров датчиков             |
|5 |[AT+DATA](#atdata)     |Test, Write       |Одиночное чтение датчика                         |

Параметры датчика передаются в виде списка \[sensor_params\]. Этот список устроен следующим образом
> \<index\>,\<data_format\>,\<range_index\>,\<polling_period_ms\>
* \<index\> - индекс датчика в целочисленном формате. Пример: ***7***
* <data_format> - формат данных для выходных данных датчика. Доступные на данный момент варианты:
    * "PLOTTER" - выходные данные в формате плоттера. О форматах данных написано [ниже](#протокол-данных).
* <range_index> - индекс выбранного диапазона изменений в целочисленном формате согласно спецификации. Пример - ***0***
* <polling_period_ms> - период отправки значений датчика в [непрерывном](#о-режиме-непрерывного-опроса) режиме. Формат - целочисленный, в миллисекундах. Пример - ***500***  
  
Рассмотрим подробнее команды протокола (в примерах символ **\>** означает направление передачи от ведущего, символ **\<** - направление передачи от ведомого):
***
#### ***AT***
Запрос наличия и работоспособности ведомого - классическая пустая АТ-команда ***АТ***. Ведомый должен вернуть ***OK***
> **пример:**  
> \> AT\r\n  
> \< OK\r\n
***
#### ***AT+STATUS***
Проверка состояния готовности ведомого.  
* в варианте Test (***AT+STATUS=?***) Ведомый должен вернуть ***OK***
    > **пример:**  
    > \> AT+STATUS=?\r\n  
    > \< OK\r\n
* в варианте Read (***AT+STATUS?***) Ведомый должен вернуть состояние своей готовности
    > **пример - ведомый не готов:**  
    > \> AT+STATUS?\r\n  
    > \< +STATUS:"BUSY"\r\n  
    > \< OK\r\n  
    > 
    > **пример - ведомый готов:**  
    > \> AT+STATUS?\r\n  
    > \< +STATUS:"READY"\r\n  
    > \< OK\r\n
***
#### ***AT+LIST***
Получение от ведомого ассоциированного списка датчиков \<index\>,\<uuid\>
* в варианте Test (***AT+LIST=?***) ведомый должен вернуть ***OK***
    > **пример:**  
    > \> AT+LIST=?\r\n  
    > \< OK\r\n
* в варианте Read (***AT+LIST?***) ведомый должен последовательно вернуть ассоциированные пары в виде \<index\>,\<uuid\>
    > **пример:**  
    > \> AT+LIST?\r\n  
    > \< +LIST:0,"123e4567-e89b-12d3-a456-426655440000"\r\n  
    > \< +LIST:1,"123e4567-e89b-12d3-a456-426655440010"\r\n  
    > \< OK  
***
#### ***AT+CFG***
Работа с параметрами датчиков.
* в варианте Test (***AT+CFG=?***) ведомый должен вернуть ***OK***
    > **пример:**  
    > \> AT+CFG=?\r\n  
    > \< OK\r\n
* в варианте Read (***AT+CFG?***) ведомый должен последовательно вернуть параметры всех датчиков (о \[sensor_params\] сказано [выше](#соглашение-о-параметрах))  
    > **пример:**  
    > \> AT+CFG?\r\n  
    > \< +CFG:0,"PLOTTER",0,0\r\n  
    > \< +CFG:1,"PLOTTER",5,0\r\n  
    > \< OK\r\n
* в варианте Write с одним параметром (***AT+CFG=\<index\>***) ведомый должен вернуть параметры сенсора по запрошенному индексу
    > **пример - запрошенный индекс существует:**  
    > \> AT+CFG=0\r\n  
    > \< +CFG:0,"PLOTTER",0,0\r\n   
    > \< OK\r\n  
    > 
    > **пример - запрошенный индекс не существует:**  
    > \> AT+CFG=2F\r\n  
    > \< ERROR\r\n
* в варианте Write с полным набором параметров (***AT+CFG=\[sensor_params\]***) ведомый должен присвоить сенсору новые параметры по запрошенному индексу
    > **пример - запрошенный индекс существует и параметры адекватны:**  
    > \> AT+CFG=0,"PLOTTER,0,0\r\n  
    > ...присвоение новых значений...  
    > \< OK\r\n  
    > 
    > **пример - запрошенный индекс не существует и/или параметры неадекватны:**  
    > \> AT+CFG=0,"PLOTTER,0,0\r\n  
    > \< ERROR\r\n
***
#### ***AT+DATA***
Однократное чтение датчика.
* в варианте Test (***AT+DATA=?***) ведомый должен вернуть ***OK***
    > **пример:**  
    > \> AT+DATA=?\r\n  
    > \< OK\r\n
* в варианте Write с одним параметром (***AT+DATA=\<index\>***) ведомый должен вернуть:
    > **пример - запрошенный индекс существует, однократно возвращаются [данные](#протокол-данных) по каналам измерения датчика (формат PLOTTER):**  
    > \> AT+DATA=0\r\n       
    > \< $0,1.4323,6.6534,3.8756\r\n  
    > \< OK\r\n  
    > 
    > **пример - запрошенный индекс не существует:**  
    > \> AT+DATA=2F\r\n  
    > \<- ERROR\r\n  
          
[К содержанию](#содержание)
***
## Протокол данных
На данный момент поддерживаются следующие протоколы кодирования возвращаемых данных:
* "PLOTTER" - данный формат передаёт значения с плавающей точкой в виде ASCII-символов. Сообщение выглядит следующим образом
> ***$\<index\>,\<value1\>,\<value2\>,...,\<valueN\>\r\n***  

где \<index\> - это индекс датчика, \<valueX\> - это данные канала датчика. Данные каналов передаются в порядке, соответствующем их субиндексу, определённому в спецификации. Пример для многоканального датчика: ***$2,5.85,10.0\r\n*** - это датчик с индексом 2, данные нулевого канала - 5.85, данные первого канала - 10.0. Пример для одноканального датчика: ***$2,5.85\r\n*** - это датчик с индексом 2, данные канала - 5.85.  
[К содержанию](#содержание)
***
## О режиме непрерывного опроса
Датчик, который в параметрах конфигурации получил значение ***\<polling_period_ms\>***, должен начать передачу своих [данных](#протокол-данных) с периодом, соответствующим полученной уставке. Отменить этот режим можно передав значение ***\<polling_period_ms\>*** равное 0 или сбросив блок SENSORS. Исходное состояние каждомо датчика - ***\<polling_period_ms\>=0***   
[К содержанию](#содержание)
***
## О управлении потоком BREAKFLOW
Настоящий протокол предполагает управление потоком со стороны блока MASTER. Это необходимо для того, чтобы можно было прервать передачу данных от блока SENSORS в режиме непрерывного опроса датчика. Таким образом, на стороне блока MASTER есть выход BREAKFLOW_OUT, на стороне блока SENSORS есть вход BREAKFLOW_IN. Пока на BREAKFLOW сохраняется низкий уровень, блок SENSORS работает в обычном режиме. Когда блок MASTER подаёт импульс высокого уровня, то по его **фронту** блок SENSORS прекращает непрерывную передачу данных и устанавливает на всех своих сенсорах polling_period_ms=0.
**ВАЖНО** - получив сигнал на прерывание передачи, блок SENSORS должен очистить свой выходной буфер с предыдущими данными, чтобы его дальнейшие ответы не слились с данными  
[К содержанию](#содержание)
***
## О сигнале RESET
Данный сигнал формирует блок MASTER, активный уровень - логический ноль. Получив данный сигнал, блок SENSORS должен произвести свой сброс и повторную инициализацию.  
[К содержанию](#содержание)
***
## Типичный порядок работы:
<p align="center">
  <img src="/related-documents/diagrams/protocol-flow.png">
</p>  
  
[К содержанию](#содержание)
