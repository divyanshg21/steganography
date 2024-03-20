import cv2
from PIL import Image

def text_to_bits(text):
    bits = bin(int.from_bytes(text.encode(), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def hide_text_in_frame(frame, text):
    height, width, _ = frame.shape
    binary_text = text_to_bits(text)
    binary_text_length = len(binary_text)
    available_space = width * height * 3

    print(f"Binary text length: {binary_text_length} bits")
    print(f"Available space in frame: {available_space} bits")

    if binary_text_length > available_space:
        print("Text too long to hide in the frame.")
        return frame

    index = 0
    for y in range(height):
        for x in range(width):
            for i in range(3):
                if index < len(binary_text):
                    frame[y][x][i] = frame[y][x][i] & ~1 | int(binary_text[index], 2)
                    index += 1

    print(f"Encoded {index} bits in the frame.")
    return frame

def hide_text_in_video(video_path, text):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(f"Video properties: FPS={fps}, Size={frame_size}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('stego_video.mp4', fourcc, fps, frame_size)
    if not out.isOpened():
        print("Error: Could not create the output video file.")
        cap.release()
        return
    print("Output video writer created successfully.")

    frame_count = 0
    frame_interval = 100  # Embed data in every 100th frame

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % frame_interval == 0:
            print(f"Processing frame {frame_count}")
            frame = hide_text_in_frame(frame, text)

        out.write(frame)

    cap.release()
    out.release()
    print("Video writer released successfully.")

    print("Text hidden in the video successfully.")

hide_text_in_video('input_video.mp4', "made by personate " * 10)