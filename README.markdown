# Безплатна бира

Python е свободен като словото, но и безплатен като бирата. Целта на задачата е да напишете проста функция, която брои поредни числа, но от време на време черпи и по бира.

Функцията трябва да се казва `freebeer` и да приема един аргументa на име `n`.

Функцията трябва да връща низ с числата от 1 до `n` (включително), в който числата, които се делят на 3 са заместени с думата `free`, числата, които се делят на 5 са заместени от думата `beer`, а числата, които се делят и на 3 и на 5 са заместени с `freebeer`. Отделните числа и думи трябва да са разделени със празно място, но не трябва да има излишни празни места в края на низа.

Пример:

    >>> freebeer(15) '1 2 free 4 beer free 7 8 free beer 11 free 13 14 freebeer'
**Съвет:** Ако имате проблем с излишно празно място на края на низа, прочетете `help(str)` в интерпретатора, за да намерите метод, който да го премахне.

# Пет дребни функции

Функционалното програмиране дели питонското общество на два лагера – тези които го харесват и всички останали*. Без значение къде попадате, трябва да умеете функционалния стил, ако искате да ви вземат насериозно като питонист. Тази задача ще ви помогне да развиете умения.

Имплементирайте следните пет функции:

## one

    def one(seq): ...
В Python има `all` и `any`. Но няма `one`. Дефинирайте функция `one`, която да връща истина когато в `seq` има точно един елемент, който се оценява като истина. Демек:

    one([0, 0, 0]) # False
	one([0, 4, 0]) # True
	one([False, 8, 0]) # True
	one([False, 8, 6, 0]) # False
	one(x / y for x, y in ((1, 2), (3, 4), (5, 0))) # False

Имплементирайте оценката на елементите в списъка мързеливо – ако оцените два елемента от `seq` като истина, това ви гарантира че `one` трябва да върне `False` и няма нужда да проверявате следващите елементи. Обърнете внимание, че последния пример връща `False`, а не предизвиква `ZeroDivisionError`

## inject

`inject` (наричан още `reduce`, `fold` или `accummulate`) е функция от по-висок ред, която свежда списък до единствена стойност. Типичен пример е да ползвате `inject(операция_събиране, списък_с_числа, първоначална_стойност)` за да получите сбора на числа в списък. Типичната употреба е нещо такова:

    def imaginary_inject(fun, seq, init): pass
    imaginary_inject(lambda a, b: a + b, [2, 3, 5, 7, 11, 13], 1) == 42
	imaginary_inject(lambda a, b: a * b, [1, 2, 3, 4], 1) == 24
	imaginary_inject(lambda a, b: a * b, [1, 2, 3, 4], 0) == 0 

Изчислението протича (горе-долу) така: извиква се `fun(init, seq[0])`, след което резултата се подава на `fun` като първи аргумент, а `seq[1]` отива като втори. Този резултат се предава отново на `fun` със `seq[2]` и така докато изчерпате `seq`.

Може да се каже, че:

    imaginary_inject(fun, [1, 2, 3], 0) == fun(fun(fun(0, 1), 2), 3)

Ние искаме нещо по-алтаво. `inject` трябва да приема функция и да връща нова функция, приемаща списък и първоначална стойност. `imaginary_inject(fun, [1, 2, 3], 0)` изглежда така:

    injector = inject(fun) injector([1, 2, 3], 0)  # или  inject(fun)([1, 2, 3], 0)

Допълнително, ако върната от `inject` функция получи само един списък, използва първия елемент от списъка като `init`.

Понеже няколко реда код често е по-красноречив от няколко страници текст, `inject` трябва да се държи така:

    inject(lambda x, y: x + y)([1, 2, 3, 4], 0) == 10
	inject(lambda x, y: x + y)([1, 2, 3, 4]) == 10
	inject(lambda x, y: x * y)([1, 2, 3, 4], 1) == 24
	inject(lambda x, y: x * y)([1, 2, 3, 4]) == 24
	inject(lambda x, y: x * y)([0, 1, 2, 3, 4]) == 0
	sum = inject(lambda x, y: x + y)
	sum([1, 2, 3, 4]) == 10
	product = inject(lambda x, y: x * y)
	product([1, 2, 3, 4]) == 24

