"""
牙齿分割模型训练脚本
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import argparse
import yaml
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from segmentation.model import SegmentationModel
from segmentation.dataset import ToothSegmentationDataset
from common.base_trainer import BaseTrainer
from common.metrics import segmentation_metrics
from common.utils import setup_logger, save_checkpoint


def parse_args():
    parser = argparse.ArgumentParser(description='训练牙齿分割模型')
    parser.add_argument('--config', type=str, default='segmentation/config.yaml',
                        help='配置文件路径')
    parser.add_argument('--resume', type=str, default=None,
                        help='从检查点继续训练')
    parser.add_argument('--gpus', type=str, default='0',
                        help='使用的GPU ID，逗号分隔')
    return parser.parse_args()


def main():
    args = parse_args()
    
    # 加载配置
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    # 设置日志
    logger = setup_logger('segmentation_train', config['training']['log_dir'])
    logger.info(f"加载配置: {args.config}")
    
    # 设置设备
    device = torch.device(f"cuda:{args.gpus.split(',')[0]}" if torch.cuda.is_available() else "cpu")
    logger.info(f"使用设备: {device}")
    
    # 创建数据集
    logger.info("加载数据集...")
    train_dataset = ToothSegmentationDataset(
        data_path=config['data']['train_path'],
        num_points=config['data']['num_points'],
        augment=True
    )
    val_dataset = ToothSegmentationDataset(
        data_path=config['data']['val_path'],
        num_points=config['data']['num_points'],
        augment=False
    )
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=config['training']['batch_size'],
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=config['training']['batch_size'],
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )
    
    logger.info(f"训练样本数: {len(train_dataset)}, 验证样本数: {len(val_dataset)}")
    
    # 创建模型
    logger.info("创建模型...")
    model = SegmentationModel(
        num_classes=config['data']['num_classes'],
        model_type=config['model']['name']
    ).to(device)
    
    # 损失函数
    criterion = nn.CrossEntropyLoss(ignore_index=-1)
    
    # 优化器
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=config['training']['learning_rate'],
        weight_decay=config['training'].get('weight_decay', 1e-4)
    )
    
    # 学习率调度器
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer,
        T_max=config['training']['epochs']
    )
    
    # 创建训练器
    trainer = BaseTrainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=criterion,
        optimizer=optimizer,
        scheduler=scheduler,
        device=device,
        config=config
    )
    
    # 从检查点恢复
    start_epoch = 0
    if args.resume:
        logger.info(f"从检查点恢复: {args.resume}")
        checkpoint = torch.load(args.resume)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint['epoch'] + 1
    
    # 开始训练
    logger.info("开始训练...")
    trainer.train(
        epochs=config['training']['epochs'],
        start_epoch=start_epoch,
        save_dir=config['training']['checkpoint_dir']
    )
    
    logger.info("训练完成！")


if __name__ == '__main__':
    main()
