import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode  # Để quét mã QR
import time
import threading
import queue
import pyodbc as odbc
import pandas as pd
import traceback
import datetime
import torch
import serial
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'WUANGTRISS\SQLEXPRESS'
DATABASE_NAME = 'QL_Nhap_Kho(DATN)'
directionOfQrCode = ''
connection_string = f"""
    DRIVER={DRIVER_NAME};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes
"""   

try:
    print("Đang kết nối với server ....")
    conn = odbc.connect(connection_string)
except:
    print("Kiểm tra lại cách kết nối nhaa")
    exit() #Thoát khỏi chương trình
else:
    print("Kết nối thành công!")

def exit_program():
    """Thoát khỏi chương trình và giải phóng tài nguyên"""
    global running
    running = False
    if cap1:
        cap1.release()
    # if cap2:
    #     cap2.release()
    conn.close()
    cv2.destroyAllWindows()
    root.destroy()
def export_excel():
    """Xuất dữ liệu ra file Excel (Chức năng mẫu, chưa thực hiện)"""
    print("Xuất Excel")

def statistics():
    """Thực hiện thống kê (Chức năng mẫu, chưa thực hiện)"""
    print("Thống kê")

# Tạo cửa sổ chính
root = tk.Tk()
root.attributes("-fullscreen", True)  # Đặt cửa sổ ở chế độ toàn màn hình
# root.geometry("900x900")  # Thiết lập kích thước cửa sổ là 800x600

# Thêm phím tắt để thoát chương trình bằng phím ESC
root.bind("<Escape>", lambda event: exit_program())
def selectData_dataBase(data):
    # global data_select
    sql_query = f"SELECT * FROM Bang_Tong_Kho Where MaHang = {data}"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        #Lấy dữ liệu từ database
        row = cursor.fetchone()
    except Exception as e:
        print(f"Lỗi lấy dữ liệu: {e}")
        traceback.print_exc()
    else:
        # Kiểm tra xem có dữ liệu được trả về không
        if row is not None:
        # Chuyển đổi dữ liệu thành list và gán vào biến
            data_select = [element for element in row]
            # print('Truy vấn dữ liệu thành công')
    return tuple(data_select)

def insertData(data):
    global conn
    global counter
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_query = ""
    time = str(current_time)
    data=tuple(data)
    data = data + (time,)
    # data.append(time)
    sql_query = f"INSERT INTO Bang_Nhap_Kho (MaHang,TenHang,XuatXu,SoLuongNhap,ThoiGianNhap) VALUES (?,?,?,?,?)"      
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query,data)
    except Exception as e:
        print(f"Lỗi chèn dữ liệu: {e}")
        traceback.print_exc()
    else:
        print(f"Thêm dữ liệu tự động vào Bang_Nhap_Kho thành công")
        cursor.commit()
#  Khởi tạo biến dem, nếu chưa có
dem = 1  # Số thứ tự bắt đầu từ 1

def add_dataBase_to_TreeView(data, tablename):
    """Thêm dữ liệu từ cơ sở dữ liệu vào Treeview."""
    global dem  # Dùng biến toàn cục để đếm số thứ tự
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time = str(current_time)
    
    # Chuyển đổi dữ liệu thành tuple và thêm thời gian vào cuối
    data = tuple(data)  # Đảm bảo data là tuple
    data = (dem,) + data + (time,)  # Thêm thời gian vào cuối dữ liệu

    # print(type(tablename))  # In ra kiểu dữ liệu của tablename (debugging)

    # Thêm dữ liệu vào Treeview với STT tự động
    treeview.insert("", "end", text=str(dem), values=data)

    # Cuộn xuống dòng cuối cùng
    last_item = treeview.get_children()[-1]
    treeview.see(last_item)

    # Cập nhật số thứ tự cho dòng tiếp theo
    dem = dem + 1  # Tăng biến dem lên 1 cho dòng tiếp theo

# Tạo nút "Thoát" với kích thước lớn hơn
exit_button = tk.Button(
    root,
    text="Thoát",
    command=exit_program,
    bg="red",
    fg="white",
    font=("Arial", 16),
    relief="raised",
    bd=3  # Độ dày đường viền
)
# Đặt vị trí nút "Thoát" ở góc dưới bên trái
exit_button.place(relx=0.01, rely=0.99, anchor="sw")

# Tạo frame 1 với viền cố định
frame1 = tk.Frame(root, width=200, height=200, bg="lightblue", bd=4, relief="solid")
frame1.place(x=10, y=10)  # Đặt ở góc trái trên cùng, cách viền 10px
frame1.pack_propagate(False)  # Ngăn frame thay đổi kích thước theo nội dung