## unfold

    def unfold(initial, step, condition, skip = None): pass

`unfold` е обратното на `inject` (още известен като `fold`). Той трансформира единична стойност в списък. Приема три аргумента -- първоначална стойност, функция с която да получи от една стойност следващата и предикат, който определя докога да се изчисляват нови стойности.

    unfold(1, lambda x: x + 1, lambda x: x < 5) == [1, 2, 3, 4]

В този случай, първоначалната стойност е 1, стъпката е увеличаване с едно (`lambda x: x + 1`), а елементите се произвеждат докато числата са по-малки от пет (`lambda x: x < 5`).

Ето още няколко примера:

    unfold(3, lambda x: x + 1, lambda x: x < 5) == [3, 4]
	unfold(3, lambda x: x + 1, lambda x: x < 0) == []
	unfold(1, lambda x: x + 2, lambda x: x < 10) == [1, 3, 5, 7, 9]

`skip` е опционален четвърти аргумент. Ако е подаден, елементите за които връща истина, се изпускат от списъка:

    unfold(1, lambda x: x + 1, lambda x: x < 10, lambda x: x % 2 == 0) == [1, 3, 5, 7, 9]
	unfold(1, lambda x: x + 1, lambda x: x < 10, lambda x: x > 4) == [1, 2, 3, 4]

## theta

    def theta(predicate, *sequences): pass

Theta join е любопитна концепция в SQL. В LINQ се нарича просто join. Функцията приема предикат и няколко списъка и връща подмножеството на декартовото произведение на тези списъци, за което предикатът се оценява като истина. Редът няма значение.

    theta(lambda x, y: x + 1 == y, [1, 3], [2, 4]) == [(1, 2), (3, 4)]
	theta(lambda x, y: x < y, [2, 5], [3, 6]) == [(2, 3), (2, 6), (5, 6)]
	theta(lambda x, y, z: x*x + y*y == z*z, range(1, 10), range(1, 10), range(1, 10)) == [(3, 4, 5), (4, 3, 5)]

Резултатът трябва да е списък (поредица) от n-орки. Редът им няма значение.

## memoize

    def memoize(fun): pass

Някои функции като `random()` връщат различно нещо всеки път, но други като `x + y` или `fib(n)` са "чисти" – стойността им зависи само от аргументите. Смятането на `fib(n)` може да бъде изключително бавно. Затова е удобно резултатите да се запомнят някъде (например в речник). При следващи извиквания се използват вече запомнените резултати, вместо функцията да се смята отново.

`memoize(fun)` връща друга функция – мемоизиращ вариант на `fun`, заедно с функция, която ще ни дава графиката на запомнените стойности (реда няма значение):

    f = lambda x: x * 2 h, graph = memoize(f)
	h(0) == f(0)
	h(2) == f(2)
	set(graph()) == {(0, 0), (2, 4)}
    h(10) == f(10)
	set(graph()) == {(0, 0), (2, 4), (10, 20)}

Можем да мемоизираме функции на няколко аргумента:

    f = lambda x, y: x**2 + x*y + y**2 h, graph = memoize(f)
	h(0, 0) == f(0, 0)
	h(1, 1) == f(1, 1)
	h(2, 2) == f(2, 2)
	set(graph()) == {(1, 1, 3), (0, 0, 0), (2, 2, 12)}

Графиката на функция на n аргумента се състои от n+1-орки – първите n елемента са аргумените, а последният е стойността на функцията.

**Важно:** `h` вика `f` най-много по веднъж за дадени аргументи!

# HTML

Проблем: писането на HTML не е приятно. Ще се опитаме да променим това с прост текстов формат.

## kiss

Напишете функция `kiss(text)`, която преобразува текст в долния формат до HTML.

## Параграфи и нови редове

Всеки самотен нов ред трябва да се замени с `<br />`. Всяка последователност от повече от един знак за нов ред указва нов параграф. Текстът във всеки параграф трябва да е ограден от `<p>` и `</p>`.

    Яздих, яздих, докато се наяздих. После спрях.  А след следобедната закуска светът беше прекрасен.

