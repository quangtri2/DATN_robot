import tkinter as tk
from tkinter import ttk
import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import threading
import queue
import time

def exit_program():
    """Thoát khỏi chương trình và giải phóng tài nguyên"""
    global running
    running = False
    if cap1:
        cap1.release()
    if cap2:
        cap2.release()
    cv2.destroyAllWindows()
    root.destroy()

def process_qr(frame):
    """Xử lý và quét mã QR"""
    qr_codes = decode(frame)
    for qr_code in qr_codes:
        data = qr_code.data.decode('utf-8')
        print(f"Đã quét được: {data}")

        # Vẽ khung quanh QR Code
        points = qr_code.polygon
        if len(points) == 4:
            pts = [(point.x, point.y) for point in points]
            pts.append(pts[0])
            for i in range(len(pts) - 1):
                cv2.line(frame, pts[i], pts[i + 1], (0, 255, 0), 2)

        # Hiển thị nội dung
        cv2.putText(frame, data, (qr_code.rect.left, qr_code.rect.top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return frame

def capture_camera(camera, queue, is_qr):
    """Luồng để đọc camera và gửi khung hình qua queue"""
    while running:
        ret, frame = camera.read()
        if ret:
            frame = cv2.resize(frame, (400, 300))
            if is_qr:
                frame = process_qr(frame)
            queue.put(frame)
        time.sleep(0.05)  # Giảm tần suất xử lý (20 FPS)

def update_frame(label, queue):
    """Cập nhật khung hình từ queue lên giao diện Tkinter"""
    if not queue.empty():
        frame = queue.get()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        label.imgtk = img
        label.configure(image=img)
    label.after(20, update_frame, label, queue)

# Tạo giao diện Tkinter
root = tk.Tk()
root.title("Quét mã QR và hiển thị camera")
root.geometry("850x400")

# Khung Camera 1
frame1 = tk.Frame(root, bg="lightblue", bd=2, relief="solid")
frame1.place(x=10, y=10, width=400, height=300)
cam1_label = tk.Label(frame1)
cam1_label.pack(expand=True)

# Khung Camera 2
frame2 = tk.Frame(root, bg="lightgreen", bd=2, relief="solid")
frame2.place(x=430, y=10, width=400, height=300)
cam2_label = tk.Label(frame2)
cam2_label.pack(expand=True)

# Nút thoát
exit_button = tk.Button(root, text="Thoát", bg="red", fg="white", command=exit_program, font=("Arial", 14))
exit_button.place(x=380, y=330, width=100, height=40)

# Mở camera
cap1 = cv2.VideoCapture(1)  # Camera 1 (quét mã QR)
cap2 = cv2.VideoCapture(0)  # Camera 2 (hiển thị bình thường)

if not cap1.isOpened():
    print("Không tìm thấy Camera 1")
    cap1 = None
if not cap2.isOpened():
    print("Không tìm thấy Camera 2")
    cap2 = None

# Biến kiểm soát luồng
running = True

# Queue để truyền dữ liệu giữa luồng và giao diện
queue1 = queue.Queue()
queue2 = queue.Queue()

# Tạo luồng cho từng camera
if cap1:
    thread1 = threading.Thread(target=capture_camera, args=(cap1, queue1, True), daemon=True)
    thread1.start()
    update_frame(cam1_label, queue1)

if cap2:
    thread2 = threading.Thread(target=capture_camera, args=(cap2, queue2, False), daemon=True)
    thread2.start()
    update_frame(cam2_label, queue2)

# Chạy giao diện
root.protocol("WM_DELETE_WINDOW", exit_program)
root.mainloop()
