"""
生成 矩阵转置动态图.md 中使用的动图 transpose_animation.gif

对应张量：shape [2, 2, 3, 4]，可以理解为一个 2x2 的"元矩阵"，
每个元素本身是一个 3x4 的小块（block）：

    元矩阵 = [ block(1,2,3)    block(4,5,6)  ]
             [ block(7,8,9)    block(10,11,12)]

x.transpose_(1, 0) 交换 dim0(组) 和 dim1(块)，效果等价于把这个 2x2
元矩阵做转置：对角线上的两个块（1,2,3 和 10,11,12）位置不变，
非对角线的两个块（4,5,6 和 7,8,9）互换位置。
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# 每个 block 的内容：3 行，每行是一个常数（重复 4 次），只展示这个代表值
BLOCKS = {
    (0, 0): [1, 2, 3],
    (0, 1): [4, 5, 6],
    (1, 0): [7, 8, 9],
    (1, 1): [10, 11, 12],
}

COLORS = {
    (0, 0): "#4C72B0",  # 对角线，不动
    (1, 1): "#4C72B0",  # 对角线，不动
    (0, 1): "#DD8452",  # 非对角线，会互换
    (1, 0): "#55A868",  # 非对角线，会互换
}

CELL_W, CELL_H = 3.2, 2.2
GAP = 0.5


def cell_origin(row, col):
    """meta-matrix 里 (row, col) 格子的左下角坐标"""
    x0 = col * (CELL_W + GAP)
    y0 = (1 - row) * (CELL_H + GAP)
    return x0, y0


def draw_block(ax, xy, values, color, label, alpha=1.0):
    x0, y0 = xy
    rect = patches.FancyBboxPatch(
        (x0, y0), CELL_W, CELL_H,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.6, edgecolor=color, facecolor=color, alpha=0.18 * alpha + 0.02,
    )
    ax.add_patch(rect)
    rect2 = patches.FancyBboxPatch(
        (x0, y0), CELL_W, CELL_H,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.8, edgecolor=color, facecolor="none", alpha=alpha,
    )
    ax.add_patch(rect2)
    ax.text(x0 + CELL_W / 2, y0 + CELL_H - 0.32, label,
             ha="center", va="top", fontsize=10, color=color, alpha=alpha, weight="bold")
    for i, v in enumerate(values):
        row_text = f"[{v}, {v}, {v}, {v}]"
        ax.text(x0 + CELL_W / 2, y0 + CELL_H - 0.75 - i * 0.5, row_text,
                 ha="center", va="top", fontsize=10.5, color="#222222", alpha=alpha,
                 family="monospace")


def smoothstep(t):
    return t * t * (3 - 2 * t)


def path_point(waypoints, t):
    """在若干个 waypoint 间分段插值（每段用 smoothstep 缓动），t in [0,1]"""
    n = len(waypoints) - 1
    seg = min(int(t * n), n - 1)
    local_t = smoothstep(t * n - seg)
    a = np.array(waypoints[seg])
    b = np.array(waypoints[seg + 1])
    return a + (b - a) * local_t


N_HOLD = 8
N_MOVE = 24
N_END_HOLD = 12
frames = N_HOLD + N_MOVE + N_END_HOLD

fig, ax = plt.subplots(figsize=(10.5, 7.6))


MARGIN = 3.6


def setup_axes():
    ax.clear()
    ax.set_xlim(-MARGIN, 2 * (CELL_W + GAP) - GAP + MARGIN)
    ax.set_ylim(-MARGIN, 2 * (CELL_H + GAP) - GAP + MARGIN)
    ax.set_aspect("equal")
    ax.axis("off")


def title_for(frame):
    if frame < N_HOLD:
        return "转置前  x.shape = [2, 2, 3, 4]\n(dim0=组, dim1=块, dim2=行, dim3=列，dim2/dim3 省略为一个代表值)"
    elif frame < N_HOLD + N_MOVE:
        return "x.transpose_(1, 0)  交换 dim0(组) 和 dim1(块)\n非对角线的两个块互换位置，对角线两个块不动"
    else:
        return "转置后  x.shape = [2, 2, 3, 4]\ny[b][a] = x[a][b]（组、块互换，块内部 行/列 完全不变）"


# 四个块的中心点
center_00 = np.array(cell_origin(0, 0)) + (CELL_W / 2, CELL_H / 2)
center_01 = np.array(cell_origin(0, 1)) + (CELL_W / 2, CELL_H / 2)
center_10 = np.array(cell_origin(1, 0)) + (CELL_W / 2, CELL_H / 2)
center_11 = np.array(cell_origin(1, 1)) + (CELL_W / 2, CELL_H / 2)

LANE = CELL_W * 0.95

# 块(0,1) [右上, 4,5,6] 走"左侧外圈"绕到 (1,0) [左下]，
# 块(1,0) [左下, 7,8,9] 走"右侧外圈"绕到 (0,1) [右上]，
# 两条路线分别贴左、右两侧从外部绕开，既不穿过对角线上静止的两个块，两条路线也不会互相交叉
path_01 = [
    tuple(center_01),
    (center_00[0] - LANE, center_01[1]),
    (center_00[0] - LANE, center_10[1]),
    tuple(center_10),
]
path_10 = [
    tuple(center_10),
    (center_11[0] + LANE, center_10[1]),
    (center_11[0] + LANE, center_01[1]),
    tuple(center_01),
]


def update(frame):
    setup_axes()
    ax.set_title(title_for(frame), fontsize=12, pad=14)

    if frame < N_HOLD:
        t = 0.0
    elif frame < N_HOLD + N_MOVE:
        t = (frame - N_HOLD) / (N_MOVE - 1)
    else:
        t = 1.0

    # 对角线的两个块：全程不动
    draw_block(ax, cell_origin(0, 0), BLOCKS[(0, 0)], COLORS[(0, 0)], "x[0][0]  →  y[0][0]  (不变)")
    draw_block(ax, cell_origin(1, 1), BLOCKS[(1, 1)], COLORS[(1, 1)], "x[1][1]  →  y[1][1]  (不变)")

    # 非对角线的两个块：分别沿左、右两条外圈路线互换位置
    center_now_01 = path_point(path_01, t)
    center_now_10 = path_point(path_10, t)
    pos_01 = (center_now_01[0] - CELL_W / 2, center_now_01[1] - CELL_H / 2)
    pos_10 = (center_now_10[0] - CELL_W / 2, center_now_10[1] - CELL_H / 2)

    label_01 = "x[0][1] (4,5,6)" if t < 0.999 else "y[1][0] = x[0][1]"
    label_10 = "x[1][0] (7,8,9)" if t < 0.999 else "y[0][1] = x[1][0]"

    draw_block(ax, pos_01, BLOCKS[(0, 1)], COLORS[(0, 1)], label_01)
    draw_block(ax, pos_10, BLOCKS[(1, 0)], COLORS[(1, 0)], label_10)

    return []


from matplotlib.animation import FuncAnimation, PillowWriter

anim = FuncAnimation(fig, update, frames=frames, interval=90, blit=False)
out_path = "/inaction_01_pytorch/chatper_01/transpose_animation.gif"
anim.save(out_path, writer=PillowWriter(fps=11))
print("saved", out_path)
