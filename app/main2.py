import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2

DB = dict(host="localhost", port=5432, dbname="reklamnoe_agentstvo",
          user="postgres", password="1234")

SQL_DATE = """
SELECT r.data_vyhoda, i.nazvanie, rd.naimenovanie, r.kolichestvo,
       rc.cena, r.kolichestvo * rc.cena AS stoimost
FROM razmeshchenie r
JOIN zayavka       z  ON z.id_zayavki       = r.id_zayavki
JOIN reklamodatel  rd ON rd.id_reklamodatel = z.id_reklamodatel
JOIN izdanie       i  ON i.id_izdanie       = r.id_izdanie
JOIN rascenka      rc ON rc.id_izdanie      = i.id_izdanie
WHERE r.data_vyhoda = %s
ORDER BY i.nazvanie, rd.naimenovanie
"""

def sql(q, p=None):
    """SQL-запрос. Ошибки показывает сам, возвращает ([], []) при сбое."""
    try:
        with psycopg2.connect(**DB) as c, c.cursor() as cur:
            cur.execute(q, p or ())
            return [d[0] for d in cur.description] if cur.description else [], cur.fetchall()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
        return [], []

def show(cols, rows):
    t.delete(*t.get_children())
    t["columns"] = cols
    for c in cols:
        t.heading(c, text=c); t.column(c, width=120, anchor="w")
    for r in rows:
        t.insert("", "end", values=r)

def tbl(name):
    show(*sql(f"SELECT * FROM {name}"))

def ask(p="Дата (ГГГГ-ММ-ДД):"):
    return (simpledialog.askstring("Дата", p, initialvalue="2026-09-20") or "").strip()

def q_date():
    d = ask()
    if d: show(*sql(SQL_DATE, (d,)))

def rep_date():
    d = ask("Дата для отчёта:")
    if not d: return
    _, rows = sql(SQL_DATE, (d,))
    if not rows: return
    total = sum(r[5] for r in rows)
    txt = (f"ОТЧЁТ: Размещения на {d}\n" + "="*60 + "\n"
           + f"{'Издание':<20}{'Рекламодатель':<20}{'Кол-во':>7}{'Цена':>10}{'Стоимость':>12}\n"
           + "-"*60 + "\n"
           + "".join(f"{r[1]:<20}{r[2]:<20}{r[3]:>7}{r[4]:>10.2f}{r[5]:>12.2f}\n" for r in rows)
           + "-"*60 + "\n" + f"{'ИТОГО:':<47}{total:>12.2f}\n")
    w = tk.Toplevel(root); w.title(f"Отчёт на {d}")
    box = tk.Text(w, font=("Courier", 10), width=80, height=20)
    box.pack(fill="both", expand=True)
    box.insert("1.0", txt); box.config(state="disabled")

MENU = {
    "Справочники": [("Рекламодатели", lambda: tbl("reklamodatel")),
                    ("Издания",       lambda: tbl("izdanie")),
                    ("Расценки",      lambda: tbl("rascenka"))],
    "Заявки":      [("Просмотр заявок", lambda: tbl("zayavka"))],
    "Размещения":  [("Просмотр размещений", lambda: tbl("razmeshchenie"))],
    "Запросы":     [("Заявки на дату", q_date)],
    "Отчёты":      [("Размещения на дату (печать)", rep_date)],
}

root = tk.Tk(); root.title("Рекламное агентство"); root.geometry("900x600")

mb = tk.Menu(root)
for name, items in MENU.items():
    m = tk.Menu(mb, tearoff=0)
    for lbl, fn in items: m.add_command(label=lbl, command=fn)
    mb.add_cascade(label=name, menu=m)
mb.add_command(label="Выход", command=root.destroy)
root.config(menu=mb)

f = tk.Frame(root); f.pack(fill="both", expand=True)
t = ttk.Treeview(f, show="headings"); t.pack(fill="both", expand=True, side="left")
s = ttk.Scrollbar(f, orient="vertical", command=t.yview)
s.pack(side="right", fill="y"); t.configure(yscrollcommand=s.set)

root.mainloop()
