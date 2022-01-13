import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont


def text_watermark(image_path, watermark_text, output_path, text_color="black"):
    im = Image.open(image_path)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    width, height = im.size
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("arial.ttf", height // 10)
    txt_width, txt_height = draw.textsize(watermark_text, font)
    margin = height // 30
    x = width - txt_width - margin
    y = height - txt_height - margin
    coordinates = (x, y)
    draw.text(coordinates, watermark_text, text_color, font=font)
    im.save(output_path)


def image_watermark(image_path, watermark_path, output_path):
    im = Image.open(image_path)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    width, height = im.size
    watermark = Image.open(watermark_path)
    wm_width, wm_height = watermark.size
    margin = height // 30
    x = width - wm_width - margin
    y = height - wm_height - margin
    coordinates = (x, y)
    im.paste(watermark, coordinates)
    im.save(output_path)


def select_image():
    global image
    image = fd.askopenfilename(initialdir=".", title="Select an Image")
    label_image.configure(text=f"Chosen image: {image}")


def select_watermark_image():
    global watermark_image
    watermark_image = fd.askopenfilename(initialdir=".", title="Select an Image")
    label_watermark_image.configure(text=f"Chosen image: {watermark_image}")
    # radio_state.set("image")


def radio_used():
    if radio_state.get() == "image":
        label_choose_watermark.configure(state="normal")
        select_watermark_button.configure(state="normal")
        label_watermark_image.configure(state="normal")
        label_watermark_text.configure(state="disabled")
        entry_watermark_text.configure(state="disabled")
    else:
        label_choose_watermark.configure(state="disabled")
        select_watermark_button.configure(state="disabled")
        label_watermark_image.configure(state="disabled")
        label_watermark_text.configure(state="normal")
        entry_watermark_text.configure(state="normal")


def watermark_func():
    option = radio_state.get()
    if option == "text":
        text_watermark(image, entry_watermark_text.get(), output_image)
    else:
        image_watermark(image, watermark_image, output_image)

    messagebox.showinfo(title="Watermark Added", message="Watermark successfully added to image!")


window = tk.Tk()
window.title("Image Watermarking")
window.minsize(width=600, height=0)
window.config(pady=30, padx=45)

label_choose = tk.Label(text="Choose an image: ")
label_choose.grid(column=0, row=0, sticky="W", pady=(0, 3))

select_button = tk.Button(text="Browse images", command=select_image)
select_button.grid(column=0, row=1, sticky="W")

label_image = tk.Label(text="Chosen image: none")
label_image.grid(column=0, row=2, sticky="W", pady=(0, 15))


radio_state = tk.StringVar()
radio_state.set("text")
radiobutton_text = tk.Radiobutton(text="Text Watermark", value="text", variable=radio_state, command=radio_used)
radiobutton_text.grid(column=0, row=3, sticky="W")

label_watermark_text = tk.Label(text="Enter Watermark Text: ")
label_watermark_text.grid(column=0, row=4, sticky="W")

entry_watermark_text = tk.Entry()
entry_watermark_text.grid(column=0, row=5, sticky="W", pady=(0, 15))

radiobutton_image = tk.Radiobutton(text="Image Watermark", value="image", variable=radio_state, command=radio_used)
radiobutton_image.grid(column=0, row=6, sticky="W")

label_choose_watermark = tk.Label(text="Choose watermark image: none")
label_choose_watermark.grid(column=0, row=7, sticky="W")
label_choose_watermark.configure(state="disabled")

select_watermark_button = tk.Button(text="Browse images", command=select_watermark_image)
select_watermark_button.grid(column=0, row=8, sticky="W")
select_watermark_button.configure(state="disabled")

label_watermark_image = tk.Label(text="Chosen image: none")
label_watermark_image.grid(column=0, row=9, sticky="W", pady=(0, 30))
label_watermark_image.configure(state="disabled")

watermark_button = tk.Button(text="Watermark the selected image!", command=watermark_func)
watermark_button.grid(column=0, row=10,  sticky="W", pady=(0, 30))

image = ""
watermark_image = ""
output_image = "watermark.jpg"

window.mainloop()
