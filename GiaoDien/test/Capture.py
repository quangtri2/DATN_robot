import cv2
import os

# Đường dẫn để lưu ảnh
save_path = "path_to_save_images"  # Thay thế bằng đường dẫn thực tế của bạn
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Mở camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Không thể mở camera")
    exit()

print("Nhấn 'c' để chụp 20 ảnh.")
print("Nhấn 'q' để thoát.")

image_count = 0
max_images = 1
session_count = 1

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc từ camera")
        break
    

    # Hiển thị hình ảnh từ camera
    cv2.imshow("Camera", frame)

    # Nhấn phím
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):  # Nhấn 'c' để bắt đầu chụp
        print(f"Bắt đầu chụp ảnh cho phiên {session_count}...")
        image_count = 0

        while image_count < max_images:
            ret, frame = cap.read()
            if not ret:
                print("Không thể đọc từ camera")
                break

            # Lưu ảnh
            image_name = os.path.join(save_path, f"Lan4_{session_count}_image_{image_count + 1}.jpg")
            cv2.imwrite(image_name, frame)
            print(f"Đã lưu: {image_name}")
            image_count += 1

            # Hiển thị ảnh chụp trong một khoảng thời gian nhỏ
            cv2.imshow("Camera", frame)
            cv2.waitKey(100)  # Đợi 100ms giữa các lần chụp

        print(f"Hoàn tất chụp {max_images} ảnh cho phiên {session_count}.")
        session_count += 1

    elif key == ord('q'):  # Nhấn 'q' để thoát
        break

# Giải phóng camera và đóng tất cả các cửa sổ
cap.release()
cv2.destroyAllWindows()
