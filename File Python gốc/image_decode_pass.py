import hashlib

def decode_hex_to_image(encoded_image_data, password):
    # Chuyển đổi chuỗi hex thành dữ liệu hình ảnh kết hợp mật khẩu
    image_data_with_password = bytes.fromhex(encoded_image_data)

    # Tách mật khẩu và dữ liệu đã mã hóa từ dữ liệu hình ảnh
    hashed_password = image_data_with_password[:32]
    encrypted_data = image_data_with_password[32:]

    # Mã hóa mật khẩu sử dụng SHA-256
    input_password_hash = hashlib.sha256(password.encode()).digest()

    # So sánh mật khẩu đã nhập với mật khẩu đã mã hóa trong dữ liệu hình ảnh
    if hashed_password != input_password_hash:
        print("Mật khẩu không đúng.")
        return

    # Giải mã dữ liệu hình ảnh
    return encrypted_data

def main():
    # Đọc chuỗi hex từ file đã mã hóa
    with open("encoded_image.txt", 'r') as encoded_file:
        encoded_image_data = encoded_file.read().strip()

    # Nhập mật khẩu từ người dùng
    password_input = input("Nhập mật khẩu để giải mã: ")

    # Giải mã dữ liệu hình ảnh
    decoded_image_data = decode_hex_to_image(encoded_image_data, password_input)

    if decoded_image_data:
        # Ghi dữ liệu hình ảnh đã giải mã vào file mới
        with open("decoded_image.png", 'wb') as decoded_file:
            decoded_file.write(decoded_image_data)
        print("Dữ liệu hình ảnh đã được giải mã và ghi vào file decoded_image.png.")

if __name__ == "__main__":
    main()
