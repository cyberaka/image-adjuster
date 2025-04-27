import React, { useEffect, useRef, useState } from 'react';
import { Stage, Layer, Rect, Image as KonvaImage, Transformer } from 'react-konva';

const SourceCanvas = ({ file, setSubjectBox }: { file: File; setSubjectBox: Function }) => {
  const [image, setImage] = useState<HTMLImageElement | null>(null);
  const [box, setBox] = useState({ x: 50, y: 50, width: 100, height: 100 });
  const rectRef = useRef<any>(null);
  const trRef = useRef<any>(null);

  useEffect(() => {
    const img = new window.Image();
    img.src = URL.createObjectURL(file);
    img.onload = () => setImage(img);
  }, [file]);

  useEffect(() => {
    setSubjectBox(box);
  }, [box, setSubjectBox]);

  useEffect(() => {
    if (trRef.current && rectRef.current) {
      trRef.current.nodes([rectRef.current]);
      trRef.current.getLayer().batchDraw();
    }
  }, [image]);

  return (
    <div className="canvas-wrapper">
      <Stage width={image?.width || 0} height={image?.height || 0}>
        <Layer>
          {image && <KonvaImage image={image} />}
          <Rect
            ref={rectRef}
            x={box.x}
            y={box.y}
            width={box.width}
            height={box.height}
            fill="rgba(0,0,255,0.2)"
            stroke="blue"
            strokeWidth={2}
            draggable
            onDragEnd={(e) => setBox({ ...box, x: e.target.x(), y: e.target.y() })}
            onTransformEnd={() => {
              const node = rectRef.current;
              const scaleX = node.scaleX();
              const scaleY = node.scaleY();
              node.scaleX(1);
              node.scaleY(1);
              setBox({
                x: node.x(),
                y: node.y(),
                width: Math.max(5, node.width() * scaleX),
                height: Math.max(5, node.height() * scaleY),
              });
            }}
          />
          <Transformer ref={trRef} />
        </Layer>
      </Stage>
    </div>
  );
};

export default SourceCanvas;