# Tạo frame 2 với viền cố định
frame2 = tk.Frame(root, width=200, height=200, bg="lightgreen", bd=4, relief="solid")
frame2.place(x=220, y=10)  # Đặt cạnh frame 1, cách nhau 10px
frame2.pack_propagate(False)  # Ngăn frame thay đổi kích thước theo nội dung

cam1_label = tk.Label(frame2)
cam1_label.pack(expand=True)
cam2_label = tk.Label(frame1)
cam2_label.pack(expand=True)
# Thêm đoạn text giới thiệu
text3 = tk.Label(root, text="Phân loại sản phẩm bằng mã QR", font=("Arial", 22), bg="white", fg="black")
text3.place(x=600, y=30)  # Đặt ngay bên dưới frame 1
# Thêm đoạn text bên dưới frame 1

# Thêm đoạn text bên dưới frame 2
text2 = tk.Label(root, text="Camera Robot", font=("Arial", 12), bg="white", fg="black")
text2.place(x=265, y=220)  # Đặt ngay bên dưới frame 2

# Bảng Treeview
treeview = ttk.Treeview(root)
treeview.place(x=10, y=270, width=800,height=270)
# Ẩn cột #0
treeview.column("#0", width=0, stretch=tk.NO)
treeview.heading("#0", text="")

def change_columns():
    """Hàm thay đổi số cột trong Treeview dựa vào Radiobutton được chọn"""
    # Xóa các cột hiện tại
    for col in treeview["columns"]:
        treeview.heading(col, text="")
        treeview.column(col, width=0)
    
    # Thêm cột mới dựa trên lựa chọn
    if selected_option.get() == 1:
        columns = ("STT", "Mã sản phẩm", "Tên sản phẩm", "Xuất Xứ", "Số lượng", "Thời gian quét")
    else:
        columns = ("STT", "Mã sản phẩm", "Tên sản phẩm", "Xuất Xứ", "Số lượng")
    treeview["columns"] = columns
    
    for col in columns:
        if col == "STT":
            treeview.column(col, width=50, anchor="center")
        elif col == "Mã sản phẩm" or col == "Thời gian quét":
            treeview.column(col, width=150, anchor="center")
        else:
            treeview.column(col, width=100, anchor="center")
        treeview.heading(col, text=col)

    # Xóa dữ liệu cũ trong Treeview
    treeview.delete(*treeview.get_children())

    # Thêm dữ liệu từ cơ sở dữ liệu hoặc mẫu
    if selected_option.get() == 1:
        None
    else:
        # Dữ liệu mẫu cho "Bảng tổng kho"
        try:
            df = pd.read_sql('SELECT * FROM Bang_Tong_Kho', conn)
            # print(df)  # In ra console để kiểm tra dữ liệu

            # Duyệt qua từng dòng của DataFrame và thêm vào Treeview
            for idx, row in df.iterrows():
                treeview.insert("", "end", values=(idx + 1, *row.values))
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu từ cơ sở dữ liệu: {e}")

# Tạo nút "Xuất Excel"
export_button = tk.Button(
    root,
    text="Xuất Excel",
    command=export_excel,
    bg="blue",
    fg="white",
    font=("Arial", 14),
    relief="raised",
    bd=3
)
export_button.place(x=10, y=630)  # Đặt nút ở dưới bảng Treeview, bên trái

# Tạo nút "Thống kê"
statistics_button = tk.Button(
    root,
    text="Thống kê",
    command=statistics,
    bg="green",
    fg="white",
    font=("Arial", 14),
    relief="raised",
    bd=3
)
statistics_button.place(x=150, y=630)  # Đặt nút ở dưới bảng Treeview, bên phải
last_qr_code = []
def process_qr(frame):
    """Xử lý và quét mã QR"""
    global last_qr_code
    qr_codes = decode(frame)
    for qr_code in qr_codes:
        data = qr_code.data.decode('utf-8')
        data_frame = data.split(",")  # Chia dữ liệu vào list
        
        # Truy vấn cơ sở dữ liệu
        df = pd.read_sql('SELECT * FROM Bang_Tong_Kho', conn)
        
        # Kiểm tra nếu mã trong cơ sở dữ liệu
        if data_frame[0].strip() in df['MaHang'].str.strip().values:
            # Mã tồn tại trong kho, hiển thị chữ xanh với "In Stock"
            text_color = (0, 255, 0)  # Màu xanh
            text1 = f'Ma: {data_frame[0]}'
            text2 = 'In Stock'
            if selected_option.get() == 1:
                if data != last_qr_code:  # Chỉ thêm nếu là mã mới
                    last_qr_code = data_frame[0]
                    data_temp = selectData_dataBase(data_frame[0]) # là một tuple
                    data_temp = data_temp[:3] + (1,) + data_temp[3 + 1:] 
                    print(data_temp)
                    insertData(data_temp)
                    add_dataBase_to_TreeView(data_temp,"name_table")
                    
        else:
            # Mã không có trong kho, hiển thị chữ đỏ với "Out of Stock"
            text_color = (0, 0, 255)  # Màu đỏ
            text1 = f'Ma: {data_frame[0]}'
            text2 = 'Out of Stock'

        # Hiển thị thông tin trên ảnh
        point_text1 = (10, 50)  # Vị trí cho chữ Ma
        point_text2 = (10, 100)  # Vị trí cho chữ In Stock / Out of Stock
        frame_text1 = cv2.putText(frame, text=text1, fontFace=cv2.FONT_HERSHEY_PLAIN,
                                  fontScale=2, color=text_color, org=point_text1, thickness=2)
        frame_text2 = cv2.putText(frame, text=text2, fontFace=cv2.FONT_HERSHEY_PLAIN,
                                  fontScale=2, color=text_color, org=point_text2, thickness=2)

        # Thêm thông tin vào bảng Treeview nếu là mã QR mới
        

        # Vẽ khung quanh QR Code
        points = qr_code.polygon
        if len(points) == 4:
            pts = [(point.x, point.y) for point in points]
            pts.append(pts[0])
            for i in range(len(pts) - 1):
                cv2.line(frame, pts[i], pts[i + 1], (0, 255, 0), 2)

    return frame

