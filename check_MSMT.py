import glob
import re

import os.path as osp

def _process_dir(dir_path, list_path, second_list_path=None):
    with open(list_path, 'r') as txt:
        lines = txt.readlines()
    dataset = []
    pid_container = set()
    count_disc = {}
    for img_idx, img_info in enumerate(lines):
        img_path, pid = img_info.split(' ')
        pid = int(pid)  # no need to relabel
        camid = int(img_path.split('_')[2])
        img_path = osp.join(dir_path, img_path)
        dataset.append((img_path, pid, camid))
        pid_container.add(pid)
        if pid in count_disc:
            count_disc[pid]+=1
        else:
            count_disc[pid] = 1

    # check if pid starts from 0 and increments with 1
    for idx, pid in enumerate(pid_container):
        assert idx == pid, "See code comment for explanation"
    
    if second_list_path:
        with open(second_list_path, 'r') as txt:
            lines = txt.readlines()
        for img_idx, img_info in enumerate(lines):
            img_path, pid = img_info.split(' ')
            pid = int(pid)  # no need to relabel
            camid = int(img_path.split('_')[2])
            img_path = osp.join(dir_path, img_path)
            dataset.append((img_path, pid, camid))
            pid_container.add(pid)
            if pid in count_disc:
                count_disc[pid]+=1
            else:
                count_disc[pid] = 1
        # check if pid starts from 0 and increments with 1
        for idx, pid in enumerate(pid_container):
            assert idx == pid, "See code comment for explanation"

    return dataset, count_disc

def _process_v1_dir(dir_path):
    img_paths = glob.glob(osp.join(dir_path, '*.jpg'))

    pid_container = set()
    dataset = []
    count = 0
    count_disc = {}
    for img_path in img_paths:
        temp = img_path.split('/')[-1].split('.')[0]
        pid, camid, img_id = temp.split('_')
        pid = int(pid)
        camid = int(camid[1:])
        dataset.append((img_path, pid, camid))
        pid_container.add(pid)
        if pid in count_disc:
            count_disc[pid]+=1
        else:
            count_disc[pid] = 1
        count += 1
    # check if pid starts from 0 and increments with 1
    for idx, pid in enumerate(pid_container):
        assert idx == pid, "See code comment for explanation"
    print(f"v1 count {count}")
    return dataset, count_disc

def get_imagedata_info(data):
        pids, cams = [], []
        for _, pid, camid in data:
            pids += [pid]
            cams += [camid]
        pids = set(pids)
        cams = set(cams)
        num_pids = len(pids)
        num_cams = len(cams)
        num_imgs = len(data)
        return num_pids, num_imgs, num_cams

def print_dataset_statistics(train, query, gallery):
        num_train_pids, num_train_imgs, num_train_cams = get_imagedata_info(train)
        num_query_pids, num_query_imgs, num_query_cams = get_imagedata_info(query)
        num_gallery_pids, num_gallery_imgs, num_gallery_cams = get_imagedata_info(gallery)

        print("Dataset statistics:")
        print("  ----------------------------------------")
        print("  subset   | # ids | # images | # cameras")
        print("  ----------------------------------------")
        print("  train    | {:5d} | {:8d} | {:9d}".format(num_train_pids, num_train_imgs, num_train_cams))
        print("  query    | {:5d} | {:8d} | {:9d}".format(num_query_pids, num_query_imgs, num_query_cams))
        print("  gallery  | {:5d} | {:8d} | {:9d}".format(num_gallery_pids, num_gallery_imgs, num_gallery_cams))
        print("  ----------------------------------------")

if __name__ == '__main__':
    root='/home/Dataset/ReID/Person_ReID/'
    dataset_dir = 'MSMT17_V2'
    dataset_dir = osp.join(root, dataset_dir)
    train_dir = osp.join(dataset_dir, 'mask_train_v2')
    test_dir = osp.join(dataset_dir, 'mask_test_v2')
    list_train_path = osp.join(dataset_dir, 'list_train.txt')
    list_val_path = osp.join(dataset_dir, 'list_val.txt')
    list_query_path = osp.join(dataset_dir, 'list_query.txt')
    list_gallery_path = osp.join(dataset_dir, 'list_gallery.txt')
    if not osp.exists(dataset_dir):
        raise RuntimeError("'{}' is not available".format(dataset_dir))
    if not osp.exists(train_dir):
        raise RuntimeError("'{}' is not available".format(train_dir))
    if not osp.exists(test_dir):
        raise RuntimeError("'{}' is not available".format(test_dir))

    train,train_disc2 = _process_dir(train_dir, list_train_path, list_val_path)
    #val, num_val_pids, num_val_imgs = self._process_dir(self.train_dir, self.list_val_path)
    query,query_disc = _process_dir(test_dir, list_query_path)
    gallery,gallery_disc = _process_dir(test_dir, list_gallery_path)
    print("=> MSMT17_V2 loaded")
    print_dataset_statistics(train, query, gallery)

    dataset_dir = 'MSMT17_V1'
    dataset_dir = osp.join(root, dataset_dir)
    train_dir = osp.join(dataset_dir, 'bounding_box_train')
    query_dir = osp.join(dataset_dir, 'query')
    gallery_dir = osp.join(dataset_dir, 'bounding_box_test')
    if not osp.exists(dataset_dir):
        raise RuntimeError("'{}' is not available".format(dataset_dir))
    if not osp.exists(train_dir):
        raise RuntimeError("'{}' is not available".format(train_dir))
    if not osp.exists(query_dir):
        raise RuntimeError("'{}' is not available".format(query_dir))
    if not osp.exists(gallery_dir):
        raise RuntimeError("'{}' is not available".format(gallery_dir))

    train1, train_disc1 = _process_v1_dir(train_dir)
    query1,query_disc1 = _process_v1_dir(query_dir)
    gallery1,gallery_disc1 = _process_v1_dir(gallery_dir)

    for key in train_disc1.keys():
        if key not in train_disc2:
            print(f"ID {key} is in v1 but not in v2.")
        else:
            if train_disc2[key] != train_disc1[key]:
                print(f"ID {key} has {train_disc1[key]} images in v1 but has {train_disc2[key]} images in v2.")

    print("=> MSMT17_V1 loaded")
    print_dataset_statistics(train1, query1, gallery1)


        

