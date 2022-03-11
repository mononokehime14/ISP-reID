# encoding: utf-8


import glob
import re
import urllib
import zipfile

import os.path as osp
import os
from PIL import Image
from utils.iotools import mkdir_if_missing
from .bases import BaseValImageDataset

import numpy as np


class OccludedREID(BaseValImageDataset):
    dataset_dir = 'OccludedREID'
    num_pids = 200

    def __init__(self, root='/mnt/data/zhukuan/', pseudo_label_subdir='train_parsing_pseudo_labels', part_num=6, verbose=True, **kwargs):
        super(OccludedREID, self).__init__()
        self.dataset_dir = osp.join(root, self.dataset_dir)
        self.query_dir = osp.join(self.dataset_dir, 'query')
        self.gallery_dir = osp.join(self.dataset_dir, 'gallery')
        self.pseudo_label_subdir = pseudo_label_subdir
        self.pseudo_label_dir = osp.join(self.dataset_dir, self.pseudo_label_subdir)
        self.part_num = part_num
        if not osp.exists(self.pseudo_label_dir):
            os.mkdir(self.pseudo_label_dir)
            
        self._check_before_run()

        query = self._process_test_dir(self.query_dir, relabel=False)
        gallery = self._process_test_dir(self.gallery_dir, relabel=False)

        if verbose:
            print("=> OccludedREID loaded")
            self.print_dataset_statistics(query, gallery)

        self.query = query
        self.gallery = gallery

        self.num_query_pids, self.num_query_imgs = self.get_val_imagedata_info(self.query)
        self.num_gallery_pids, self.num_gallery_imgs = self.get_val_imagedata_info(self.gallery)

    def _check_before_run(self):
        """Check if all files are available before going deeper"""
        if not osp.exists(self.dataset_dir):
            raise RuntimeError("'{}' is not available".format(self.dataset_dir))
        if not osp.exists(self.query_dir):
            raise RuntimeError("'{}' is not available".format(self.query_dir))
        if not osp.exists(self.gallery_dir):
            raise RuntimeError("'{}' is not available".format(self.gallery_dir))
            
    def _process_test_dir(self, dir_path, relabel=False):
        img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
        #pattern = re.compile(r'([-\d]+)_c(\d)')

        pid_container = set()
        for img_path in img_paths:
            #print(img_path)
            pid = int(img_path.split('/')[-1].split('_')[0])
            #print(pid)
            #pid, _ = map(int, pattern.search(img_path).groups())
            pid_container.add(pid)
        pid2label = {pid: label for label, pid in enumerate(pid_container)}

        dataset = []
        for img_path in img_paths:
            pid = int(img_path.split('/')[-1].split('_')[0])
            # pid, camid = map(int, pattern.search(img_path).groups())
            # assert 1 <= camid <= 8
            # camid -= 1  # index starts from 0
            if relabel: pid = pid2label[pid]
            dataset.append((img_path, pid))

        return dataset
