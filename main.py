import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

# Constants
FONT_NAME = "Courier"
BG_COLOR = '#85A98F'
BUTTON_COLOR = '#D3F1DF'
TEXT_COLOR = '#2C3930'

# Main window setup
window = tk.Tk()
window.title("Image Watermark")
window.config(padx=100, pady=50, highlightthickness=0, bg=BG_COLOR)


def save_image(image):
    """Save the watermarked image to a file"""
    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Files", "*.png"),
            ("JPEG Files", "*.jpg;*.jpeg"),
            ("All Files", "*.*"),
        ],
    )
    if save_path:
        try:
            image.save(save_path)
            messagebox.showinfo("Saved", f"Image saved successfully to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image:\n{str(e)}")


def show_image_window(img, title):
    """Display the watermarked image in a new window"""
    # Resize for display (preserve aspect ratio)
    display_size = (400, 400)
    img.thumbnail(display_size, Image.LANCZOS)
    
    # Convert for Tkinter
    photo = ImageTk.PhotoImage(img)
    
    # Create a new window
    image_window = tk.Toplevel(window)
    image_window.title(title)
    
    # Display the image
    label = tk.Label(image_window, image=photo)
    label.image = photo  # Keep a reference!
    label.pack()
    
    # Add save button
    save_btn = tk.Button(
        image_window,
        text="Save Watermarked Image",
        command=lambda: save_image(img),
        bg="#4CAF50",
        fg="white"
    )
    save_btn.pack(pady=10)


def add_text_watermark():
    """Add text watermark to an image"""
    try:
        # Ask user to select an image
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if not file_path:
            return
        
        # Open and convert image
        img = Image.open(file_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Ask for watermark text
        watermark_text = simpledialog.askstring("Watermark", "Enter watermark text:")
        if not watermark_text:
            return
        
        # Create drawing context
        draw = ImageDraw.Draw(img)
        
        # Font handling with multiple fallbacks
        font_size = min(img.size) // 10  # 10% of smallest dimension
        try:
            # Try several common fonts
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("arialbd.ttf", font_size)
                except:
                    font = ImageFont.load_default().font_variant(size=font_size)
        except Exception as e:
            messagebox.showwarning("Font Warning", f"Using default font: {str(e)}")
            font = ImageFont.load_default()
        
        # Calculate text size and position
        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
        
        # Add text with outline effect
        for x_offset, y_offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            draw.text(
                (x + x_offset, y + y_offset),
                watermark_text,
                font=font,
                fill=(0, 0, 0, 128)  # Black outline
            )
        draw.text(
            (x, y),
            watermark_text,
            font=font,
            fill=(255, 255, 255, 180)  # White text
        )
        
        # Show the result
        show_image_window(img, "Watermarked - " + os.path.basename(file_path))
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add watermark:\n{str(e)}")


def add_logo_watermark():
    """Add logo watermark to an image"""
    # Get background image
    bg_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    if not bg_path:
        return
    
    # Get logo image
    logo_path = filedialog.askopenfilename(
        filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
        title="Select Logo Image (PNG with transparency)"
    )
    if not logo_path:
        return
    
    try:
        background = Image.open(bg_path).convert('RGBA')
        logo = Image.open(logo_path).convert('RGBA')
        
        # Resize logo to 20% of background width (maintain aspect ratio)
        new_width = background.width // 5
        ratio = new_width / float(logo.width)
        new_height = int(float(logo.height) * ratio)
        logo = logo.resize((new_width, new_height), Image.LANCZOS)
        
        # Position logo in bottom-right corner with margin
        position = (
            background.width - logo.width - 20,
            background.height - logo.height - 20
        )
        
        # Create transparent layer for logo
        transparent = Image.new('RGBA', background.size, (0, 0, 0, 0))
        transparent.paste(logo, position, logo)
        
        # Combine images
        watermarked = Image.alpha_composite(background, transparent)
        
        show_image_window(watermarked, "Logo Watermark - " + bg_path.split('/')[-1])
    
    except Exception as e:
        messagebox.showerror("Error", f"Could not process images:\n{str(e)}")


# UI Elements
canvas = tk.Canvas(window, width=400, height=448, bg=BG_COLOR, highlightthickness=0)
photo = tk.PhotoImage(file="pictures.png")
canvas.create_image(200, 224, image=photo)
canvas.grid(column=0, row=2, columnspan=3, pady=10)

title_label = tk.Label(
    text="Image Watermark Tool",
    font=(FONT_NAME, 24, "bold"),
    fg="#5A6C57",
    bg=BG_COLOR
)
title_label.grid(column=0, row=0, columnspan=3, pady=10)

# Buttons
button_style = {
    'highlightthickness': 0,
    'width': 15,
    'height': 2,
    'font': ("Arial", 12),
    'bg': BUTTON_COLOR,
    'fg': TEXT_COLOR,
    'activebackground': "#45a049",
    'activeforeground': "white",
    'relief': "raised"
}

text_button = tk.Button(
    text="Add Text",
    command=add_text_watermark,
    **button_style
)
text_button.grid(column=0, row=3, padx=10, pady=10)

logo_button = tk.Button(
    text="Add Logo",
    command=add_logo_watermark,
    **button_style
)
logo_button.grid(column=2, row=3, padx=10, pady=10)

window.mainloop()