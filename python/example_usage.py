"""
Python AI 模块使用示例
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

# 示例1: 使用分割模型
def example_segmentation():
    """牙齿分割示例"""
    print("="*50)
    print("示例 1: 牙齿分割")
    print("="*50)
    
    from segmentation.model import SegmentationModel
    import torch
    
    # 创建模型
    model = SegmentationModel(num_classes=33, model_type='pointnet++')
    print(f"模型参数量: {sum(p.numel() for p in model.parameters()):,}")
    
    # 模拟输入
    dummy_input = torch.randn(2, 10000, 3)  # batch_size=2, 10000个点, xyz坐标
    
    # 前向传播
    output = model(dummy_input)
    print(f"输入形状: {dummy_input.shape}")
    print(f"输出形状: {output.shape}")  # (2, 33, 10000)
    
    print("✅ 分割模型测试成功！\n")


# 示例2: 使用地标点检测模型
def example_landmarks():
    """地标点检测示例"""
    print("="*50)
    print("示例 2: 地标点检测")
    print("="*50)
    
    from landmarks.model import LandmarkDetectionModel
    import torch
    
    # 创建模型
    model = LandmarkDetectionModel(num_landmarks=10)
    print(f"模型参数量: {sum(p.numel() for p in model.parameters()):,}")
    
    # 模拟输入
    dummy_input = torch.randn(2, 2048, 3)
    
    # 前向传播
    landmarks = model(dummy_input)
    print(f"输入形状: {dummy_input.shape}")
    print(f"输出地标点形状: {landmarks.shape}")  # (2, 10, 3)
    
    print("✅ 地标点检测模型测试成功！\n")


# 示例3: 使用牙轴检测模型
def example_tooth_axis():
    """牙轴检测示例"""
    print("="*50)
    print("示例 3: 牙轴检测")
    print("="*50)
    
    from tooth_axis.model import ToothAxisModel
    import torch
    
    # 创建模型
    model = ToothAxisModel()
    print(f"模型参数量: {sum(p.numel() for p in model.parameters()):,}")
    
    # 模拟输入
    dummy_input = torch.randn(2, 2048, 3)
    
    # 前向传播
    origin, direction = model(dummy_input)
    print(f"输入形状: {dummy_input.shape}")
    print(f"牙轴起点形状: {origin.shape}")  # (2, 3)
    print(f"牙轴方向形状: {direction.shape}")  # (2, 3)
    print(f"方向向量模长: {torch.norm(direction, dim=1)}")  # 应该接近1.0
    
    print("✅ 牙轴检测模型测试成功！\n")


# 示例4: 使用通用工具
def example_utils():
    """通用工具示例"""
    print("="*50)
    print("示例 4: 通用工具")
    print("="*50)
    
    from common.metrics import segmentation_metrics, landmark_metrics, axis_metrics
    import numpy as np
    
    # 分割指标
    pred = np.random.randint(0, 33, 10000)
    target = np.random.randint(0, 33, 10000)
    seg_metrics = segmentation_metrics(pred, target, num_classes=33)
    print(f"分割准确率: {seg_metrics['accuracy']:.4f}")
    print(f"平均 IoU: {seg_metrics['mean_iou']:.4f}")
    
    # 地标点指标
    pred_landmarks = np.random.randn(10, 3)
    gt_landmarks = pred_landmarks + np.random.randn(10, 3) * 0.5
    landmark_metric = landmark_metrics(pred_landmarks, gt_landmarks)
    print(f"平均径向误差: {landmark_metric['mre']:.4f}")
    
    # 牙轴指标
    pred_origin = np.array([0.1, 0.2, 0.3])
    pred_direction = np.array([0.0, 0.0, 1.0])
    gt_origin = np.array([0.15, 0.25, 0.35])
    gt_direction = np.array([0.1, 0.0, 0.99])
    axis_metric = axis_metrics(pred_origin, pred_direction, gt_origin, gt_direction)
    print(f"起点误差: {axis_metric['origin_error']:.4f}")
    print(f"角度误差: {axis_metric['angle_error_deg']:.2f}°")
    
    print("✅ 通用工具测试成功！\n")


if __name__ == '__main__':
    print("\n" + "="*50)
    print("Python AI 模块使用示例")
    print("="*50 + "\n")
    
    try:
        example_segmentation()
        example_landmarks()
        example_tooth_axis()
        example_utils()
        
        print("="*50)
        print("🎉 所有示例运行成功！")
        print("="*50)
        print("\n下一步:")
        print("1. 查看 QUICKSTART.md 了解详细使用方法")
        print("2. 准备你的数据集")
        print("3. 修改配置文件")
        print("4. 开始训练模型！")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("\n提示: 请确保已安装所有依赖:")
        print("  pip install -r requirements.txt")

