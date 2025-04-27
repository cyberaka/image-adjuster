# Image Adjuster API (FastAPI + Pillow)

This project provides a RESTful API for cropping and placing a subject from a source image onto a target image. The API expands the crop region around the subject to fit the target image's available space while maintaining the subject's aspect ratio.

## Features

- Accepts source and target images along with bounding box and placement parameters.
- Expands crop region around the subject without scaling or distorting.
- Composites the cropped subject onto the target image.
- Returns crop and placement box details.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd image-adjuster
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
# OR
venv\Scripts\activate  # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt**

```
fastapi
uvicorn
pillow
```

### 4. Project Structure

```
/image-adjuster
|-- main.py               # FastAPI server
|-- image_service.py      # Image processing logic (Pillow)
|-- requirements.txt      # Python dependencies
|-- README.md             # Setup and usage instructions
```

---

## Running the Server

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`.

---

## API Endpoint

### POST `/adjust-image`

**Request Body (JSON):**

```json
{
  "sourceImagePath": "<source image path>",
  "targetImagePath": "<target image path>",
  "outputImagePath": "<output image path>",
  "sourceImage": { "width": 796, "height": 452 },
  "subjectBox": { "x": 283, "y": 124, "width": 306, "height": 320 },
  "targetImage": { "width": 452, "height": 796 },
  "placementPoint": { "x": 72, "y": 236 }
}
```

**Response:**

```json
{
  "message": "Image adjusted successfully",
  "cropBox": { "x": 210, "y": 0, "width": 452, "height": 452 },
  "placementBox": { "x": -1, "y": 112, "width": 452, "height": 452 },
  "outputImagePath": "<output image path>"
}
```

---

## Testing the API

Use **curl** or **Postman**:

```bash
curl -X POST "http://localhost:8000/adjust-image" \
-H "Content-Type: application/json" \
-d '{
  "sourceImagePath": "/Users/abhinavanand/Desktop/billi/source.png",
  "targetImagePath": "/Users/abhinavanand/Desktop/billi/target.png",
  "outputImagePath": "/Users/abhinavanand/Desktop/billi/output.png",
  "sourceImage": { "width": 796, "height": 452 },
  "subjectBox": { "x": 283, "y": 124, "width": 306, "height": 320 },
  "targetImage": { "width": 452, "height": 796 },
  "placementPoint": { "x": 72, "y": 236 }
}'
```

---

## Notes

- Ensure that **source image paths** and **target image paths** are valid and accessible.
- Output images will be saved at the specified `outputImagePath`.
- This API assumes **Pillow** is used for image processing.
