"""
牙齿分割模型推理脚本
"""

import torch
import argparse
from pathlib import Path
import numpy as np
import sys
sys.path.append(str(Path(__file__).parent.parent))

from segmentation.model import SegmentationModel
from common.utils import load_mesh, save_mesh, visualize_segmentation


def parse_args():
    parser = argparse.ArgumentParser(description='牙齿分割推理')
    parser.add_argument('--model', type=str, required=True,
                        help='模型权重路径')
    parser.add_argument('--input', type=str, default=None,
                        help='输入文件路径')
    parser.add_argument('--input_dir', type=str, default=None,
                        help='输入文件夹路径（批量处理）')
    parser.add_argument('--output', type=str, default='output.obj',
                        help='输出文件路径')
    parser.add_argument('--output_dir', type=str, default='results',
                        help='输出文件夹路径')
    parser.add_argument('--num_points', type=int, default=10000,
                        help='采样点数')
    parser.add_argument('--visualize', action='store_true',
                        help='可视化结果')
    parser.add_argument('--device', type=str, default='cuda',
                        help='计算设备')
    return parser.parse_args()


def inference_single(model, points, device):
    """单个样本推理"""
    model.eval()
    
    with torch.no_grad():
        # 转换为 tensor
        points_tensor = torch.from_numpy(points).float().unsqueeze(0).to(device)
        
        # 推理
        output = model(points_tensor)
        pred = output.argmax(dim=1).cpu().numpy()[0]
    
    return pred


def main():
    args = parse_args()
    
    # 设置设备
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}")
    
    # 加载模型
    print(f"加载模型: {args.model}")
    checkpoint = torch.load(args.model, map_location=device)
    
    model = SegmentationModel(
        num_classes=checkpoint.get('num_classes', 33),
        model_type=checkpoint.get('model_type', 'pointnet++')
    ).to(device)
    
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    # 单个文件推理
    if args.input:
        print(f"处理文件: {args.input}")
        
        # 加载网格
        vertices, faces = load_mesh(args.input)
        
        # 采样点云
        if len(vertices) > args.num_points:
            indices = np.random.choice(len(vertices), args.num_points, replace=False)
            points = vertices[indices]
        else:
            points = vertices
        
        # 推理
        pred_labels = inference_single(model, points, device)
        
        # 保存结果
        save_mesh(args.output, vertices, faces, labels=pred_labels)
        print(f"结果已保存到: {args.output}")
        
        # 可视化
        if args.visualize:
            visualize_segmentation(vertices, pred_labels)
    
    # 批量推理
    elif args.input_dir:
        input_path = Path(args.input_dir)
        output_path = Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 获取所有文件
        files = list(input_path.glob('*.obj')) + list(input_path.glob('*.ply'))
        print(f"找到 {len(files)} 个文件")
        
        for file in files:
            print(f"处理: {file.name}")
            
            # 加载和推理
            vertices, faces = load_mesh(str(file))
            
            if len(vertices) > args.num_points:
                indices = np.random.choice(len(vertices), args.num_points, replace=False)
                points = vertices[indices]
            else:
                points = vertices
            
            pred_labels = inference_single(model, points, device)
            
            # 保存
            output_file = output_path / f"{file.stem}_seg{file.suffix}"
            save_mesh(str(output_file), vertices, faces, labels=pred_labels)
        
        print(f"所有结果已保存到: {args.output_dir}")
    
    else:
        print("请指定 --input 或 --input_dir")


if __name__ == '__main__':
    main()
