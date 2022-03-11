# encoding: utf-8


import torch
import numpy as np


def train_collate_fn(batch):
    imgs, pids, _, _, mask_target, _ = zip(*batch)
    pids = torch.tensor(pids, dtype=torch.int64)
    mask_target = torch.tensor(np.array(mask_target), dtype=torch.int64)
    return torch.stack(imgs, dim=0), pids, mask_target
    
def clustering_collate_fn(batch):
    imgs, pids, _, _, _, mask_target_path = zip(*batch)
    return torch.stack(imgs, dim=0), mask_target_path, pids


def val_collate_fn(batch):
    imgs, pids, camids, _, mask_target, _ = zip(*batch)
    return torch.stack(imgs, dim=0), pids, camids

def val_collate_fn_self(batch):
    imgs, pids, img_paths = zip(*batch)
    return torch.stack(imgs, dim=0), pids