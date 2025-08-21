import os
import shutil
import random
from glob import glob

# Set random seed for reproducibility
random.seed(42)

# Paths
DATA_ROOT = 'data/raw/cos40007_dataset'
ALL_IMAGES = 'data/all_images'
ALL_LABELS = 'data/all_labels'
SPLIT_ROOT = 'data/split'

# Create output directories
os.makedirs(ALL_IMAGES, exist_ok=True)
os.makedirs(ALL_LABELS, exist_ok=True)
for split in ['train', 'val', 'test']:
    os.makedirs(os.path.join(SPLIT_ROOT, split, 'images'), exist_ok=True)
    os.makedirs(os.path.join(SPLIT_ROOT, split, 'labels'), exist_ok=True)

# Collect all images and labels
image_exts = ['*.jpg', '*.jpeg', '*.png']
label_exts = ['*.txt']  # Adjust as needed

def collect_files(root, subfolder, exts):
    files = []
    for ext in exts:
        files.extend(glob(os.path.join(root, '**', subfolder, ext), recursive=True))
    return files

all_images = collect_files(DATA_ROOT, 'Images', image_exts)
all_labels = collect_files(DATA_ROOT, 'Labels', label_exts)

# Map images to labels by filename (without extension)
def get_basename(path):
    return os.path.splitext(os.path.basename(path))[0]

label_map = {get_basename(l): l for l in all_labels}

pairs = []
for img in all_images:
    base = get_basename(img)
    if base in label_map:
        pairs.append((img, label_map[base]))

# Copy all images and labels to unified folders
for img, lbl in pairs:
    shutil.copy(img, os.path.join(ALL_IMAGES, os.path.basename(img)))
    shutil.copy(lbl, os.path.join(ALL_LABELS, os.path.basename(lbl)))

# Shuffle and split
random.shuffle(pairs)
n = len(pairs)
train_end = int(0.7 * n)
val_end = int(0.85 * n)
train_pairs = pairs[:train_end]
val_pairs = pairs[train_end:val_end]
test_pairs = pairs[val_end:]

splits = {'train': train_pairs, 'val': val_pairs, 'test': test_pairs}

for split, split_pairs in splits.items():
    for img, lbl in split_pairs:
        shutil.copy(img, os.path.join(SPLIT_ROOT, split, 'images', os.path.basename(img)))
        shutil.copy(lbl, os.path.join(SPLIT_ROOT, split, 'labels', os.path.basename(lbl)))

print(f"Total pairs: {n}\nTrain: {len(train_pairs)}, Val: {len(val_pairs)}, Test: {len(test_pairs)}")
print(f"Done. Check the '{SPLIT_ROOT}' directory.")
