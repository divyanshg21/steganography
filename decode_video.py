import cv2

def bits_to_text(bits):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def extract_text_from_frame(frame):
    height, width, _ = frame.shape
    bits = ''

    for y in range(height):
        for x in range(width):
            for i in range(3):
                bits += str(frame[y][x][i] & 1)

    bits = ''.join([bits[i:i+8] for i in range(0, len(bits), 8)])
    decoded_text = ''

    for byte in bits:
        decoded_text += bits_to_text(byte)
        if bits_to_text(byte) == '\x00':
            break

    return decoded_text

def extract_text_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    decoded_text = ''
    frame_count = 0
    frame_interval = 100  # Extract data from every 100th frame

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % frame_interval == 0:
            print(f"Processing frame {frame_count}")
            decoded_text += extract_text_from_frame(frame)

    cap.release()
    return decoded_text

decoded_text = extract_text_from_video('stego_video.mp4')
print(f"Decoded text: {decoded_text}")