става на

    <p>Яздих, яздих, докато се наяздих.<br /> После спрях.</p>  <p>А след следобедната закуска светът беше прекрасен.</p>

* Не оставяйте празни параграфи.
* Махнете `<br />` от началото и края на параграфите.

## Заглавия

Ако един ред започва и завършва с един и същ брой знака за равно (?6), то той се заменя със съответното заглавие:

    == Баба ==

става на

    <h2>Баба</h2>

* Заглавията също указват край на параграф.
* Заглавията никога не се намират в параграф.

## Списъци

Няколко (>1) последователни реда започващи с `*` трябва да се оформят в списък:

    Домашни любимци: * Куче * Котка * Моторна резачка
	
става на

    <p>Домашни любимци:</p>
	<ul>
	    <li>Куче</li>
		<li>Котка</li>
		<li>Моторна резачка</li>
	</ul>

* Всеки елемент на списъка не е по-дълъг от един ред.
* Между елементите на списъка няма празни редове.
* Списъците също указват край на параграф.
* Списъците никога не се намират в параграф.
* Ако нещо прилича на списък, но не отговаря на горните условия, не го пипайте.

## Коментари

Всеки ред, започващ с `#` се игнорира не се включва в резултата.

## Адреси

Ако намерите интернет адреси ги преобразувайте до връзки:

   Здрасти, това е моят сайт: http://unhappyhipsters.com/. А пощата ми е: pop@armenia.com. Пишете ми!
   
става на

    Здрасти, това е моят сайт: <a href="http://unhappyhipsters.com/">http://unhappyhipsters.com/</a>. А пощата ми е: <a href="mailto: pop@armenia.com">pop@armenia.com</a>. Пишете ми!

* В адресите няма празни места.
* Адресите никога не завършват на препинателен знак (точка, запетая, въпросителен или удивителен знак). Ако един иначе валиден адрес завършва на препинателен знак, не включвайте препинателния знак във връзката, но не го премахвайте от текста.
* `pipo.morkova@example.org`, `bullet_40_proof@example.org` и `mityo+the+python@people.example.org` са все валидни адреси. `mityo@python` не е.
* Домейните са само на латиница и могат да включват само буквите от английската азбука, цифри, точка и тире.
* Пътят може да съдържа само буквите от английската азбука, цифри, права наклонена черта, точка, долна черта, тире, въпросителен знак, амперсанд или #
* Непощенските адреси започват с `http://`
* Потребителското име на e-mail адрес може да включва само буквите от английската азбука, цифри, точка, долна черта или плюс.

## Специален текст

    [iamsocool]Примигвам, примигвам! Ослепявам, ослепявам![/iamsocool]

става на

    <span class="iamsocool">Примигвам, примигвам! Ослепявам, ослепявам!</span>
	
	Казаха ми, че [weak]съм силен[/weak] и, че гълъбите не ядат сникърси.
	
	А после не бяха прави.

става на

    <p>Казаха ми, че <span class="weak">съм силен</span> и, че гълъбите не ядат сникърси.</p>
	<p>А после не бяха прави.</p>
	
* Името на класа винаги е с малки букви от английската азбука.
* Ако в текста има отварящ `[xxx]`, то има и затварящ. И обратно.
* В специалния текст никъде няма повече от един последоватален знак за нов ред.
* Специалният текст не променя по никакъв начин правилата за параграфи и нови редове. Той не е параграф сам по себе си и ако е самичък в параграф трябва да бъде ограден от `<p>`.

## Още важни неща

* Не ни интересува празното място. Няма разлика къде и по колко слагате от него.
* Не се притеснявайте за бързодействието на вашата програма. Опитайте да я напишете така, че да се чете и разбира лесно от хора.
* Регулярните изрази са необходимост, но не са панацея.

# Geometry Classes

Да се имплементира модул за работа с обекти в разширеното двумерно евклидово пространство.

Модулът трябва да предостави следните класове: `Point`, `Vector`, `Line`, `GeometricError`

## Вектор

Класът `Vector` предоставя следната функционалност:

