## задание 1
![фото со временем работы функций](images\time_work.png) \

### Создание экземпляров:

UsualClass быстрее всего создаются
SlotsClass создается медленнее
WeakrefClass создается медленнее всех остальных классов

### Изменение атрибутов:

UsualClass работают быстрее WeakrefClass, но медленнее SlotsClass
SlotsClass изменяются быстрее всего
WeakrefClass работает медленнее всех


запускалось с помощью команды : \
```python -m cProfile -s ncalls .\08\weakref_slots.py```
## Задание 2

### Создание экземпляров:
![создание экземпляров обычного класса](images\create_slotsClass.png) \
Наименьшее потребление памяти у SlotsClass (115.0 MiB прироста) \
![создание экземпляров обычного класса](images\create_weakrefClass.png) \
Наибольшее потребление у WeakrefClass (161.0 MiB прироста)
![создание экземпляров обычного класса](images\create_usualclass.png) \
Обычный класс занимает промежуточное положение (145.6 MiB прироста)
### Изменение атрибутов:
![change экземпляров обычного класса](images\use_usualyClass.png) \
![change экземпляров обычного класса](images\use_slotsClass.png) \
![change экземпляров обычного класса](images\use_weakrefClass.png) \
SlotsClass и WeakrefClass не потребляют дополнительной памяти \
UsualClass потребляет 44.5 MiB дополнительной памяти
### Отрицательные значения Increment:

Это артефакт измерения, а не реальное уменьшение памяти
связано с оптимизацией памяти Python