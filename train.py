import torch
from ultralytics import YOLO


def get_device():
    # check for nvidia gpu
    if torch.cuda.is_available():
        return 0
    # check for apple silicon
    if torch.backends.mps.is_available():
        return 'mps'
    return 'cpu'


def main():
    device = get_device()
    print(f"running on: {device}")

    # load model
    model = YOLO('yolo11n.pt')

    # start training
    model.train(
        data='dataset/data.yaml',
        epochs=50,
        imgsz=640,
        device=device,
        name='dino_v1',
        exist_ok=True,
        plots=True
    )


if __name__ == '__main__':
    main()
