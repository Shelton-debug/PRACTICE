import tkinter as tk
from tkinter import Listbox, messagebox

root = tk.Tk()
root.title("To-Do List")
root.geometry("400x450")
root.resizable(False, False)

def add_task():
    task = entry.get()
    if task != "":
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def delete_task():
    try:
        selected = listbox.curselection()[0]
        listbox.delete(selected)
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

def clear_tasks():
    listbox.delete(0, tk.END)
    
def show_tasks():
    tasks = listbox.get(0, tk.END)
    if tasks:
        messagebox.showinfo("Tasks", "\n".join(tasks))
    else:
        messagebox.showinfo("Tasks", "No tasks available.")
        
def save_tasks():
    tasks = listbox.get