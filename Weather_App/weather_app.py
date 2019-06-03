import tkinter as tk
from retrieve_weather_information import retrieve

class Weather:
    def __init__(self, master):
        
        master.title("WEATHER APP")
        tk.Label(master, text="City name").grid(row=0)
        self.e1 = tk.Entry(master)
        self.e1.grid(row=0, column=1)
        self.btn1 = tk.Button(master, text="Submit", width=8, height=3,  command=self.get_info)
        self.btn1.grid(row=1)
        self.label1 = tk.Label(master, text="Temperature in Celcius")
        self.label1.grid(row=2)
        self.e2 = tk.Entry(master)
        self.e2.grid(row=2, column = 1)
        self.label2 = tk.Label(master, text="Description")
        self.label2.grid(row=3)
        self.e3 = tk.Entry(master)
        self.e3.grid(row=3, column = 1)

    def get_info(self):
        output = retrieve(self.e1.get())
        
        if output["cod"] != "404":
            self.label1.grid()
            self.label2.grid()
            self.e3.grid()
            self.e2.delete(0, tk.END)
            self.e2.insert(0, "{:.2f}".format(output["main"]["temp"] - 273))
            self.e3.delete(0, tk.END)
            self.e3.insert(0, output["weather"][0]["description"])
        else:
            self.label1.grid_forget()
            self.label2.grid_forget()
            self.e3.grid_forget()
            self.e2.delete(0, tk.END)
            self.e2.insert(0, "City not found")
            


window = tk.Tk()
app = Weather(window)

window.mainloop()
