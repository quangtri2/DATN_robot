import qrcode

# Tên file mặc định

# Nhập nội dung để tạo mã QR
text = input("Nội dung: ")
print(f"Nội dung được nhập: {text}")

# Kiểm tra nếu nội dung rỗng
if not text.strip():
    print("Nội dung không được để trống. Hãy chạy lại chương trình!")
    exit()

# Tạo đối tượng QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Thêm dữ liệu vào QR Code
qr.add_data(text)
qr.make(fit=True)

# Tạo hình ảnh QR Code
img = qr.make_image(fill_color="black", back_color="white")

# Đường dẫn lưu file (sử dụng giá trị của name)
file_path = rf"C:\Users\quang\OneDrive\Desktop\DATN\picture\{text}.png"

# Lưu file trực tiếp
img.save(file_path)
print(f"Mã QR đã được lưu tại: {file_path}")
print(f"Mã QR chứa nội dung: {text}")
