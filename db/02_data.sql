INSERT INTO reklamodatel (id_reklamodatel, naimenovanie, telefon) VALUES
(1, 'ООО Ромашка',  '+7-900-111-11-11'),
(2, 'ИП Иванов',    '+7-900-222-22-22'),
(3, 'ООО Вектор',   '+7-900-333-33-33');

INSERT INTO izdanie (id_izdanie, nazvanie, tip_izdaniya, izdatelstvo) VALUES
(1, 'Вечерний город', 'газета',   'Городская типография'),
(2, 'Мир рекламы',    'журнал',   'Издательский дом Мир'),
(3, 'Новости24',      'интернет', 'ООО Новости24');

INSERT INTO rascenka (id_rascenki, id_izdanie, cena) VALUES
(1, 1, 5000.00),
(2, 2, 12000.00),
(3, 3, 3000.00);

INSERT INTO zayavka (id_zayavki, id_reklamodatel, soderzhanie, data_zayavki) VALUES
(1, 1, 'Реклама кофейни',      '2026-09-01'),
(2, 2, 'Реклама автосервиса',  '2026-09-05'),
(3, 1, 'Реклама нового меню',  '2026-09-10');

INSERT INTO razmeshchenie (id_razmeshcheniya, id_zayavki, id_izdanie, data_vyhoda, kolichestvo) VALUES
(1, 1, 1, '2026-09-20', 1),
(2, 1, 2, '2026-09-25', 1),
(3, 2, 3, '2026-09-20', 5),
(4, 3, 1, '2026-09-30', 2),
(5, 3, 2, '2026-09-20', 1);
