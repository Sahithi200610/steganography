import cv2 as cv
import os
import string
import hashlib

def hide_message_with_passcode(image_path, message, passcode, output_path):
    key = hashlib.sha256(passcode.encode()).digest()

    encrypted_message = ''.join([chr(ord(char) ^ key[i % len(key)]) for i, char in enumerate(message)])

    encrypted_message += '###'  
    binary_message = ''.join([format(ord(c), '08b') for c in encrypted_message])

    img = cv.imread(image_path)
    if img is None:
        raise ValueError("Image not found!")

    max_bytes = img.shape[0] * img.shape[1] * 3 // 8
    if len(binary_message) > max_bytes:
        raise ValueError("Message is too long to fit in the image.")

    data_index = 0
    for row in img:
        for pixel in row:
            for i in range(3):
                if data_index < len(binary_message):
                    pixel[i] = int(format(pixel[i], '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1

    cv.imwrite(output_path, img)
    os.system(f'start {output_path}')  

image_path = 'mypic.jpg'
output_path = 'encryptedImage.png'
message = input("Enter the secret message:")
passcode = input("Enter a passcode:")
hide_message_with_passcode(image_path, message, passcode, output_path)
print("Message hidden successfully in", output_path)