* Конструктор: `Vector(x, y)`
* Оператори `==` и `!=` за сравняване на вектори. (2 вектора са равни ако посоките и дължините им съвпадат)
* Възможност за ползване на функциите repr и str, като за всеки вектор `vect` е изпълнено: `eval(repr(vect)) == vect`
* Бинарни оператори `+ - *`, като те са съответно: векторен сбор; векторна разлика и скаларно произведение на вектори.
* Бинарен оператор `*?`, умножаващ вектор по число (забележка: векторите могат да се умножават скаларно и по други вектори)
* Бинарен оператор `/?`, делящ вектор на число.
* Унарни оператори `+ -`, като те са съответно: идентитет на вектора; противоположен вектор
* Метод `vect.length()`, връщащ дължината на вектора `vect`.
* Метод `vect.scaled(number)`, връщащ *нов* вектор, който отговаря на вектора `vect` умножен с числото `number`.
* Метод `vect.normalized()`, връщащ *нов* вектор, отговарящ на нормализиран `vect` (т.е. има същата посока като `vect` и дължина 1)
* Метод `vect.normal()`, връщащ *нов* вектор, със същата дължина като `vect`, и посока перпендикулярна на `vect` (забележка: в 2-мерно пространство тези вектори са два. Няма значение кой от тях ще върнете)
* Методи `vect.iscollinear(vect2)` и `vect.isnormal(vect2)`, които връщат `True`, ако векторите са съответно колинеарни или перпендикулярни и `False` - в противен случай.
* Метод `vect.isnormalized()` връщащ `True`, ако дължината на вектора е 1.
* Metod `vect.iszero()`, връщащ `True`, ако дължината на вектора е 0 (нулев вектор).

## Точка

Класът `Point` описва точка от разширената евклидова равнина.

Уточнения: В разширената евклидова равнина точките представляват тройки `(x, y, z)` Ако z=0, наричаме точката безкрайна. Ако z?0, то тази точка съвпада с точката в (не-разширено) евклидово пространство с координати `(x', y')`, като е изпълнено: `x', y' = x/z, y/z`

Класът предоставя следната функционалност:

* Конструктор: `Point(x, y, z=1)`.
* Оператори `==` и `!=` за сравняване на точки. (забележка: точките `(x, y, z)` и `(c*x, c*y, c*z)` съвпадат, за всяка реална константа `c?`)
* Възможност за ползване на функциите `repr` и `str`, като за всяка точка `p?` е изпълнено: `eval(repr(p)) == 	p`
* Метод `p.isinfinite()`, връщащ `True`, ако точката е безкрайна.
* Метод `p.distance(other)`, връщащ разстояние между две точки, ако `other` е точка и разстояние между точка и права, ако `other` е права.

## Права

Класът `Line` описва права. Интересно е, че тя може да се представи (еднозначно) по няколко начина.

* Уравнение на права: `ax + by + cz = 0`
* Начална точка и вектор: `{p + k*v}`, където `k?` - произволно реално число, `p?` - точка, `v?` - вектор.
* Две точки p1, p2 (p1 ? p2)

Изборът кой начин да ползвате е изцяло ваш.

Уточнения: Правата, минаваща през кои да е две безкрайни точки е безкрайната права. Тя е единствена и съдържа всички безкрайни точки. Права, съдържаща крайна точка и безкрайна точка е валидна и не-безкрайна права.

Класът предоставя следната функционалност:

* Конструкор `Line(a, b)`, приемащ 2 точки *или* вектор и точка.
* Оператори `==` и `!=` за сравняване на прави. (забележка: ако правите съдържат едни и същи точки, то те са равни)
* Оператор `v in l`, който за точка `v?` и права `l?` връща `True`, само ако точката лежи на правата.
* Оператор `*?`, връщащ пресечната точка на две прави. (забележка: успоредни прави се пресичат в безкрайна точка; безкрайната права и не-безкрайна - също)
* Възможност за ползване на функциите `repr` и `str`, като за всяка права `l?` е изпълнено: `eval(repr(l)) == 	l`
* Метод `l.isinfinite()`, връщащ `True`, ако правата съвпада с безкрайната права
* Метод `l.distance(p)`, връщащ разстоянието от правата до точката `p?`
* Метод `l.isparallel(other)`, връщащ `True`, ако правите `l?` и `other` са успоредни (забележка: всяка права е успоредна със себе си)
* Методи `l.colinear_vector()` и `l.normal_vector()`, връщащи съответно колинеарен и нормален (перпендикулярен) вектор на правата. (забележка: дължината и направлението на върнатите вектори са без значение)

