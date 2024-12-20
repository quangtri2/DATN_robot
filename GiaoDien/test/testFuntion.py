import tkinter as tk
def reset_squares(squares):
    for square in squares:
        square.config(bg="white")  # Đặt màu nền về trắng
# Hàm để làm sáng các ô nhỏ trong mỗi hình vuông lớn
def highlight_squares(square, is_range, indices):
    reset_squares(square)
    for i in range(1, 5):
        if is_range and i <= indices[0]:
            square[i-1].config(bg="yellow")  # Sáng tất cả ô từ 1 đến số trong indices[0]
        elif not is_range and i in indices:
            square[i-1].config(bg="yellow")  # Sáng các ô tương ứng với các số trong indices

# Hàm nhận giá trị và cập nhật giao diện
def update_interface(square_id, is_range, indices):
    if square_id == "001":
        highlight_squares(squares_A, is_range, indices)
    elif square_id == "002":
        highlight_squares(squares_B, is_range, indices)
    elif square_id == "003":
        highlight_squares(squares_C, is_range, indices)

# Tạo cửa sổ chính
root = tk.Tk()
root.geometry("600x600")  # Đặt kích thước cửa sổ thành 600x600

frame_cm = tk.Frame(root)
frame_cm.place(x=200,y=100)
# Tạo Label tiêu đề
label = tk.Label(frame_cm, text="Giám sát", font=("Arial", 16), fg="blue")
label.grid(row=0, column=0, columnspan=2, pady=10)  # Đặt Label ở hàng đầu tiên, giữa 2 cột

# Tạo frame cho mỗi hình vuông lớn A, B, C
frame_A = tk.Frame(frame_cm)
frame_A.grid(row=1, column=0, padx=10, pady=10)

frame_B = tk.Frame(frame_cm)
frame_B.grid(row=1, column=1, padx=10, pady=10)

frame_C = tk.Frame(frame_cm)
frame_C.grid(row=1, column=2, padx=10, pady=10)

# Tạo các ô vuông nhỏ trong mỗi hình vuông lớn
squares_A = [tk.Button(frame_A, text=str(i), width=10, height=5) for i in range(1, 5)]
for i, square in enumerate(squares_A):
    square.grid(row=i//2, column=i%2)

squares_B = [tk.Button(frame_B, text=str(i), width=10, height=5) for i in range(1, 5)]
for i, square in enumerate(squares_B):
    square.grid(row=i//2, column=i%2)

squares_C = [tk.Button(frame_C, text=str(i), width=10, height=5) for i in range(1, 5)]
for i, square in enumerate(squares_C):
    square.grid(row=i//2, column=i%2)

# Gắn các phím với các chức năng
root.bind('<m>', lambda event: update_interface("001", False, [1, 2, 3]))
root.bind('<x>', lambda event: update_interface("002", True, [3]))
root.bind('<c>', lambda event: update_interface("003", False, [1, 2, 4]))
root.bind('<v>', lambda event: update_interface("001", False, [2]))

root.mainloop()
