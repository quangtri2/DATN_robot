import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import threading
import queue
import torch
import serial
import time
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

def exit_program():
    """Thoát khỏi chương trình và giải phóng tài nguyên"""
    global running
    running = False
    if cap:
        cap.release()
    cv2.destroyAllWindows()
    root.destroy()

def read_arduino():
    """Đọc tín hiệu từ Arduino để chuyển đổi chế độ"""
    global qr_mode
    while running:
        if arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip()
            if data == "1":  # Tín hiệu từ Arduino để chuyển sang QR mode
                qr_mode = True
            elif data == "0":  # Tín hiệu từ Arduino để chuyển sang YOLO mode
                qr_mode = False
        time.sleep(0.1)

def process_qr(frame):
    """Xử lý và quét mã QR"""
    global last_qr_code
    qr_codes = decode(frame)
    for qr_code in qr_codes:
        data = qr_code.data.decode('utf-8')
        if data != last_qr_code:  # Chỉ thêm nếu là mã mới
            last_qr_code = data
            # Hiển thị dữ liệu vào bảng Treeview
            current_time = time.strftime("%H:%M:%S")  # Lấy thời gian hiện tại
            treeview.insert("", "end", values=(len(treeview.get_children()) + 1, data, "Sản phẩm XYZ", current_time))

        # Vẽ khung xung quanh QR Code
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

def process_yolo(frame):
    """Xử lý và nhận diện bằng YOLOv5"""
    results = yolo_model(frame)
    detections = results.xyxy[0].cpu().numpy()

    for *box, conf, cls in detections:
        x1, y1, x2, y2 = map(int, box)
        label = f"{yolo_model.names[int(cls)]} {conf:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return frame

def capture_camera(camera, queue):
    """Luồng để đọc camera và gửi khung hình qua queue"""
    while running:
        ret, frame = camera.read()
        if ret:
            frame = cv2.flip(frame, 0)
            frame = cv2.resize(frame, (640, 480))
            if qr_mode:
                frame = process_qr(frame)
            else:
                frame = process_yolo(frame)
            queue.put(frame)
        time.sleep(0.03)  # Giảm tần suất xử lý (khoảng 30 FPS)

def update_frame(label, queue):
    """Cập nhật khung hình từ queue lên giao diện Tkinter"""
    if not queue.empty():
        frame = queue.get()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        label.imgtk = img
        label.configure(image=img)
    label.after(10, update_frame, label, queue)

# Khởi tạo YOLOv5
# yolo_model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
yolo_model = torch.hub.load('yolov5', 'custom', path='best.pt', force_reload=True, source="local")
# .to('cuda')
# Kết nối Arduino qua Serial
arduino_port = "COM11"  # Thay bằng cổng Arduino của bạn
arduino_baudrate = 115200
try:
    arduino = serial.Serial(arduino_port, arduino_baudrate, timeout=1)
    print(f"Đã kết nối với Arduino qua {arduino_port}")
except Exception as e:
    print(f"Không thể kết nối với Arduino: {e}")
    exit()

# Tạo cửa sổ chính
root = tk.Tk()
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda event: exit_program())

# Khung camera
cam_label = tk.Label(root)
cam_label.pack(expand=True, fill="both")

# Bảng Treeview
columns = ("STT", "Mã sản phẩm", "Tên sản phẩm", "Thời gian quét")
treeview = ttk.Treeview(root, columns=columns, show="headings", height=15)
treeview.pack(side=tk.BOTTOM, fill="x")
for col in columns:
    treeview.heading(col, text=col)

# Biến kiểm soát
qr_mode = True  # Mặc định là chế độ quét mã QR
running = True
last_qr_code = ""

# Mở camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Không tìm thấy Camera!")
    exit()

# Queue để truyền dữ liệu giữa luồng và giao diện
frame_queue = queue.Queue()

# Tạo luồng cho camera
thread_camera = threading.Thread(target=capture_camera, args=(cap, frame_queue), daemon=True)
thread_camera.start()
update_frame(cam_label, frame_queue)

# Tạo luồng để đọc tín hiệu từ Arduino
thread_arduino = threading.Thread(target=read_arduino, daemon=True)
thread_arduino.start()

# Chạy giao diện
root.protocol("WM_DELETE_WINDOW", exit_program)
root.mainloop()
