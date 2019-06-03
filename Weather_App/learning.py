import tkinter as tk

window = tk.Tk()
window.title("Counting seconds")


button = tk.Button(window, text="Stop", width = 25, command=window.destroy)

button.pack()

window.mainloop()
