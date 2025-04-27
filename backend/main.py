from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from PIL import Image
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

class Dimensions(BaseModel):
    width: int
    height: int

class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int

class PlacementPoint(BaseModel):
    x: int
    y: int

class ImageAdjustRequest(BaseModel):
    sourceImageFilename: str
    targetImageFilename: str
    outputImageFilename: str
    sourceImage: Dimensions
    subjectBox: BoundingBox
    targetImage: Dimensions
    placementPoint: PlacementPoint

# Image processing logic
def adjust_image(source_path, target_path, output_path, source_img, subject_box, target_img, placement_point):
    crop_box = calculate_crop_box(source_img, subject_box, target_img)
    source_img_obj = Image.open(source_path)
    target_img_obj = Image.open(target_path)

    cropped_subject = source_img_obj.crop((
        crop_box['x'],
        crop_box['y'],
        crop_box['x'] + crop_box['width'],
        crop_box['y'] + crop_box['height']
    ))

    offset_x = subject_box['x'] - crop_box['x']
    offset_y = subject_box['y'] - crop_box['y']
    placement_box = {
        "x": placement_point['x'] - offset_x,
        "y": placement_point['y'] - offset_y,
        "width": crop_box['width'],
        "height": crop_box['height']
    }

    target_img_obj.paste(cropped_subject, (placement_box['x'], placement_box['y']))
    target_img_obj.save(output_path)

    return crop_box, placement_box

def calculate_crop_box(source_img, subject_box, target_img):
    subject_aspect = subject_box['width'] / subject_box['height']
    max_crop_width = min(target_img['width'], source_img['width'])
    max_crop_height = min(target_img['height'], source_img['height'])

    crop_width = max_crop_width
    crop_height = crop_width / subject_aspect
    if crop_height > max_crop_height:
        crop_height = max_crop_height
        crop_width = crop_height * subject_aspect

    subject_center_x = subject_box['x'] + subject_box['width'] / 2
    subject_center_y = subject_box['y'] + subject_box['height'] / 2
    crop_x = max(0, subject_center_x - crop_width / 2)
    crop_y = max(0, subject_center_y - crop_height / 2)

    if crop_x + crop_width > source_img['width']:
        crop_x = source_img['width'] - crop_width
    if crop_y + crop_height > source_img['height']:
        crop_y = source_img['height'] - crop_height

    return {
        "x": int(crop_x),
        "y": int(crop_y),
        "width": int(crop_width),
        "height": int(crop_height)
    }

# API Endpoints
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@app.post("/adjust-image")
async def adjust_image_endpoint(request: ImageAdjustRequest):
    try:
        source_path = f"{UPLOAD_DIR}/{request.sourceImageFilename}"
        target_path = f"{UPLOAD_DIR}/{request.targetImageFilename}"
        output_path = f"{OUTPUT_DIR}/{request.outputImageFilename}"

        crop_box, placement_box = adjust_image(
            source_path,
            target_path,
            output_path,
            request.sourceImage.dict(),
            request.subjectBox.dict(),
            request.targetImage.dict(),
            request.placementPoint.dict()
        )
        return {
            "message": "Image adjusted successfully",
            "cropBox": crop_box,
            "placementBox": placement_box,
            "outputImagePath": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/output-image/{filename}")
async def get_output_image(filename: str):
    file_path = f"{OUTPUT_DIR}/{filename}"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename)
    raise HTTPException(status_code=404, detail="Image not found")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or restrict to ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)