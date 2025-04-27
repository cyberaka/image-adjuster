
import React, { useEffect, useState } from 'react';
import { Stage, Layer, Rect, Image as KonvaImage } from 'react-konva';

const SourceCanvas = ({ file, setSubjectBox }: { file: File; setSubjectBox: Function }) => {
  const [image, setImage] = useState<HTMLImageElement | null>(null);
  const [box, setBox] = useState({ x: 50, y: 50, width: 100, height: 100 });

  useEffect(() => {
    const img = new window.Image();
    img.src = URL.createObjectURL(file);
    img.onload = () => setImage(img);
  }, [file]);

  useEffect(() => {
    setSubjectBox(box);
  }, [box, setSubjectBox]);

  return (
    <Stage width={400} height={300}>
      <Layer>
        {image && <KonvaImage image={image} width={400} height={300} />}
        <Rect
          x={box.x}
          y={box.y}
          width={box.width}
          height={box.height}
          fill="rgba(0,0,255,0.2)"
          stroke="blue"
          strokeWidth={2}
          draggable
          onDragEnd={(e) => setBox({ ...box, x: e.target.x(), y: e.target.y() })}
          onTransformEnd={(e) => {
            const node = e.target;
            const scaleX = node.scaleX();
            const scaleY = node.scaleY();
            node.scaleX(1);
            node.scaleY(1);
            setBox({
              x: node.x(),
              y: node.y(),
              width: Math.max(5, node.width() * scaleX),
              height: Math.max(5, node.height() * scaleY)
            });
          }}
        />
      </Layer>
    </Stage>
  );
};

export default SourceCanvas;
