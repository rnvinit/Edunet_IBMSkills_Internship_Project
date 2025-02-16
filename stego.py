"""
=============================================================
Secure Data Hiding in Images Using Steganography
=============================================================

Name of Developer: Vinit Kumar Shukla
M Tech CSE 3rd Sem 
SJC INSTITUTE OF TECHNOLOGY
Chickballapur- 562101, Karnataka.
Edunet Foundation – AICTE Internship
SkillsBuild Program on Cyber Security (CS)
"""

import cv2
import os
import numpy as np

# File Paths
IMAGE_PATH = r"D:\M Tech\M Tech 3rd Sem\Internship\Edunet-CS-Project\Vinit_Img.png"
OUTPUT_PATH = r"D:\M Tech\M Tech 3rd Sem\Internship\Edunet-CS-Project\encrypted_image.png"

# Character encoding dictionaries
char_to_int = {chr(i): i for i in range(256)}
int_to_char = {i: chr(i) for i in range(256)}

def embed_message(image_path, output_path, secret_message, passcode):
    """
    Embeds a secret message into an image without corrupting its structure.
    """
    img = cv2.imread(image_path)
    
    if img is None:
        print("Error: Unable to read the image. Please check the path.")
        return False

    # Convert to writable format
    img = np.array(img, dtype=np.uint8)

    height, width, _ = img.shape
    total_pixels = height * width * 3  # Storage capacity in RGB channels

    if len(secret_message) > total_pixels - 10:  # Ensuring safe storage
        print("Error: Message too large to fit in the image!")
        return False

    # Convert passcode to ASCII values
    password_ascii = [char_to_int[char] for char in passcode]

    # Store message length in the first pixel
    img[0, 0, 0] = len(secret_message)

    # Store passcode length in the second pixel
    img[0, 0, 1] = len(passcode)

    # Embed the passcode in the next pixels
    for i, char in enumerate(password_ascii):
        img[0, i + 1, 0] = char  

    # Embed the message
    idx = 0
    for row in range(height):
        for col in range(width):
            for channel in range(3):  # RGB channels
                if row == 0 and col < (len(passcode) + 1):
                    continue  # Skip first few pixels used for metadata
                
                if idx < len(secret_message):
                    img[row, col, channel] = char_to_int[secret_message[idx]]
                    idx += 1
                else:
                    break

    # Save encrypted image
    cv2.imwrite(output_path, img)
    print(f"Encryption successful! Image saved as: {output_path}")

    # Open image using system default viewer
    os.system(f'start "" "{output_path}"')

    return True

def extract_message(image_path):
    """
    Extracts the hidden message from an image using the correct passcode.
    """
    img = cv2.imread(image_path)
    
    if img is None:
        print("Error: Unable to read the image. Please check the path.")
        return False

    # Retrieve the stored message length
    msg_len = img[0, 0, 0]

    # Retrieve the stored passcode length
    passcode_len = img[0, 0, 1]

    # Retrieve the stored passcode
    stored_passcode = ""
    for i in range(passcode_len):
        stored_passcode += int_to_char[img[0, i + 1, 0]]

    # Ask for user input passcode
    entered_passcode = input("Enter passcode for decryption: ")

    if entered_passcode != stored_passcode:
        print("AUTHENTICATION FAILED: Incorrect passcode.")
        return False

    # Extract the hidden message
    secret_message = ""
    idx = 0
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            for channel in range(3):  # RGB channels
                if row == 0 and col < (passcode_len + 1):
                    continue  # Skip metadata
                
                if idx < msg_len:
                    secret_message += int_to_char[img[row, col, channel]]
                    idx += 1
                else:
                    break

    print(f"Decryption Successful! Secret message:\n{secret_message}")
    return True


# ========== MAIN PROGRAM ==========

print("Welcome to Secure Image Steganography")
print("-------------------------------------")
print("1. Encrypt a message in an image")
print("2. Decrypt a message from an image")

choice = input("Enter your choice (1/2): ")

if choice == "1":
    secret_message = input("Enter your secret message: ")
    passcode = input("Set a passcode for encryption: ")

    embed_message(IMAGE_PATH, OUTPUT_PATH, secret_message, passcode)

elif choice == "2":
    extract_message(OUTPUT_PATH)

else:
    print("Invalid choice! Please enter either 1 or 2.")
