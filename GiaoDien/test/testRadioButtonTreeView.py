import tkinter as tk
from tkinter import ttk
import pyodbc as odbc
import pandas as pd


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

def change_columns():
    """Hàm thay đổi số cột trong Treeview dựa vào Radiobutton được chọn"""
    # Xóa các cột hiện tại
    for col in tree["columns"]:
        tree.heading(col, text="")
        tree.column(col, width=0)
    
    # Thêm cột mới dựa trên lựa chọn
    if selected_option.get() == 1:
        columns = ("STT", "Mã sản phẩm", "Tên sản phẩm", "Xuất Xứ", "Số lượng", "Thời gian quét")
    else:
        columns = ("STT", "Mã sản phẩm", "Tên sản phẩm", "Xuất Xứ", "Số lượng")
    tree["columns"] = columns
    
    for col in columns:
        if col == "STT":
            tree.column(col, width=50, anchor="center")
        elif col == "Mã sản phẩm" or col == "Thời gian quét":
            tree.column(col, width=150, anchor="center")
        else:
            tree.column(col, width=100, anchor="center")
        tree.heading(col, text=col)

    # Xóa dữ liệu cũ trong Treeview
    tree.delete(*tree.get_children())

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
                tree.insert("", "end", values=(idx + 1, *row.values))
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu từ cơ sở dữ liệu: {e}")
# Tạo cửa sổ chính
root = tk.Tk()
root.title("Treeview with Dynamic Columns")
root.geometry("700x400")

# Nhãn tiêu đề
label = tk.Label(root, text="Chọn loại bảng để thay đổi số cột:")
label.pack(anchor="w", pady=5)

# Tạo biến lưu trạng thái của Radiobutton
selected_option = tk.IntVar(value=1)

# Radiobuttons
rb1 = tk.Radiobutton(root, text="Bảng nhập kho", variable=selected_option, value=1, command=change_columns)
rb1.pack(anchor="w")

rb2 = tk.Radiobutton(root, text="Bảng tổng kho", variable=selected_option, value=2, command=change_columns)
rb2.pack(anchor="w")

# Treeview
tree = ttk.Treeview(root)
# tree.pack(expand=True, fill="both")
tree.place(x=20, y=50, width=660, height=300)
# Ẩn cột #0
tree.column("#0", width=0, stretch=tk.NO)
tree.heading("#0", text="")

# Khởi tạo cột ban đầu
change_columns()

# Chạy ứng dụng
root.mainloop()
