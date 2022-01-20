import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont


TRANSPARENCY = 180  # 0 (full transparent) - 255 (not transparent)
# R, G, B = (0, 0, 0)  # black
COLORS = {"black": (0, 0, 0),
          "white": (255, 255, 255)}


def img_opacity(image_object, level):
    """
    :param image_object: Image object from Pillow
    :param level: Transparency (0-255)
    :return: None

    Add opacity(transparency) to an Image object only to nontransparent pixels.
    """
    data = image_object.getdata()
    new_data = []
    for item in data:
        if item[3] != 0:  # if pixel is not transparent (alpha channel is not 0)
            r_, g_, b_, a_ = item
            new_data.append((r_, g_, b_, level))  # change only alpha channel
        else:
            new_data.append(item)
    image_object.putdata(new_data)


def text_watermark(image_path, wm_text, output_path, wm_text_color):
    im = Image.open(image_path).convert("RGBA")  # open image and convert to have alpha channel
    txt_im = Image.new("RGBA", im.size, (0, 0, 0, 0))  # new transparent image of same size for text
    width, height = txt_im.size
    draw = ImageDraw.Draw(txt_im)
    font = ImageFont.truetype("arial.ttf", height // 10)
    txt_width, txt_height = draw.textsize(wm_text, font)
    margin = height // 30
    x = width - txt_width - margin
    y = height - txt_height - margin
    coordinates = (x, y)
    draw.text(coordinates, wm_text, wm_text_color, font=font)

    watermarked_im = Image.alpha_composite(im, txt_im)  # combine 2 images
    watermarked_im = watermarked_im.convert("RGB")
    watermarked_im.save(output_path)


def image_watermark(image_path, watermark_path, output_path):
    im = Image.open(image_path).convert("RGBA")  # open image and convert to have alpha channel
    wm_im = Image.new("RGBA", im.size, (0, 0, 0, 0))  # new transparent image of same size for watermark
    width, height = wm_im.size
    watermark = Image.open(watermark_path).convert("RGBA")  # open watermark image and convert to have alpha channel
    img_opacity(watermark, TRANSPARENCY)
    wm_width, wm_height = watermark.size
    margin = height // 30
    x = width - wm_width - margin
    y = height - wm_height - margin
    coordinates = (x, y)
    wm_im.paste(watermark, coordinates)

    watermarked_im = Image.alpha_composite(im, wm_im)  # combine 2 images
    watermarked_im = watermarked_im.convert("RGB")
    watermarked_im.save(output_path)


def select_image():
    global image
    image = fd.askopenfilename(initialdir=".", title="Select an Image")
    folder = image.split("/")[-2]
    filename = image.split("/")[-1]
    label_image.configure(text=f"Chosen image: {folder}/{filename}")


def select_watermark_image():
    global watermark_image
    watermark_image = fd.askopenfilename(initialdir=".", title="Select an Image")
    folder = watermark_image.split("/")[-2]
    watermark_filename = watermark_image.split("/")[-1]
    label_watermark_image.configure(text=f"Chosen image: {folder}/{watermark_filename}")
    # radio_state.set("image")


def radio_used():
    if radio_state.get() == "image":
        label_choose_watermark.configure(state="normal")
        select_watermark_button.configure(state="normal")
        label_watermark_image.configure(state="normal")
        label_watermark_text.configure(state="disabled")
        entry_watermark_text.configure(state="disabled")
        text_color_listbox.configure(state="disabled")
    else:
        label_choose_watermark.configure(state="disabled")
        select_watermark_button.configure(state="disabled")
        label_watermark_image.configure(state="disabled")
        label_watermark_text.configure(state="normal")
        entry_watermark_text.configure(state="normal")
        text_color_listbox.configure(state="normal")


def text_color_listbox_used(event):
    global r
    global g
    global b
    text_color = text_color_listbox.get(text_color_listbox.curselection())
    r, g, b = (COLORS[text_color])
    return event  # this line is only to "use" event so the code has no warnings :)


def watermark_func():
    try:
        option = radio_state.get()
        if option == "text":
            text_watermark(image, entry_watermark_text.get(), output_image, (r, g, b, a))
        else:
            image_watermark(image, watermark_image, output_image)

        messagebox.showinfo(title="Watermark Added", message="Watermark successfully added to image!")
    except AttributeError:
        messagebox.showerror(title="Error", message="Please select an image!")


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
entry_watermark_text.grid(column=0, row=5, sticky="W")

text_color_listbox = tk.Listbox()
i = 0
for color in COLORS:
    text_color_listbox.insert(i, color)
    i += 1
text_color_listbox.config(height=i)
text_color_listbox.bind("<<ListboxSelect>>", text_color_listbox_used)
text_color_listbox.grid(column=0, row=6, sticky="W", pady=(0, 15))

radiobutton_image = tk.Radiobutton(text="Image Watermark", value="image", variable=radio_state, command=radio_used)
radiobutton_image.grid(column=0, row=7, sticky="W")

label_choose_watermark = tk.Label(text="Choose watermark image: none")
label_choose_watermark.grid(column=0, row=8, sticky="W")
label_choose_watermark.configure(state="disabled")

select_watermark_button = tk.Button(text="Browse images", command=select_watermark_image)
select_watermark_button.grid(column=0, row=9, sticky="W")
select_watermark_button.configure(state="disabled")

label_watermark_image = tk.Label(text="Chosen image: none")
label_watermark_image.grid(column=0, row=10, sticky="W", pady=(0, 30))
label_watermark_image.configure(state="disabled")

watermark_button = tk.Button(text="Watermark the selected image!", command=watermark_func)
watermark_button.grid(column=0, row=11,  sticky="W", pady=(0, 30))

image = ""
watermark_image = ""
output_image = "watermark.jpg"
r, g, b, a = (0, 0, 0, 255)

window.mainloop()
