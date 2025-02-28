import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор расходов")
        self.root.geometry("400x400")
        self.root.configure(bg="#f0f0f0")

        # Заголовок
        title_label = tk.Label(root, text="Калькулятор расходов", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        # Сумма
        self.amount_label = tk.Label(root, text="Сумма:", bg="#f0f0f0")
        self.amount_label.pack(pady=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack(pady=5)

        # Категория
        self.category_label = tk.Label(root, text="Категория:", bg="#f0f0f0")
        self.category_label.pack(pady=5)
        self.category_entry = tk.Entry(root)
        self.category_entry.pack(pady=5)

        # Описание
        self.description_label = tk.Label(root, text="Описание:", bg="#f0f0f0")
        self.description_label.pack(pady=5)
        self.description_entry = tk.Entry(root)
        self.description_entry.pack(pady=5)

        # Дата
        self.date_label = tk.Label(root, text="Дата (YYYY-MM-DD):", bg="#f0f0f0")
        self.date_label.pack(pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.pack(pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Кнопки
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=20)

        self.add_button = tk.Button(button_frame, text="Добавить расход", command=self.add_expense, bg="#4CAF50", fg="white", width=15)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.view_button = tk.Button(button_frame, text="Просмотреть расходы", command=self.view_expenses, bg="#2196F3", fg="white", width=15)
        self.view_button.pack(side=tk.LEFT, padx=5)

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()
        date = self.date_entry.get()

        if not amount or not category or not date:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")
            return

        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (amount, category, description, date)
            VALUES (?, ?, ?, ?)
        ''', (float(amount), category, description, date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "Расход добавлен!")
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def view_expenses(self):
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses')
        rows = cursor.fetchall()
        conn.close()

        expenses_window = tk.Toplevel(self.root)
        expenses_window.title("Список расходов")
        expenses_window.geometry("400x300")

        tree = ttk.Treeview(expenses_window, columns=("Amount", "Category", "Description", "Date"), show='headings')
        tree.heading("Amount", text="Сумма")
        tree.heading("Category", text="Категория")
        tree.heading("Description", text="Описание")
        tree.heading("Date", text="Дата")
        tree.pack(fill=tk.BOTH, expand=True)

        for row in rows:
            tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
