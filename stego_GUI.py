import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

# Function to encrypt message
def encrypt_message():
    filepath = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not filepath:
        return
    
    img = cv2.imread(filepath)
    msg = message_entry.get()
    password = passcode_entry.get()
    
    if not msg or not password:
        messagebox.showerror("Error", "Message and passcode cannot be empty!")
        return
    
    d = {chr(i): i for i in range(256)}
    n, m, z = 0, 0, 0
    
    for char in msg:
        if char in d:
            img[n, m, z] = d[char]
        else:
            messagebox.showerror("Error", "Invalid character in message!")
            return
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3
    
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        cv2.imwrite(save_path, img)
        messagebox.showinfo("Success", "Encryption successful! Image saved.")

# Function to decrypt message
def decrypt_message():
    filepath = filedialog.askopenfilename(title="Select Encrypted Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not filepath:
        return
    
    img = cv2.imread(filepath)
    password = passcode_entry.get()
    
    if not password:
        messagebox.showerror("Error", "Passcode cannot be empty!")
        return
    
    c = {i: chr(i) for i in range(256)}
    n, m, z = 0, 0, 0
    decrypted_message = ""
    
    try:
        for _ in range(100):  # Read first 100 characters
            pixel_value = img[n, m, z]
            if isinstance(pixel_value, np.ndarray):
                pixel_value = pixel_value[0]  # Take first value from array if needed
            if pixel_value in c:
                decrypted_message += c[pixel_value]
            else:
                break
            n = (n + 1) % img.shape[0]
            m = (m + 1) % img.shape[1]
            z = (z + 1) % 3
        
        if decrypted_message.strip():
            messagebox.showinfo("Decryption Result", f"Decrypted Message: {decrypted_message.strip()}")
        else:
            messagebox.showerror("Error", "No valid hidden message found!")
    except KeyError:
        messagebox.showerror("Error", "Decryption failed. Invalid encoded data.")

# GUI Setup
root = tk.Tk()
root.title("Secure Data Hiding in Images Using Steganography")
root.geometry("650x550")
root.configure(bg="white")

# Header Section
tk.Label(root, text="|| Jai Sri Gurudev ||", font=("Arial", 16, "bold"), fg="red", bg="white").pack(pady=5)
tk.Label(root, text="SJC INSTITUTE OF TECHNOLOGY", font=("Arial", 14, "bold"), bg="white").pack()
tk.Label(root, text="Chickballapur- 562101, Karnataka.", font=("Arial", 12), bg="white").pack()
tk.Label(root, text="Developer: Vinit Kumar Shukla", font=("Arial", 12, "bold"), bg="white").pack()
tk.Label(root, text="M Tech CSE 3rd Sem", font=("Arial", 12), bg="white").pack()
tk.Label(root, text="Edunet Foundation – AICTE Internship", font=("Arial", 12), bg="white").pack()
tk.Label(root, text="SkillsBuild Program on Cyber Security (CS)", font=("Arial", 12), bg="white").pack()
tk.Label(root, text="Title: Secure Data Hiding in Images Using Steganography", font=("Arial", 12, "bold"), bg="white").pack(pady=5)

# Input Section
frame = tk.Frame(root, bg="white")
frame.pack(pady=10)

tk.Label(frame, text="Enter Secret Message:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
message_entry = tk.Entry(frame, width=40, font=("Arial", 12))
message_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Enter Passcode:", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
passcode_entry = tk.Entry(frame, width=40, font=("Arial", 12), show="*")
passcode_entry.grid(row=1, column=1, padx=5, pady=5)

# Buttons Section
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=15)

encrypt_btn = tk.Button(button_frame, text="Encrypt Message", command=encrypt_message, bg="green", fg="white", font=("Arial", 12), width=20)
encrypt_btn.grid(row=0, column=0, padx=10, pady=5)

decrypt_btn = tk.Button(button_frame, text="Decrypt Message", command=decrypt_message, bg="blue", fg="white", font=("Arial", 12), width=20)
decrypt_btn.grid(row=0, column=1, padx=10, pady=5)

root.mainloop()
