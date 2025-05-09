import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

# === CONFIGURATION === #
FONT_NAME = "Courier"
DEFAULT_FONT_SIZE = 36
BACKGROUND_COLOR = '#85A98F'
BUTTON_COLOR = "#D3F1DF"
TEXT_COLOR = "#2C3930"

# === MAIN WINDOW SETUP === #
window = tk.Tk()
window.title("Image Watermark Tool")
window.config(padx=100, pady=50, bg=BACKGROUND_COLOR)

# === UTILITY FUNCTIONS === #
def save_image(image):
    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg;*.jpeg"), ("All Files", "*.*")],
    )
    if save_path:
        image.save(save_path)
        messagebox.showinfo("Saved", f"Image saved successfully to:\n{save_path}")

def open_image_and_add_text():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    if not file_path:
        return

    try:
        img = Image.open(file_path)
        watermark_text = simpledialog.askstring("Watermark", "Enter watermark text:")
        if not watermark_text:
            return

        watermarked_img = img.copy()
        draw = ImageDraw.Draw(watermarked_img)

        try:
            font = ImageFont.truetype("arial.ttf", DEFAULT_FONT_SIZE)
        except IOError:
            font = ImageFont.load_default()

        x = watermarked_img.width // 2
        y = watermarked_img.height // 2

        draw.text((x, y), text=watermark_text, fill=(255, 255, 255, 128), font=font,
                  anchor="ms", stroke_width=2, stroke_fill=(0, 0, 0))

        show_result_window(watermarked_img, file_path)

    except Exception as e:
        messagebox.showerror("Error", f"Could not process image:\n{str(e)}")

def add_logo_to_image():
    bg_path = filedialog.askopenfilename(title="Select Background Image")
    logo_path = filedialog.askopenfilename(title="Select Logo Image")
    if not bg_path or not logo_path:
        return

    try:
        background = Image.open(bg_path)
        logo = Image.open(logo_path).convert("RGBA")

        # Center logo
        x = (background.width - logo.width) // 2
        y = (background.height - logo.height) // 2
        background.paste(logo, (x, y), logo)

        show_result_window(background, bg_path)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to add logo:\n{str(e)}")

def show_result_window(image, title):
    image_copy = image.copy()
    image_copy.thumbnail((400, 400), Image.LANCZOS)
    tk_image = ImageTk.PhotoImage(image_copy)

    image_window = tk.Toplevel(window)
    image_window.title(f"Preview - {os.path.basename(title)}")
    label = tk.Label(image_window, image=tk_image)
    label.image = tk_image
    label.pack()

    save_btn = tk.Button(image_window, text="Save Image", command=lambda: save_image(image),
                         bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    save_btn.pack(pady=10)

# === GUI ELEMENTS === #
title_label = tk.Label(window, text="Image Watermark Tool",
                      font=(FONT_NAME, 24, "bold"), bg=BACKGROUND_COLOR, fg="#5A6C57")
title_label.grid(column=0, row=0, columnspan=3, pady=10)

canvas = tk.Canvas(window, width=400, height=300, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=1, columnspan=3, pady=20)

try:
    logo_img = Image.open("pictures.png")
    logo_img.thumbnail((400, 300), Image.LANCZOS)
    photo = ImageTk.PhotoImage(logo_img)
    canvas.create_image(200, 150, image=photo)
except Exception:
    canvas.create_text(200, 150, text="[Image Placeholder]", font=("Arial", 20), fill="white")

btn_add_text = tk.Button(window, text="Add Text Watermark", command=open_image_and_add_text,
                         bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=18, height=2)
btn_add_text.grid(column=0, row=2, padx=10, pady=10)

btn_add_logo = tk.Button(window, text="Add Logo Watermark", command=add_logo_to_image,
                         bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=18, height=2)
btn_add_logo.grid(column=2, row=2, padx=10, pady=10)

# === START MAINLOOP === #
window.mainloop()
