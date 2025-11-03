"""
通用训练器基类
"""

import torch
from tqdm import tqdm
from pathlib import Path
import logging


class BaseTrainer:
    """
    通用训练器，所有任务可以继承使用
    """
    
    def __init__(self, model, train_loader, val_loader, criterion,
                 optimizer, scheduler, device, config):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.device = device
        self.config = config
        
        self.logger = logging.getLogger(__name__)
    
    def train_epoch(self):
        """训练一个epoch"""
        self.model.train()
        total_loss = 0.0
        
        pbar = tqdm(self.train_loader, desc="Training")
        for batch_idx, batch_data in enumerate(pbar):
            # 数据移到设备
            batch_data = [x.to(self.device) if torch.is_tensor(x) else x 
                         for x in batch_data]
            
            # 前向传播
            self.optimizer.zero_grad()
            loss = self._compute_loss(batch_data)
            
            # 反向传播
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            
            # 更新进度条
            pbar.set_postfix({'loss': total_loss / (batch_idx + 1)})
        
        return total_loss / len(self.train_loader)
    
    def validate(self):
        """验证"""
        self.model.eval()
        total_loss = 0.0
        
        with torch.no_grad():
            for batch_data in tqdm(self.val_loader, desc="Validating"):
                batch_data = [x.to(self.device) if torch.is_tensor(x) else x 
                             for x in batch_data]
                loss = self._compute_loss(batch_data)
                total_loss += loss.item()
        
        return total_loss / len(self.val_loader)
    
    def _compute_loss(self, batch_data):
        """计算损失，子类可以重写"""
        # 默认实现：假设 batch_data = (inputs, targets)
        if len(batch_data) == 2:
            inputs, targets = batch_data
            outputs = self.model(inputs)
            loss = self.criterion(outputs, targets)
        else:
            # 更复杂的情况，子类需要重写
            raise NotImplementedError("请在子类中实现 _compute_loss 方法")
        
        return loss
    
    def train(self, epochs, start_epoch=0, save_dir='checkpoints'):
        """完整训练流程"""
        save_path = Path(save_dir)
        save_path.mkdir(parents=True, exist_ok=True)
        
        best_val_loss = float('inf')
        
        for epoch in range(start_epoch, epochs):
            self.logger.info(f"\nEpoch {epoch + 1}/{epochs}")
            
            # 训练
            train_loss = self.train_epoch()
            self.logger.info(f"Train Loss: {train_loss:.4f}")
            
            # 验证
            val_loss = self.validate()
            self.logger.info(f"Val Loss: {val_loss:.4f}")
            
            # 学习率调度
            if self.scheduler:
                self.scheduler.step()
            
            # 保存最佳模型
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                self.save_checkpoint(save_path / 'best_model.pth', epoch)
                self.logger.info(f"保存最佳模型 (val_loss: {val_loss:.4f})")
            
            # 定期保存
            if (epoch + 1) % self.config['training'].get('save_frequency', 10) == 0:
                self.save_checkpoint(save_path / f'checkpoint_epoch_{epoch + 1}.pth', epoch)
    
    def save_checkpoint(self, path, epoch):
        """保存检查点"""
        torch.save({
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict() if self.scheduler else None,
        }, path)
