# Parking Spot Detection

This project detects parking spots in images and videos using YOLOv8.

## Features
- Organize and split datasets for training/validation/testing
- Train YOLOv8 models
- Evaluate and visualize results (mAP, confusion matrix, PR curve)
- Predict on images and videos

## Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download or organize your dataset in the `data/` directory as described below.

## Dataset Structure
```
data/
  raw/
    cos40007_dataset/
      Indoor/Outdoor/
        Images/
        Labels/
  split/
    images/
      train/ val/ test/
    labels/
      train/ val/ test/
```

## Training
- Edit `src/config/data.yaml` to point to your split data.
- Run the training notebook: `notebooks/training.ipynb`

## Evaluation
- Run the evaluation notebook: `notebooks/eval.ipynb`
- mAP and other metrics will be printed and saved.

## Prediction
- Use `notebooks/predict.ipynb` to run predictions on images or videos.

## Notes
- Make sure to adjust paths in the code/notebooks to match your setup.
- For Kaggle datasets, set up your API key as described in the Kaggle docs.

## License
MIT
