import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2

DB = dict(
    host="localhost",
    port=5432,
    dbname="reklamnoe_agentstvo",
    user="postgres",
    password="1234",
)

def get_conn():
    return psycopg2.connect(**DB)

def show_rows(columns, rows):
    tree.delete(*tree.get_children())
    tree["columns"] = columns
    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=120, anchor="w")
    for r in rows:
        tree.insert("", "end", values=r)

def open_table(name):
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {name}")
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
        show_rows(cols, rows)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def query_by_date():
    d = simpledialog.askstring("Дата", "Введите дату (ГГГГ-ММ-ДД):", initialvalue="2026-09-20")
    if not d:
        return
    sql = """
        SELECT r.data_vyhoda,
               i.nazvanie       AS izdanie,
               rd.naimenovanie  AS reklamodatel,
               r.kolichestvo,
               rc.cena,
               r.kolichestvo * rc.cena AS stoimost
        FROM razmeshchenie r
        JOIN zayavka       z  ON z.id_zayavki       = r.id_zayavki
        JOIN reklamodatel  rd ON rd.id_reklamodatel = z.id_reklamodatel
        JOIN izdanie       i  ON i.id_izdanie       = r.id_izdanie
        JOIN rascenka      rc ON rc.id_izdanie      = i.id_izdanie
        WHERE r.data_vyhoda = %s
        ORDER BY i.nazvanie, rd.naimenovanie
    """
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (d,))
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
        show_rows(cols, rows)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def report_by_date():
    d = simpledialog.askstring("Дата", "Дата для отчёта (ГГГГ-ММ-ДД):", initialvalue="2026-09-20")
    if not d:
        return
    sql = """
        SELECT i.nazvanie, rd.naimenovanie, r.kolichestvo, rc.cena,
               r.kolichestvo * rc.cena AS stoimost
        FROM razmeshchenie r
        JOIN zayavka       z  ON z.id_zayavki       = r.id_zayavki
        JOIN reklamodatel  rd ON rd.id_reklamodatel = z.id_reklamodatel
        JOIN izdanie       i  ON i.id_izdanie       = r.id_izdanie
        JOIN rascenka      rc ON rc.id_izdanie      = i.id_izdanie
        WHERE r.data_vyhoda = %s
        ORDER BY i.nazvanie, rd.naimenovanie
    """
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (d,))
            rows = cur.fetchall()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
        return

    text = f"ОТЧЁТ: Размещения на {d}\n"
    text += "=" * 60 + "\n"
    text += f"{'Издание':<20}{'Рекламодатель':<20}{'Кол-во':>7}{'Цена':>10}{'Стоимость':>12}\n"
    text += "-" * 60 + "\n"
    total = 0
    for r in rows:
        text += f"{r[0]:<20}{r[1]:<20}{r[2]:>7}{r[3]:>10.2f}{r[4]:>12.2f}\n"
        total += r[4]
    text += "-" * 60 + "\n"
    text += f"{'ИТОГО:':<47}{total:>12.2f}\n"

    win = tk.Toplevel(root)
    win.title(f"Отчёт на {d}")
    txt = tk.Text(win, font=("Courier", 10), width=80, height=20)
    txt.pack(fill="both", expand=True)
    txt.insert("1.0", text)
    txt.config(state="disabled")

root = tk.Tk()
root.title("Рекламное агентство")
root.geometry("900x600")

menubar = tk.Menu(root)

m_ref = tk.Menu(menubar, tearoff=0)
m_ref.add_command(label="Рекламодатели", command=lambda: open_table("reklamodatel"))
m_ref.add_command(label="Издания",       command=lambda: open_table("izdanie"))
m_ref.add_command(label="Расценки",      command=lambda: open_table("rascenka"))
menubar.add_cascade(label="Справочники", menu=m_ref)

m_req = tk.Menu(menubar, tearoff=0)
m_req.add_command(label="Просмотр заявок", command=lambda: open_table("zayavka"))
menubar.add_cascade(label="Заявки", menu=m_req)

m_pl = tk.Menu(menubar, tearoff=0)
m_pl.add_command(label="Просмотр размещений", command=lambda: open_table("razmeshchenie"))
menubar.add_cascade(label="Размещения", menu=m_pl)

m_q = tk.Menu(menubar, tearoff=0)
m_q.add_command(label="Заявки на дату", command=query_by_date)
menubar.add_cascade(label="Запросы", menu=m_q)

m_rep = tk.Menu(menubar, tearoff=0)
m_rep.add_command(label="Размещения на дату (печать)", command=report_by_date)
menubar.add_cascade(label="Отчёты", menu=m_rep)

menubar.add_command(label="Выход", command=root.destroy)

root.config(menu=menubar)

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

tree = ttk.Treeview(frame, show="headings")
tree.pack(fill="both", expand=True, side="left")

scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scroll.pack(side="right", fill="y")
tree.configure(yscrollcommand=scroll.set)

root.mainloop()
