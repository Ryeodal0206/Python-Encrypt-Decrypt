import hashlib

def encode_video_to_hex(video_path, password):
    # Đọc nội dung của video dưới dạng byte
    with open(video_path, 'rb') as f:
        video_data = f.read()

    # Mã hóa mật khẩu sử dụng SHA-256
    hashed_password = hashlib.sha256(password.encode()).digest()

    # Kết hợp mật khẩu với dữ liệu video
    video_data_with_password = hashed_password + video_data

    # Chuyển đổi dữ liệu video kết hợp mật khẩu thành chuỗi hex
    encoded_data = video_data_with_password.hex()

    return encoded_data

def main():
    # Đường dẫn đến video
    video_path = "D:\Crypto\BEST_TrendLines_Strategy.mp4"

    # Mật khẩu để mã hóa video
    password = "12345"

    # Mã hóa video thành chuỗi hex với mật khẩu
    encoded_video_data = encode_video_to_hex(video_path, password)

    # Ghi chuỗi hex vào file mới
    with open("encoded_video.txt", 'w') as encoded_file:
        encoded_file.write(encoded_video_data)

    print("Video đã được mã hóa và ghi vào file encoded_video.txt")

if __name__ == "__main__":
    main()