## Геометрична грешка

Класът `GeometricError` ще ползваме, както за всевъзможните невалидни извиквания, така и за недефинирано поведение на нашите методи. Той (естествено) трябва да бъде наследник на Exception. Ако сте сигурни, че нещо е невалидно или недефинирано - вдигайте това изключение.

В следните ситуации ползването му е задължително:

* Пресичане на права със себе си
* Строене на права по две съвпадащи точки
* Строене на права по точка и нулев вектор
* Нормализиране на нулев вектор

# Unit testing & metaprogramming

Ще си поиграем с unit тестове, декоратори и метакласове.

## unit_converter

Напишете динамичен декоратор `unit_converter(a, b)`, който да приема функция, която връща числов резултат, и обръща резултата й от една мерна единица към друга - например от инчове към сантиметри.

`unit_converter(a, b)` трябва да конвертира резултата `x` на функцията по формулата `ax + b`.

Пример:

    @unit_converter(1.8, 32)
    def celsius_function():
        return 18.0; # градуси по целзий

	>>> print(celsius_function()) # връща градуси по фаренхайт
	64.4 # 1.8 * 18.0 + 32 = 64.4` 

Като всеки добър декоратор, и този трябва позволява декорираната функцията да има произволен брой и вид аргументи.

## Unit test

Ваш колега е написал функция `is_prime(x)`, която връща `True` ако `x` е просто число.

Не сте сигурни дали функцията работи както трябва, за това трябва да напишете unit тест клас, наречен IsPrimeTest, който да тества функцията.

Вашият клас трябва да има следните тестове:

* `testBasic()`, който проверява поведението на `is_prime()` при 1, 2, 4, 6 и 7
* `testNegative()`, за поведението на `is_prime()` при отрицателни числа (`is_prime()` би трябвало да върне `False`)
* `testNonNumber()`, за поведението на `is_prime()` при не-числа (`is_prime()` ще хвърли exception)
* `testRandom()`, за поведението на is_prime() при 10,000 случайно генерирани числа, които да сравнявате с ваша имплементация на функцията с друго име

Трябва да спазвате протокола за unit тестове на Python, включително да наследявате правилния клас.

Функцията `is_prime()`, която трябва да тествате, се намира в примерния тест. За да я използвате напишете

    from p10sample import is_prime

## Метакласове

Напишете метаклас `NegativeMeta`, който за всеки метод `<b>x</b>` от оригиналния клас да създава метод `not_<b>x</b>`, който да приема същите аргументи, но да връща отрицателния булеви резултат (с `not`).

Пример:

    class Comparer(metaclass = NegativeMeta):
        def __init__(self, a):
            self.a = a
        
        def is_bigger_than(self, b):
            return self.a > b
    
    >>> twenty = Comparer(20)
    >>> print('not_is_bigger_than' in dir(twenty)) #True
    >>> print(twenty.is_bigger_than(40)) #False
    >>> print(twenty.not_is_bigger_than(40)) #True

Няма нужда да проверявате дали вече има метод с име `not_<b>x</b>`. Методите, започващи с __ също можете да оставите на мира.

## Метакласове 2

Напишете втора версия на `NegativeMeta`, наречена `NegativeMetaDynamic`, която се държи по същия начин, но изпълнява методите `not_<b>x</b>` динамично, вместо да ги създава при дефинирането на класа.

Пример:

    class Comparer2(metaclass = NegativeMetaDynamic):
        def __init__(self, a):
            self.a = a
        
        def is_bigger_than(self, b):
            return self.a > b
    
    >>> twenty = Comparer2(20)
    >>> print('not_is_bigger_than' in dir(twenty)) # !!! False
    >>> print(twenty.is_bigger_than(40)) # False
    >>> print(twenty.not_is_bigger_than(40)) # True
