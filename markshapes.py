import tkinter as tk

window = tk.Tk()
window.title("CGP Assignment - Canvas Drawing")
window.geometry("500x400")

canvas = tk.Canvas(window, width=500, height=400, bg="white")
canvas.pack()


canvas.create_rectangle(50, 50, 150, 150, fill="beige")

canvas.create_oval(200, 50, 350, 150, fill="blue")

canvas.create_line(50, 200, 300, 200, fill="green", width=3)

canvas.create_text(250, 350, text="Ramirez, Mark Adrian", font=("Arial", 15, "bold"))

# Run the window
window.mainloop()