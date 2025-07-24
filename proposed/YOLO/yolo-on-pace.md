# PACE Documentation Contribution Template

## Document Metadata
* **Author**: Dylan Herbig 
* **Date Created**: [2025-07-18]
* **Applicable Clusters**: Only utilized on ICE, but also applicable for Phoenix and Hive

## YOLO Model Setup

### Overview
This documentation describes the setup and usage of a YOLOv8-based object detection pipeline used to identify lizard toepads from scanned images. YOLO (You Only Look Once) is a real-time object detection system that is fast, accurate, and well-suited for high-throughput morphometric tasks. This tool is highly relevant to PACE users working in biology, image processing, and machine learning, particularly for research teams digitizing morphological traits at scale. This guide assumes that you have already created a labeled dataset.


### Prerequisites
- Required access/permissions:
  - Active PACE account
  - Allocate computatioanl resources using `salloc` command
- Software dependencies:
  - conda 
  - Python 3.10+ (tested with 3.13)
  - Ultralytics YOLOv11 (`pip install ultralytics`)
  - Pillow (`pip install pillow`)
- Storage requirements:
  - At least 5–10 GB for dataset preparation and model training
  - Fast local storage (e.g., SSD-backed node storage) is recommended
- Other prerequisites:
  - A labeled dataset (images + YOLO-style .txt annotations)
  - Conda environment setup 

### Step-by-Step Instructions

1. Enable `conda` to be able to create and manage language-agnostic virtual environments
   ```bash
   # Install latest version of Miniconda via terminal
   mkdir -p ~/miniconda3
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
   bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
   rm ~/miniconda3/miniconda.sh
   ```
   In case you have a different architecture compared to `x86_64` use `uname -m` to figure out what architecture your system is on. Also refer to this guide for additional information: https://www.anaconda.com/docs/getting-started/miniconda/install#linux

2. Create and activate Conda environment:
   ```bash
   conda create -n yolo11-env python=3.13 -y
   conda activate yolo11-env
   ```

3. Install required packages:
   ```bash
   pip install ultralytics pillow
   ```

4. At this point, your images and `.txt` files should be split and arranged into `train` and `val` folder under `dataset/images/` and `dataset/labels/`

5. Train the YOLO model

   ```bash
   yolo task=detect mode=train model=yolov11n.pt data=custom_data.yaml epochs=50 imgsz=640
   ```
   Parameter Descriptions
   - `task=detect`: Specifies the type of task YOLO should perform. In this case, `detect` means object detection (bounding box prediction). Other options include `segment` (segmentation), `classify` (image classification), etc.
   - `mode=train`: Indicates the operation mode. `train` tells YOLO to train a model from the given data. Other modes include `predict`, `val`, and `export`.
   - `model=yolov11n.pt`: 	Chooses the model architecture and optionally a pretrained weights file to start from. `yolov11n.pt` is the nano version of YOLOv11 — the smallest and fastest, best for quick experiments and resource-constrained environments. Alternatives include `yolov11s.pt` (small), `yolov11m.pt` (medium), etc. More information about current YOLO versions can be found here: https://docs.ultralytics.com/models/#featured-models 
   - `data=custom_data.yaml`: Points to your custom dataset configuration file. This YAML file defines the training/validation folder paths, number of classes (`nc`), and class names.
   - `epochs=50`: The number of times the model will iterate over the entire training dataset. More epochs usually lead to better performance (up to a point), but increase training time.
   - `imgsz=640`: Sets the size (height and width) of input images used during training and validation. All images are resized to this dimension. The default is 640x640. Larger sizes may improve accuracy, but increase GPU memory requirements and training time.

   **Output**: Once successfully trained, your model should be saved under a `runs/detect/model_name` directory

6. After you have successfully trained your model, you can now run inferencing on a new image. You can either create a custom inferencing function from a Python file or from the terminal
   ```bash
   yolo task=detect mode=predict model=runs/detect/tps_yolo_exp4/weights/best.pt source=data/miami_fall_24_jpgs/1001.jpg imgsz=640 save=True
   ```
   Parameter Descriptions:
   - `model`:  Path to your trained model weights 
   - `source`: Path to the image, folder, or video you want to run inference on
   - `save=True`: Save the predicted images with bounding boxes drawn
   
### Configuration Details
1. YOLO `data.yaml` configuration file
   ```yaml
   path: dataset
   train: images/train
   val: images/val
   nc: 3
   names: ["toepad", "toe", "ruler"]
   ```

2. Parameter Descriptions
   - `path`: Base directory of the dataset
   - `train`, `val`: Relative paths to training and validation image folders
   - `nc`: Number of classes (3 for toepads)
   - `names`: List of class names

3. More detailed configuration settings can be found here: https://docs.ultralytics.com/usage/cfg/

### Troubleshooting

#### Common Issue 1
**Error Message:**
```
PIL.Image.DecompressionBombError: Image size (199042800 pixels) exceeds limit of 178956970 pixels
```

**Resolution:**
1. Ensure the input image resolution is within reasonable limits before passing to YOLO.
2. Resize extremely large images or adjust `Image.MAX_IMAGE_PIXELS`:
    ```python
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    ```

### Storage and Resource Considerations
- Disk Space Requirements:
  - Temporary storage: 5-10 GB
  - Permanent storage: Optional, depending on output volume
- Memory Usage:
  - Minimum: 4 GB RAM
  - Recommended: 16+ GB RAM for large batch training
- CPU Requirements:
  - Minimum cores: 2 cores
  - Optimal performance: 8+ cores or GPU-enabled compute node
- Quota Impact:
  - High read/write I/O during training. Avoid running on shared `/home` paths.

### Directory Structure
```
project/
├── dataset/
│   └── images/
│       └── train/
│       └── val/
│   └── labels/
│       └── train/
│       └── val/
├── config/
│   └── [configuration files]
└── data/
    └── [data files]
```

### Additional Resources
- Internal PACE Documentation for accessing additional computational resources:
  - https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042096
- External Resources:
  - YOLO: https://www.ultralytics.com/yolo

### Complete Working Example
```bash
# Allocate computational resources for training your model
salloc -N1 --ntasks-per-node=4 -t8:00:00 --gres=gpu:H200:1

# Activate conda environment
conda activate yolo11-env

# Assumming all dependencies have been installed via pip, train your model
yolo task=detect mode=train model=yolov11n.pt data=custom_data.yaml epochs=50 imgsz=640

# Run inference
python yolo_predict.py
```

Expected workflow and output:
```
✅ Dataset prepared at: dataset
   Images: 2100 | Train: 1680 | Val: 420
Predicting with YOLOv11...
Predicted boxes: tensor([[x1, y1, x2, y2], ...])
```

**NOTE**: You may need to fine-tune the imgsz and batch parameters depending on GPU memory availability.

**WARNING**: Make sure your input `.jpg` files and `.txt` labels are correctly matched and formatted in YOLO format (class_id center_x center_y width height, all normalized).

### Version Information
- Software version documented: YOLOv11 (Ultralytics 8.3.168)
- Last tested on PACE: [2025-07-18]
- Compatible PACE environments: ICE (with Conda and Python 3.10+)
