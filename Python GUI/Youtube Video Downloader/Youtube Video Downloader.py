from pytube import YouTube
import tkinter as tk
from tkinter import ttk
from tkinter import *
import io
import base64
import urllib.request
import io
from PIL import Image, ImageTk
import tkinter as tk
from urllib.request import urlopen
from threading import *
from plyer import notification


root = Tk()
root.title("YouTube Video Downloader")

photo = PhotoImage(file = "youtube_logo.png")
root.iconphoto(True, photo)

yt = YouTube('https://www.youtube.com/watch?v=rsNnQt3DmA4')
url_image = yt.thumbnail_url


def threading_download():
    # Call download function
    t=Thread(target=download)
    t.start()
    
def threading_search():
    # Call search function
    t = Thread(target=search)
    t.start()

def show_image(url):
    image_bytes = urlopen(url).read()
    # internal data file
    data_stream = io.BytesIO(image_bytes)
    # open as a PIL image object
    pil_image = Image.open(data_stream)

    # optionally show image info
    # get the size of the image
    w, h = pil_image.size
    # split off image file name
    fname = url.split('/')[-1]
    sf = "{} ({}x{})".format(fname, w, h)
    root.title(sf)

    # convert PIL image object to Tkinter PhotoImage object
    tk_image = ImageTk.PhotoImage(pil_image)

    # put the image on a typical widget
    label = tk.Label(root, image=tk_image, bg='black')
    label.pack(padx=5, pady=5)
    
def search():
    url = entry.get()
    global yt
    yt = YouTube(url)
    title = yt.title
    label_text.set(title)
    set_quality_combobox()
    

def download():
    resolution = quality_combo.get()
    if resolution in quality:
        notification.notify(title='Quality of Picture not selected',
                            message='Please Select the Quality of Picture !!! ',
                            app_icon=None, 
                            timeout=10,
                           )
            
    stream = yt.streams.filter(file_extension='mp4', res=quality_combo.get())
    stream.first().download()
    

def set_quality_combobox():
    stream = yt.streams.filter(file_extension='mp4')
    global quality
    quality = ["48p", "128p", "144p", "240p", "360p" ,"480p", "720p", "1080p"]

    for i in quality:
        li = stream.filter(res=i).first()
        if li==None:
            quality.remove(i)
    
    quality_combo['values'] = quality
    
    
    
#=====================================================================================================================

entry = ttk.Entry(root, width=60)
entry.grid(row=2, column=1, columnspan=3, sticky="NSEW", padx=2, pady=2)

label_text = StringVar()
label_text.set("Download the Video")
label = Label(root, textvariable=label_text, width=50)
label.grid(row=1, column=1, columnspan=3, padx=2, pady=2)
    
n = tk.StringVar()
n.set("Quality")
quality_combo = ttk.Combobox(root, width = 27, textvariable = n)
quality_combo.grid(row=3, column=1, padx=2, pady=2)

search_button = Button(root, text="Search", command=threading_search, width = 15)
search_button.grid(row=3, column=2, padx=2, pady=2)

download_button = Button(root, text="Download", command=threading_download, width = 15)
download_button.grid(row=3, column=3, padx=2, pady=2)


root.mainloop()