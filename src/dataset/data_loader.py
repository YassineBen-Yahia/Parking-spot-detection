import os
import kagglehub

def download_from_kaggle(dataset, download_path='data/raw'):
    """
    Download a dataset from Kaggle using kagglehub.
    Args:
        dataset (str): Kaggle dataset identifier
        download_path (str): Local directory where the dataset will be copied
    """
    os.makedirs(download_path, exist_ok=True)

    

    try:
        # kagglehub returns the local path to the dataset
        dataset_path = kagglehub.dataset_download(dataset)

        # Optionally copy/move to your custom download_path
        print(f"Dataset available at: {dataset_path}")
        return dataset_path

    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return None


if __name__ == "__main__":
    download_from_kaggle("tarajanebhasker/parking-lot")
