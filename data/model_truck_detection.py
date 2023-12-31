#트럭 객체 추출 모델 : facebook/detr-resnet-50

from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image

def model_truck_detection(img, coordinates):

    # you can specify the revision tag if you don't want the timm dependency
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

    inputs = processor(images=img, return_tensors="pt")
    outputs = model(**inputs)

    # convert outputs (bounding boxes and class logits) to COCO API
    # let's only keep detections with score > 0.9
    target_sizes = torch.tensor([img.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.5)[0]

    box_size = 1000000
    #best_score = 0

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):

        box = [round(i, 2) for i in box.tolist()]

        # 번호판을 포함하는 트럭만 추출
        if(coordinates[0] < box[0] or coordinates[1] < box[1] or coordinates[2] > box[2] or coordinates[3] > box[3]) : continue

        # 제일 작은 박스의 트럭 추출
        if(box_size > ((box[2] - box[0]) * (box[3] - box[1]))) :
            box_size = (box[2] - box[0]) * (box[3] - box[1])

            truck_img = img.crop((box[0], box[1], box[2], box[3]))
            truck_img.save('./images/' + 'truck_img' + '.jpg','JPEG')