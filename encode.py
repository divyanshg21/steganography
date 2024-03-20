from PIL import Image

def text_to_bits(text):
    bits = bin(int.from_bytes(text.encode(), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def hide_text_in_image(image_path, text):
    img = Image.open(image_path)
    width, height = img.size
    binary_text = text_to_bits(text)
    binary_text_length = len(binary_text)

    if binary_text_length > width * height * 3:
        print("Text too long to hide in the image.")
        return

    binary_text += '0' * ((width * height * 3) - binary_text_length)

    pixel_values = list(img.getdata())

    new_pixel_values = []
    index = 0
    for pixel in pixel_values:
        if index < len(binary_text):
            new_pixel = list(pixel)
            for i in range(3):
                new_pixel[i] = new_pixel[i] & ~1 | int(binary_text[index], 2)
                index += 1
            new_pixel_values.append(tuple(new_pixel))
        else:
            new_pixel_values.append(pixel)

    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixel_values)
    new_img.save('stego_image.png')

    print("Text hidden in the image successfully.")

hide_text_in_image('input_image.png', "made by personate " * 100)  
