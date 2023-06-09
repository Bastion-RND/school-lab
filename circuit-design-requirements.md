# Настоящий документ предназначен для внешних разработчиков и содержит требования к схемотехнике мультисенсора
***
## [Соглашение о терминах](/terms-convention.md)
***
Блок MASTER построен на основе модуля ESP32-WROVER-E (со встроенной PCB антенной) от Espressif. Назначение этого блока - опрос сенсоров в блоке SENSORS и передача данных в приложение через Bluetooth. Референс схемотехники данного блока определён в настоящем документе.  
Блок SENSORS реализуется внешним разработчиком. Назначение этого блока - опрос реальных физических датчиков и передача данных об измерениях MASTER-у.  
В качестве интерфейса для связи блоков применён UART (конкретно, с точки зрения периферии ESP32, это UART1). Скорость UART-а - 115200. В следующей таблице показано набор пинов для подключения:

|Пин MASTER-а                     |Назначение                                 |Пин SENSORS-а     |                                    
|:--------------------------------|:------------------------------------------|:-----------------|
|IO23(out) - TX                   |Передача данных от MASTER к SENSORS        |?(in) - RX        |
|IO22(in) - RX                    |Передача данных от SENSORS к MASTER        |?(out) - TX       |
|IO21(pull-down, out) - BREAKFLOW |MASTER управляет потоком данных от SENSORS |?(in) - BREAKFLOW |
|IO18(pull-up, out) - RESET       |MASTER сбрасывает SENSORS                  |?(in) - RESET     |  

Активный логический уровень на TX, RX, RESET - логический ноль, на BREAKFLOW - логическая единица. BREAKFLOW притянут к минусу питания ESP32, RESET притянут к плюсу питания ESP32 (3V3).  
Кроме того, на стороне MASTER необходимо реализовать два делителя (для измерения напряжения АКБ и для контроля за напряжением USB) и светодиод для индикации статуса подключения к приложению.
***
## Возможны следующие варианты реализации MASTER-а
### Вариант 1
Использование ESP32-WROVER-E в "чистом" виде, распаяв его на плате разрабатываемого мультисенсора
<p align="center">
  <img src="/related-documents/pictures/esp32-wrover-e-view.png">
</p>
Следует помнить, что для прошивки данного модуля потребуется разместить программатор непосредственно на плате мультисенсора. Схема:
<p align="center">
  <img src="/related-documents/schematics/master-on-base-esp32-wrover-e-single-module.png">
</p>  

### Вариант 2
Использование отладочной платы LOLIN D32 PRO
<p align="center">
  <img src="/related-documents/pictures/lolin-d32-pro-view.png">
</p>
В данном варианте программатор уже размещён на плате модуля. Схемотехника в данном случае выглядит так:
<p align="center">
  <img src="/related-documents/schematics/master-on-base-lolin-d32-pro.png">
</p>

***
От внешнего разработчика требуется:
* предоставить четыре пина интерфейса;
* обеспечить гальваническую связь минусов питания MASTER и SENSORS;
* обеспечить MASTER питанием 3,3VDC ([вариант 1](#вариант-1)) или 5VDC ([вариант 2](#вариант-2)). Ток - не менее 0,5А;
* в случае разных логических уровней интерфейса на стороне MASTER и SENSORS - обеспечить их согласование. 
