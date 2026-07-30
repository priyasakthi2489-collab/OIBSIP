import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bmi_records.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi(
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    date TEXT
)
""")
conn.commit()

# ---------------- BMI FUNCTION ----------------
def calculate_bmi():
    try:
        name = name_entry.get().strip()

        if name == "":
            messagebox.showerror("Error", "Please enter your name.")
            return

        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and Height must be positive.")
            return

        bmi = weight / (height ** 2)

        if bmi < 18.5:
            category = "Underweight"
            color = "blue"
        elif bmi < 25:
            category = "Normal"
            color = "green"
        elif bmi < 30:
            category = "Overweight"
            color = "orange"
        else:
            category = "Obese"
            color = "red"

        result_label.config(
            text=f"BMI = {bmi:.2f}\nCategory = {category}",
            fg=color
        )

        cursor.execute(
            "INSERT INTO bmi VALUES (?,?,?,?,?)",
            (
                name,
                weight,
                height,
                bmi,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        conn.commit()

        messagebox.showinfo("Success", "BMI record saved successfully!")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# ---------------- GRAPH FUNCTION ----------------
def show_graph():
    name = name_entry.get().strip()

    if name == "":
        messagebox.showerror("Error", "Please enter the user name.")
        return

    try:
        cursor.execute(
            "SELECT date, bmi FROM bmi WHERE name=? ORDER BY date",
            (name,)
        )

        rows = cursor.fetchall()

        if len(rows) == 0:
            messagebox.showinfo("No Data", "No BMI records found for this user.")
            return

        dates = [row[0] for row in rows]
        bmi_values = [row[1] for row in rows]

        plt.figure(figsize=(7,4))
        plt.plot(dates, bmi_values, marker="o")
        plt.title(f"{name}'s BMI Trend")
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except sqlite3.Error:
        messagebox.showerror("Database Error", "Unable to read records.")

# ---------------- GUI ----------------
window = tk.Tk()
window.title("BMI Calculator")
window.geometry("400x400")

tk.Label(window, text="Name").pack(pady=5)
name_entry = tk.Entry(window)
name_entry.pack()

tk.Label(window, text="Weight (kg)").pack(pady=5)
weight_entry = tk.Entry(window)
weight_entry.pack()

tk.Label(window, text="Height (m)").pack(pady=5)
height_entry = tk.Entry(window)
height_entry.pack()

tk.Button(
    window,
    text="Calculate BMI",
    command=calculate_bmi
).pack(pady=10)

tk.Button(
    window,
    text="Show BMI Trend",
    command=show_graph
).pack(pady=5)

result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack(pady=20)

window.mainloop()

conn.close()
s
