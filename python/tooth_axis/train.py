"""
牙轴检测模型训练
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import argparse
import yaml
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from tooth_axis.model import ToothAxisModel
from tooth_axis.dataset import ToothAxisDataset
from common.base_trainer import BaseTrainer
from common.utils import setup_logger


def parse_args():
    parser = argparse.ArgumentParser(description='训练牙轴检测模型')
    parser.add_argument('--config', type=str, default='tooth_axis/config.yaml')
    parser.add_argument('--resume', type=str, default=None)
    parser.add_argument('--gpus', type=str, default='0')
    return parser.parse_args()


def main():
    args = parse_args()
    
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    device = torch.device(f"cuda:{args.gpus.split(',')[0]}" if torch.cuda.is_available() else "cpu")
    logger = setup_logger('tooth_axis_train', config['training']['log_dir'])
    
    # 数据集
    train_dataset = ToothAxisDataset(config['data']['train_path'], augment=True)
    val_dataset = ToothAxisDataset(config['data']['val_path'], augment=False)
    
    train_loader = DataLoader(train_dataset, batch_size=config['training']['batch_size'],
                             shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=config['training']['batch_size'],
                           shuffle=False, num_workers=4)
    
    # 模型
    model = ToothAxisModel(backbone=config['model']['backbone']).to(device)
    
    # 损失函数：Angular loss for direction + MSE for origin
    criterion = nn.MSELoss()
    
    optimizer = torch.optim.Adam(model.parameters(), 
                                lr=config['training']['learning_rate'])
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, 
                                                           T_max=config['training']['epochs'])
    
    trainer = BaseTrainer(model, train_loader, val_loader, criterion,
                         optimizer, scheduler, device, config)
    
    trainer.train(epochs=config['training']['epochs'],
                 save_dir=config['training']['checkpoint_dir'])


if __name__ == '__main__':
    main()
