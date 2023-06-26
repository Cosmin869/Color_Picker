import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
import pyautogui
import serial
from PIL import ImageTk, Image
import time


root = tk.Tk()
root.title("Picker")
root.geometry("600x600")

imag = Image.open("Color_circle.jpg")
imag = imag.resize((400, 400))  # Schimbam dimensiunile
photo = ImageTk.PhotoImage(imag)
image_label = tk.Label(root, image=photo)
image_label.pack()

ser = serial.Serial('COM3', 9600)

def get_rgb_color(x, y):
    screenshot = pyautogui.screenshot()
    color = screenshot.getpixel((x, y))
    return color

def color(event):
    image_x = root.winfo_rootx() + image_label.winfo_x()
    image_y = root.winfo_rooty() + image_label.winfo_y()
    mx = image_x + event.x
    my = image_y + event.y 
    color = get_rgb_color(mx, my)
    r,g,b = color
    rgb_color = f'{r},{g},{b}'
    backcolor = '#%02x%02x%02x' % color
    root.configure(background=backcolor)
    print(rgb_color)
    send_color_to_arduino(rgb_color)
    #root.unbind("<Button-1>")
    

def send_color_to_arduino(rgb_color):
    ser.write(f'{rgb_color}\n'.encode())

def selectPicture():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        # Updatam imaginea cu paleta de culori cu noua imagine
        image = Image.open(file_path)
        image = image.resize((400, 400))  # Modificam dimensiunile
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo  # incarcam poza in variabila

def buttonAction():
    choose_color = colorchooser.askcolor()[0]
    r,g,b = choose_color
    rgb_color = f'{r},{g},{b}'
    backcolor = '#%02x%02x%02x' % choose_color
    root.configure(background=backcolor)
    print(rgb_color)
    send_color_to_arduino(rgb_color)
    time.sleep(1)
    
    #print(choose_color)


# Butoanele
PickColorButton = tk.Button(root, text="Pick a color", command=buttonAction)
PickColorButton.pack()
root.bind("<Motion>", color)
#root.bind("",RGB_Spectrum())
UploadPhotoButton = tk.Button(root, text="Select a Picure", command=selectPicture)
UploadPhotoButton.pack()

root.mainloop()
