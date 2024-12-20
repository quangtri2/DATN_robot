import tkinter as tk
from tkinter import ttk

# Hàm chuyển đổi hiển thị giữa hai bảng
def switch_table():
    if selected_table.get() == 1:
        table1.place(x=10, y=50,width=700)
        table2.place_forget()
    else:
        table2.delete(*table2.get_children())  # Xóa dữ liệu hiện tại
        table2.place(x=10, y=50,width=700)
        table1.place_forget()

# Hàm xóa dữ liệu của bảng đang được hiển thị
def clear_table():
    if selected_table.get() == 1:
        for row in table1.get_children():
            table1.delete(row)
    else:
        for row in table2.get_children():
            table2.delete(row)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Treeview Switcher")
root.geometry("800x500")

# Radiobutton để chuyển đổi giữa các bảng
selected_table = tk.IntVar(value=1)
radio1 = tk.Radiobutton(root, text="Table 1", variable=selected_table, value=1, command=switch_table)
radio1.place(x=10, y=10)

radio2 = tk.Radiobutton(root, text="Table 2", variable=selected_table, value=2, command=switch_table)
radio2.place(x=100, y=10)

# Nút xóa dữ liệu
clear_button = tk.Button(root, text="Clear Table", command=clear_table)
clear_button.place(x=200, y=10)

# Tạo bảng Treeview thứ nhất
table1 = ttk.Treeview(root, columns=("STT", "Mã sản phẩm", "Tên sản phẩm", "Xuất Xứ", "Số lượng", "Thời gian quét"), show="headings")
for col in ("STT", "Mã sản phẩm", "Tên sản phẩm", "Xuất Xứ", "Số lượng", "Thời gian quét"):
    table1.heading(col, text=col)
    table1.column(col, width=100)

table1.place(x=10, y=50,width=700)

# Tạo bảng Treeview thứ hai
table2 = ttk.Treeview(root, columns=("STT", "Mã sản phẩm", "Tên sản phẩm", "Xuất Xứ", "Số lượng"), show="headings")
for col in ("STT", "Mã sản phẩm", "Tên sản phẩm", "Xuất Xứ", "Số lượng"):
    table2.heading(col, text=col)
    table2.column(col, width=100)

# Hiển thị cửa sổ chính
root.mainloop()
