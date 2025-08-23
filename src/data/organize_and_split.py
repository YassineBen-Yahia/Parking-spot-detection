

import os
import shutil
import random
from glob import glob

# Set random seed for reproducibility
random.seed(42)

# Paths
DATA_ROOT = os.path.join('data', 'raw', 'cos40007_dataset')
SPLIT_ROOT = os.path.join('split')
IMAGES_ROOT = os.path.join(SPLIT_ROOT, 'images')
LABELS_ROOT = os.path.join(SPLIT_ROOT, 'labels')

# Remove previous split folders if they exist (optional, for clean rerun)
def remove_dir_if_exists(path):
	if os.path.exists(path):
		shutil.rmtree(path)

remove_dir_if_exists(SPLIT_ROOT)
for sub in ['train', 'val', 'test']:
	os.makedirs(os.path.join(IMAGES_ROOT, sub), exist_ok=True)
	os.makedirs(os.path.join(LABELS_ROOT, sub), exist_ok=True)

# Collect all images and labels
image_exts = ['*.jpg', '*.jpeg', '*.png']
label_exts = ['*.txt', '*.xml', '*.json']  # Adjust as needed

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

if not pairs:
	print("No image-label pairs found. Please check your dataset structure and label extensions.")
	exit(1)

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
		shutil.copy2(img, os.path.join(IMAGES_ROOT, split, os.path.basename(img)))
		shutil.copy2(lbl, os.path.join(LABELS_ROOT, split, os.path.basename(lbl)))

print(f"Total pairs: {n}\nTrain: {len(train_pairs)}, Val: {len(val_pairs)}, Test: {len(test_pairs)}")
print(f"Done. Check the '{SPLIT_ROOT}' directory.")
