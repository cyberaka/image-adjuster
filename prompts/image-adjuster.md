# Image Adjuster Program Specification

## Objective

Create a **TypeScript + Sharp** program that:

1. **Identifies a subject** in a source image (bounding box provided).
2. **Expands the crop region** around the subject based on the target image’s available space.
3. **Maintains the subject's aspect ratio** (no distortion).
4. **Places the cropped region** onto a provided target image at a specified point.
5. **Outputs:**
   - Crop box in the source image.
   - Placement box in the target image.
   - Final composited target image with the subject placed at the correct location.

---

## Input Parameters

- **Source image**: File path (e.g., `source.png`).
- **Target image**: File path (e.g., `target.png`).
- **Source image dimensions**: `{ width, height }`.
- **Subject bounding box** in the source image: `{ x, y, width, height }`.
- **Target image dimensions**: `{ width, height }`.
- **Placement point** in target image: `{ x, y }` (where the subject should be placed).

---

## Output

- **Crop box** (from the source image): `{ x, y, width, height }`.
- **Placement box** (on the target image): `{ x, y, width, height }`.
- Final **composited target image** saved as a file (e.g., `output.png`).

---

## Constraints

1. **No scaling or distortion** of the subject (aspect ratio preserved).
2. **Expand the crop region** from the subject outward **as much as the target allows**, without exceeding the **source image bounds**.
3. The **placement point** in the target is for the **subject's original bounding box**, so any **expansion of the crop region must adjust the placement accordingly**.

---

## Visual Explanation

### **Source Image Layout:**

```
|-------------------| <-- source image (e.g., 796x452)
|                   |
|     |-------|     | <-- subject bounding box (e.g., 306x320 at x:283, y:124)
|     |Subject|     |
|     |-------|     |
|                   |
|-------------------|
```

### **Target Image Layout (Empty Space):**

```
|--------------| <-- target image (e.g., 452x796)
|              |
|              |
|              |
|              |
|              |
|              |
|              |
|              |
|              |
|--------------|
```

### **Subject Placement Proposal in Target:**

```
|--------------| <-- target image
|              |
|    |-------| | <-- subject placed here (starting at placement point)
|    |Subject| |
|    |-------| |
|              |
|              |
|--------------|
```

### **Expanded Crop Region in Source:**

- **Expand the crop region** around the subject, keeping **aspect ratio**, up to:
  - **Target width (452)**.
  - **Source height (452)**.

```
|-------------------| <-- source image
|  [        ]       | <-- expanded crop box around subject
|   |-------|       |
|   |Subject|       |
|   |-------|       |
|  [        ]       |
|-------------------|
```

---

## Example Inputs

```json
{
  "sourceImage": { "width": 796, "height": 452 },
  "subjectBox": { "x": 283, "y": 124, "width": 306, "height": 320 },
  "targetImage": { "width": 452, "height": 796 },
  "placementPoint": { "x": 72, "y": 236 }
}
```

---

## Expected Crop and Placement Logic

1. **Calculate expanded crop region:**

   - **Max crop width** = `min(452, source width)` = 452.
   - **Max crop height** = `min(796, source height)` = 452.
   - **Maintain subject's aspect ratio**.

2. **Center crop region around subject:**

   - Subject center (X) = `283 + 306 / 2 = 436`.
   - Subject center (Y) = `124 + 320 / 2 = 284`.
   - Crop X = `436 - 452 / 2 = 210`.
   - Crop Y = `284 - 452 / 2 = 58` (adjusted to stay within bounds).

3. **Final Crop Box:**

   ```json
   { "x": 210, "y": 0, "width": 452, "height": 452 }
   ```

4. **Adjust placement in target:**

   - Offset X = `subjectBox.x - cropBox.x = 283 - 210 = 73`.
   - Offset Y = `subjectBox.y - cropBox.y = 124 - 0 = 124`.
   - Final placement point:

   ```json
   { "x": placementPoint.x - offsetX, "y": placementPoint.y - offsetY }
   ```

5. **Final Placement Box:**
   ```json
   { "x": -1, "y": 112, "width": 452, "height": 452 }
   ```

---

## Code Requirements

- **TypeScript**.
- **Sharp** for image manipulation.
- Implement:
  - **Crop region calculation** with boundary checks.
  - **Placement adjustment** based on expanded crop.
  - **Composite** the cropped subject onto the target image.
- Include:
  - **Console output** for crop and placement boxes.
  - Save the **final composited target image**.
