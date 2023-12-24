import matplotlib.pyplot as plt
import os
import numpy as np

# Danh sách tên tệp dữ liệu
file_names = ["time_astar.txt", "time_bfs.txt", "time_ids.txt"]

# Danh sách tên tương ứng với mỗi tệp
algorithm_names = ["A*", "BFS", "IDS"]

# Danh sách chứa dữ liệu từ các tệp
all_data = []

# Đọc dữ liệu từ từng tệp và thêm vào danh sách
for file_name in file_names:
    with open(file_name, 'r') as file:
        lines = file.readlines()

    data = [float(line.strip()) for line in lines]
    all_data.append(data)

# Tạo giá trị x từ 15 đến 24 với chi tiết số hơn
x_values = np.linspace(10, 30, num=21)

# Vẽ nhiều đường trên cùng một đồ thị
for i, data in enumerate(all_data):
    plt.plot(x_values, data, marker='o', linestyle='-', linewidth=2, markersize=8, label=algorithm_names[i])

# Thêm tiêu đề và chú thích
plt.title('So sánh thời gian thực thi giữa các thuật toán')
plt.xlabel('Kích thước đầu vào')
plt.ylabel('Thời gian thực thi (s)')
plt.legend()
plt.grid(True)

# Tăng kích thước đồ thị
fig = plt.gcf()
fig.set_size_inches(10, 6)

# Hiển thị đồ thị
plt.show()
