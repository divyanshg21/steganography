from PIL import Image

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    pixel_values = list(img.getdata())

    binary_text = ""
    for pixel in pixel_values:
        for value in pixel:
            binary_text += str(value & 1)

    text = bits_to_text(binary_text)
    return text

def bits_to_text(bits):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

decoded_text = extract_text_from_image('stego_image.png')  # Change the path to your stego image
print("Decoded Text:", decoded_text)
