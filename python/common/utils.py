"""
通用工具函数
"""

import numpy as np
import logging
from pathlib import Path
import sys


def setup_logger(name, log_dir='logs', level=logging.INFO):
    """设置日志"""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 文件处理器
    file_handler = logging.FileHandler(log_path / f'{name}.log')
    file_handler.setLevel(level)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # 格式化
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def load_mesh(file_path):
    """加载网格文件"""
    vertices = []
    faces = []
    
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                vertices.append(vertex)
            elif line.startswith('f '):
                parts = line.strip().split()
                face = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                faces.append(face)
    
    return np.array(vertices, dtype=np.float32), np.array(faces, dtype=np.int32)


def save_mesh(file_path, vertices, faces, labels=None):
    """保存网格文件"""
    with open(file_path, 'w') as f:
        # 写入顶点
        for i, v in enumerate(vertices):
            if labels is not None:
                f.write(f"v {v[0]} {v[1]} {v[2]} # label: {labels[i]}\n")
            else:
                f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        
        # 写入面
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")


def visualize_segmentation(vertices, labels):
    """可视化分割结果"""
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 为每个标签使用不同颜色
        unique_labels = np.unique(labels)
        colors = plt.cm.tab20(np.linspace(0, 1, len(unique_labels)))
        
        for i, label in enumerate(unique_labels):
            mask = labels == label
            points = vertices[mask]
            ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
                      c=[colors[i]], label=f'Tooth {label}', s=1)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.show()
        
    except ImportError:
        print("需要安装 matplotlib 才能可视化")


def normalize_points(points):
    """归一化点云到单位球"""
    centroid = points.mean(axis=0)
    points = points - centroid
    max_dist = np.max(np.linalg.norm(points, axis=1))
    points = points / (max_dist + 1e-8)
    return points
