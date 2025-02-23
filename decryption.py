import cv2 as cv
import string
import hashlib

def reveal_message_with_passcode(image_path, passcode):
    
    key = hashlib.sha256(passcode.encode()).digest()

    img = cv.imread(image_path)
    if img is None:
        raise ValueError("Image not found!")

    binary_message = ''
    for row in img:
        for pixel in row:
            for i in range(3):
                binary_message += format(pixel[i], '08b')[-1]

    all_bytes = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    encrypted_message = ''
    for byte in all_bytes:
        encrypted_message += chr(int(byte, 2))
        if encrypted_message[-3:] == '###':  
            break

    encrypted_message = encrypted_message[:-3]  

    
    decrypted_message = ''.join([chr(ord(char) ^ key[i % len(key)]) for i, char in enumerate(encrypted_message)])

    return decrypted_message

encrypted_image_path = 'encryptedImage.png'
passcode = input("Enter passcode for Decryption:")
message = reveal_message_with_passcode(encrypted_image_path, passcode)
print("Decrypted message:", message)
