import tkinter as tk
from tkinter import messagebox

# 全局变量
board = [[0 for _ in range(15)] for _ in range(15)]  # 15x15 棋盘，0:空，1:黑，2:白
record_black = []  # 黑棋落子记录（棋子编号）
record_white = []  # 白棋落子记录（棋子编号）
rec = []  # 总落子记录（防重复）
current_turn = 1  # 1:黑棋回合，2:白棋回合
game_over = False

# 启动界面
def show_start_page():
    start_root = tk.Toplevel(root)
    start_root.title("Game Start")
    start_root.geometry("200x100")
    tk.Button(start_root, text="Start", command=lambda: [start_root.destroy(), init_game()]).pack(pady=20)
    tk.Button(start_root, text="Quit", command=root.quit).pack()

# 初始化游戏界面
def init_game():
    global game_over, current_turn, board, record_black, record_white, rec
    # 重置游戏状态
    game_over = False
    current_turn = 1
    board = [[0 for _ in range(15)] for _ in range(15)]
    record_black = []
    record_white = []
    rec = []

    game_root = tk.Toplevel(root)
    game_root.title("五子棋")
    game_root.geometry("640x640")

    canvas = tk.Canvas(game_root, width=600, height=600, bg="#D3D3D3")
    canvas.pack()

    # 绘制 15x15 棋盘
    for i in range(15):
        canvas.create_line(20, 20 + i * 40, 580, 20 + i * 40, width=1)
        canvas.create_line(20 + i * 40, 20, 20 + i * 40, 580, width=1)

    # 精准落子判定：计算最近交叉点
    def get_piece_id(x, y):
        col = round((x - 20) / 40)
        row = round((y - 20) / 40)
        if 0 <= row < 15 and 0 <= col < 15:
            return row * 15 + col  # 棋子编号 = 行×15 + 列
        return -1

    # 检查五子连珠
    def check_win(record):
        for piece_id in record:
            row, col = piece_id // 15, piece_id % 15
            # 检查四个方向
            directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
            for dr, dc in directions:
                count = 0
                for step in range(-4, 5):
                    r = row + dr * step
                    c = col + dc * step
                    if 0 <= r < 15 and 0 <= c < 15:
                        if (r * 15 + c) in record:
                            count += 1
                            if count >= 5:
                                return True
                        else:
                            count = 0
        return False

    # 黑棋落子（左键）
    def callback1(event):
        global current_turn, game_over
        if game_over or current_turn != 1:
            return
        piece_id = get_piece_id(event.x, event.y)
        if piece_id != -1 and piece_id not in rec:
            # 记录落子
            record_black.append(piece_id)
            rec.append(piece_id)
            row, col = piece_id // 15, piece_id % 15
            # 绘制黑棋
            canvas.create_oval(
                20 + col * 40 - 18, 20 + row * 40 - 18,
                20 + col * 40 + 18, 20 + row * 40 + 18,
                fill="black"
            )
            # 检查胜负
            if check_win(record_black):
                messagebox.showinfo("Game Over", "Black wins!")
                game_over = True
                game_root.destroy()
            else:
                current_turn = 2  # 切换到白棋回合

    # 白棋落子（右键）
    def callback2(event):
        global current_turn, game_over
        if game_over or current_turn != 2:
            return
        piece_id = get_piece_id(event.x, event.y)
        if piece_id != -1 and piece_id not in rec:
            # 记录落子
            record_white.append(piece_id)
            rec.append(piece_id)
            row, col = piece_id // 15, piece_id % 15
            # 绘制白棋
            canvas.create_oval(
                20 + col * 40 - 18, 20 + row * 40 - 18,
                20 + col * 40 + 18, 20 + row * 40 + 18,
                fill="white", outline="black"
            )
            # 检查胜负
            if check_win(record_white):
                messagebox.showinfo("Game Over", "White wins!")
                game_over = True
                game_root.destroy()
            else:
                current_turn = 1  # 切换到黑棋回合
    # 绑定鼠标事件
    canvas.bind("<Button-1>", callback1)  # 左键黑棋
    canvas.bind("<Button-3>", callback2)  # 右键白棋


# 主程序
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_start_page()
    root.mainloop()