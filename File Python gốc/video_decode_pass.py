import hashlib

def decode_hex_to_video(encoded_video_data, password):
    # Chuyển đổi chuỗi hex thành dữ liệu video kết hợp mật khẩu
    video_data_with_password = bytes.fromhex(encoded_video_data)

    # Tách mật khẩu và dữ liệu đã mã hóa từ dữ liệu video
    hashed_password = video_data_with_password[:32]
    encrypted_data = video_data_with_password[32:]

    # Mã hóa mật khẩu sử dụng SHA-256
    input_password_hash = hashlib.sha256(password.encode()).digest()

    # So sánh mật khẩu đã nhập với mật khẩu đã mã hóa trong dữ liệu video
    if hashed_password != input_password_hash:
        print("Mật khẩu không đúng.")
        return

    # Giải mã dữ liệu video
    return encrypted_data

def main():
    # Đọc chuỗi hex từ file đã mã hóa
    with open("encoded_video.txt", 'r') as encoded_file:
        encoded_video_data = encoded_file.read().strip()

    # Nhập mật khẩu từ người dùng
    password_input = input("Nhập mật khẩu để giải mã: ")

    # Giải mã dữ liệu video
    decoded_video_data = decode_hex_to_video(encoded_video_data, password_input)

    if decoded_video_data:
        # Ghi dữ liệu video đã giải mã vào file mới
        with open("decoded_video.mp4", 'wb') as decoded_file:
            decoded_file.write(decoded_video_data)
        print("Dữ liệu video đã được giải mã và ghi vào file decoded_video.mp4.")

if __name__ == "__main__":
    main()
