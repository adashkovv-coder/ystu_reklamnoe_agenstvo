-- 1.1. Вывести все доступные издания (газеты, журналы, интернет-СМИ)
SELECT id_izdanie, nazvanie, tip_izdaniya, izdatelstvo 
FROM izdanie;

-- 1.2. Вывести рекламодателей, зарегистрированных в системе
SELECT id_reklamodatel, naimenovanie, telefon 
FROM reklamodatel;

-- 1.3. Вывести заявки, поданные в сентябре 2026 года
SELECT id_zayavki, soderzhanie, data_zayavki 
FROM zayavka 
WHERE data_zayavki >= '2026-09-01' AND data_zayavki <= '2026-09-30';

-- 2.1.1. Вывести название издания и его цену за размещение
SELECT i.nazvanie, r.cena
FROM izdanie i, rascenka r
WHERE i.id_izdanie = r.id_izdanie;

-- 2.1.2. Вывести имя рекламодателя и текст его заявки
SELECT reklamodatel.naimenovanie, zayavka.soderzhanie
FROM reklamodatel, zayavka
WHERE reklamodatel.id_reklamodatel = zayavka.id_reklamodatel;

-- 2.2.1. Вывести информацию о заявках вместе с названиями рекламодателей
SELECT r.naimenovanie AS Рекламодатель, z.soderzhanie AS Заявка, z.data_zayavki AS Дата_заявки
FROM zayavka z
INNER JOIN reklamodatel r ON z.id_reklamodatel = r.id_reklamodatel;

-- 2.3.1. Соединение трех таблиц: вывести где (издание) и когда выходила реклама по конкретной заявке
SELECT i.nazvanie AS Издание, z.soderzhanie AS Текст_заявки, rm.data_vyhoda AS Дата_выхода
FROM razmeshchenie rm
INNER JOIN izdanie i ON rm.id_izdanie = i.id_izdanie
INNER JOIN zayavka z ON rm.id_zayavki = z.id_zayavki;

-- 2.4.1. LEFT JOIN: Выведет ВСЕХ рекламодателей, даже если у них еще нет ни одной заявки
SELECT r.naimenovanie, z.soderzhanie
FROM reklamodatel r
LEFT JOIN zayavka z ON r.id_reklamodatel = z.id_reklamodatel;

-- 2.4.2. RIGHT JOIN: Выведет ВСЕ заявки, даже если рекламодатель по какой-то причине отсутствует
SELECT r.naimenovanie, z.soderzhanie
FROM reklamodatel r
RIGHT JOIN zayavka z ON r.id_reklamodatel = z.id_reklamodatel;

-- 2.4.3. FULL JOIN: Выведет все записи из обеих таблиц
SELECT r.naimenovanie, z.soderzhanie
FROM reklamodatel r
FULL JOIN zayavka z ON r.id_reklamodatel = z.id_reklamodatel;

-- 2.5.1. Вывести заявки, отсортированные по дате подачи (от старых к новым)
SELECT id_zayavki, soderzhanie, data_zayavki
FROM zayavka
ORDER BY data_zayavki ASC;

-- 2.6.1. Таблица razmeshchenie является дочерней по отношению к zayavka и izdanie.
SELECT id_razmeshcheniya, id_zayavki, id_izdanie, data_vyhoda
FROM razmeshchenie
WHERE id_zayavki = 1;

-- 2.7.1. BETWEEN: Выбрать размещения, которые вышли в период с 20 по 25 сентября 2026
SELECT id_razmeshcheniya, data_vyhoda
FROM razmeshchenie
WHERE data_vyhoda BETWEEN '2026-09-20' AND '2026-09-25';

-- 2.7.2. IN: Выбрать рекламодателей с конкретными ID (например, первый и третий)
SELECT id_reklamodatel, naimenovanie
FROM reklamodatel
WHERE id_reklamodatel IN (1, 3);

-- 2.7.3. LIKE: Выбрать издания, в названии которых есть слово "Вечерний"
SELECT nazvanie
FROM izdanie
WHERE nazvanie LIKE '%Вечерний%';
