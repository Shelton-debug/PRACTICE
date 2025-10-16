import tkinter as tk

root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x400")
root.resizable(False, False)

entry = tk.Entry(root, font=("Arial", 24), bd=10, borderwidth=4, relief="ridge", justify="right")
entry.pack(padx=10, pady=10, fill="both")

def click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = eval(entry.get())
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, text)

buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"],
    ['.', '(', ')', '%']
]
for row in buttons:
    frame = tk.Frame(root)
    frame.pack(expand=True, fill="both")
    for value in row:
       btn = tk.Button(frame, text=value, font=("Arial", 18), height=2, width=4, bg="lightgray")
       btn.pack(side="left", expand=True, fill="both", padx=5, pady=5)
       btn.bind("<Button-1>", click)
       
root.mainloop()