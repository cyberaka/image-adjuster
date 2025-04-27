import React, { useEffect, useState } from 'react';
import { Stage, Layer, Rect, Image as KonvaImage } from 'react-konva';

const TargetCanvas = ({
  file,
  placementPoint,
  setPlacementPoint,
  subjectBox
}: {
  file: File;
  placementPoint: any;
  setPlacementPoint: Function;
  subjectBox: { x: number; y: number; width: number; height: number } | null;
}) => {
  const [image, setImage] = useState<HTMLImageElement | null>(null);

  useEffect(() => {
    const img = new window.Image();
    img.src = URL.createObjectURL(file);
    img.onload = () => setImage(img);
  }, [file]);

  return (
    <div className="canvas-wrapper">
      <Stage width={image?.width || 0} height={image?.height || 0} onClick={(e) => {
        const stage = e.target.getStage();
        const pointer = stage?.getPointerPosition();
        if (pointer) {
          setPlacementPoint({ x: pointer.x, y: pointer.y });
        }
      }}>
        <Layer>
          {image && <KonvaImage image={image} />}
          {placementPoint && subjectBox && (
            <Rect
              x={placementPoint.x}
              y={placementPoint.y}
              width={subjectBox.width}
              height={subjectBox.height}
              fill="rgba(255,0,0,0.5)"
              draggable
              onDragEnd={(e) =>
                setPlacementPoint({ x: e.target.x(), y: e.target.y() })
              }
            />
          )}
        </Layer>
      </Stage>
    </div>
  );
};

export default TargetCanvas;