def capture_camera(camera, queue):
    """Luồng để đọc camera và gửi khung hình qua queue"""
    while running:
        ret, frame = camera.read()
        if ret:
            frame = cv2.resize(frame, (200, 200))
            if qr_mode:
                frame = process_qr(frame)
                print("QR")
            # else:
            #     frame = process_yolo(frame)
            #     print("YoLo")

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
    label.after(20, update_frame, label, queue)


# def read_arduino():
#     """Đọc tín hiệu từ Arduino để chuyển đổi chế độ"""
#     global qr_mode
#     while running:
#         if arduino.in_waiting > 0:
#             data = arduino.readline().decode('utf-8').strip()
#             if data == "1":  # Tín hiệu từ Arduino để chuyển sang QR mode
#                 qr_mode = True
#             elif data == "0":  # Tín hiệu từ Arduino để chuyển sang YOLO mode
#                 qr_mode = False
#         time.sleep(0.1)


# def process_yolo(frame):
#     """Xử lý và nhận diện bằng YOLOv5"""
#     results = yolo_model(frame)
#     detections = results.xyxy[0].cpu().numpy()

#     for *box, conf, cls in detections:
#         x1, y1, x2, y2 = map(int, box)
#         label = f"{yolo_model.names[int(cls)]} {conf:.2f}"
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
#         cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     return frame

# yolo_model = torch.hub.load('yolov5', 'custom', path='best.pt', force_reload=True, source="local")
# .to('cuda')
# Kết nối Arduino qua Serial
arduino_port = "COM11"  # Thay bằng cổng Arduino của bạn
arduino_baudrate = 115200
# try:
#     arduino = serial.Serial(arduino_port, arduino_baudrate, timeout=1)
#     print(f"Đã kết nối với Arduino qua {arduino_port}")
# except Exception as e:
#     print(f"Không thể kết nối với Arduino: {e}")
#     exit()
# Tạo biến lưu trạng thái của Radiobutton
selected_option = tk.IntVar(value=2)

# Radiobuttons
rb1 = tk.Radiobutton(root, text="Bảng nhập kho", variable=selected_option, value=1, command=change_columns)
rb1.place(x=10,y=550)

rb2 = tk.Radiobutton(root, text="Bảng tổng kho", variable=selected_option, value=2, command=change_columns)
rb2.place(x=10,y=580)
# Mở camera
cap1 = cv2.VideoCapture(0)  # Camera 1 (quét mã QR)

# cap2 = cv2.VideoCapture(1)  # Camera 2 (hiển thị bình thường)

if not cap1.isOpened():
    print("Không tìm thấy Camera 1")
    cap1 = None
# Biến kiểm soát luồng
running = True
qr_mode = True  # Mặc định là chế độ quét mã QR

# Queue để truyền dữ liệu giữa luồng và giao diện
queue1 = queue.Queue()

thread1 = threading.Thread(target=capture_camera, args=(cap1, queue1), daemon=True)
thread1.start()
update_frame(cam1_label, queue1)

# Tạo luồng để đọc tín hiệu từ Arduino
# thread_arduino = threading.Thread(target=read_arduino, daemon=True)
# thread_arduino.start()


change_columns()

# Chạy giao diện
root.protocol("WM_DELETE_WINDOW", exit_program)
root.mainloop()
