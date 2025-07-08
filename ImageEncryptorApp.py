import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os

# Basic encryption: Add key and swap pixels
def encrypt_image(img, key):
    arr = np.array(img)
    flat = arr.flatten()
    np.random.seed(key)
    indices = np.arange(len(flat))
    np.random.shuffle(indices)

    flat = ((flat.astype(np.uint16) + key) % 256).astype(np.uint8)
    flat = flat[indices]

    encrypted = flat.reshape(arr.shape)
    return Image.fromarray(encrypted.astype(np.uint8))

# Reverse: Undo swap and subtract key
def decrypt_image(img, key):
    arr = np.array(img)
    flat = arr.flatten()

    np.random.seed(key)
    indices = np.arange(len(flat))
    shuffled_indices = np.argsort(np.random.permutation(len(flat)))

    flat = flat[shuffled_indices]
    flat = ((flat.astype(np.int16) - key) % 256).astype(np.uint8)

    decrypted = flat.reshape(arr.shape)
    return Image.fromarray(decrypted.astype(np.uint8))

class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 Image Encryptor & Decryptor")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e2f")

        self.original_image = None
        self.processed_image = None

        self.build_ui()

    def build_ui(self):
        title = tk.Label(self.root, text="🖼️ Image Encryption Tool", font=("Helvetica", 20, "bold"), bg="#1e1e2f", fg="#ffde59")
        title.pack(pady=10)

        self.canvas_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.canvas_frame.pack()

        self.original_label = tk.Label(self.canvas_frame, text="Original", bg="#1e1e2f", fg="#ffffff")
        self.original_label.grid(row=0, column=0, padx=20)

        self.result_label = tk.Label(self.canvas_frame, text="Result", bg="#1e1e2f", fg="#ffffff")
        self.result_label.grid(row=0, column=1, padx=20)

        self.original_canvas = tk.Label(self.canvas_frame)
        self.original_canvas.grid(row=1, column=0)

        self.processed_canvas = tk.Label(self.canvas_frame)
        self.processed_canvas.grid(row=1, column=1)

        control_frame = tk.Frame(self.root, bg="#1e1e2f")
        control_frame.pack(pady=20)

        self.key_entry = tk.Entry(control_frame, font=("Helvetica", 14))
        self.key_entry.insert(0, "1234")
        self.key_entry.grid(row=0, column=0, padx=10)

        load_btn = tk.Button(control_frame, text="📂 Load Image", command=self.load_image, bg="#3a3a5a", fg="#ffffff", font=("Helvetica", 12))
        load_btn.grid(row=0, column=1, padx=10)

        enc_btn = tk.Button(control_frame, text="🔐 Encrypt", command=self.encrypt, bg="#007acc", fg="white", font=("Helvetica", 12))
        enc_btn.grid(row=0, column=2, padx=10)

        dec_btn = tk.Button(control_frame, text="🔓 Decrypt", command=self.decrypt, bg="#00b386", fg="white", font=("Helvetica", 12))
        dec_btn.grid(row=0, column=3, padx=10)

        save_btn = tk.Button(control_frame, text="💾 Save Result", command=self.save_result, bg="#aa00ff", fg="white", font=("Helvetica", 12))
        save_btn.grid(row=0, column=4, padx=10)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            img = Image.open(path).convert("RGB")
            self.original_image = img
            self.display_image(img, self.original_canvas)

    def display_image(self, img, canvas):
        img = img.resize((300, 300))
        photo = ImageTk.PhotoImage(img)
        canvas.image = photo
        canvas.configure(image=photo)

    def get_key(self):
        try:
            return int(self.key_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Key", "Key must be an integer.")
            return None

    def encrypt(self):
        if not self.original_image:
            messagebox.showerror("Error", "Please load an image first.")
            return
        key = self.get_key()
        if key is None:
            return
        self.processed_image = encrypt_image(self.original_image, key)
        self.display_image(self.processed_image, self.processed_canvas)

    def decrypt(self):
        if not self.original_image:
            messagebox.showerror("Error", "Please load an image first.")
            return
        key = self.get_key()
        if key is None:
            return
        self.processed_image = decrypt_image(self.original_image, key)
        self.display_image(self.processed_image, self.processed_canvas)

    def save_result(self):
        if not self.processed_image:
            messagebox.showerror("Error", "No image to save.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png")])
        if path:
            self.processed_image.save(path)
            messagebox.showinfo("Saved", f"Image saved to {os.path.basename(path)}")

# Launch app
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()
