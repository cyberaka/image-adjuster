import React, { useEffect, useState } from 'react';
import { Stage, Layer, Rect, Image as KonvaImage } from 'react-konva';

const TargetCanvas = ({
  file,
  placementPoint,
  setPlacementPoint
}: {
  file: File;
  placementPoint: any;
  setPlacementPoint: Function;
}) => {
  const [image, setImage] = useState<HTMLImageElement | null>(null);

  useEffect(() => {
    const img = new window.Image();
    img.src = URL.createObjectURL(file);
    img.onload = () => setImage(img);
  }, [file]);

  return (
    <div style={{ width: '400px', height: '300px', overflow: 'auto', border: '1px solid gray' }}>
      <Stage width={image?.width || 0} height={image?.height || 0} onClick={(e) => {
        const stage = e.target.getStage();
        const pointer = stage?.getPointerPosition();
        if (pointer) {
          setPlacementPoint({ x: pointer.x, y: pointer.y });
        }
      }}>
        <Layer>
          {image && <KonvaImage image={image} />}
          {placementPoint && (
            <Rect
              x={placementPoint.x}
              y={placementPoint.y}
              width={50}
              height={50}
              fill="rgba(255,0,0,0.5)"
              draggable
            />
          )}
        </Layer>
      </Stage>
    </div>
  );
};

export default TargetCanvas;
