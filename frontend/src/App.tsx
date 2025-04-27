import React, { useState } from 'react';
import { Container, Button, Form, Tabs, Tab } from 'react-bootstrap';
import SourceCanvas from './SourceCanvas';
import TargetCanvas from './TargetCanvas';
import axios from 'axios';
import './App.css'; // For full height styling

const App = () => {
  const [sourceFile, setSourceFile] = useState<File | null>(null);
  const [targetFile, setTargetFile] = useState<File | null>(null);
  const [outputImageUrl, setOutputImageUrl] = useState<string>('');
  const [subjectBox, setSubjectBox] = useState<{ x: number; y: number; width: number; height: number } | null>(null);
  const [placementPoint, setPlacementPoint] = useState<{ x: number; y: number } | null>(null);
  const [sourceFilename, setSourceFilename] = useState<string>('');
  const [targetFilename, setTargetFilename] = useState<string>('');

  const handleSourceUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSourceFile(file);
      const formData = new FormData();
      formData.append('file', file);
      const res = await axios.post('http://localhost:8000/upload-image', formData);
      setSourceFilename(res.data.filename);
    }
  };

  const handleTargetUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setTargetFile(file);
      const formData = new FormData();
      formData.append('file', file);
      const res = await axios.post('http://localhost:8000/upload-image', formData);
      setTargetFilename(res.data.filename);
    }
  };

  const handleSend = async () => {
    if (!subjectBox || !placementPoint) return;
    const adjustPayload = {
      sourceImageFilename: sourceFilename,
      targetImageFilename: targetFilename,
      outputImageFilename: 'output.png',
      sourceImage: { width: 796, height: 452 },
      subjectBox: {
        x: Math.round(subjectBox.x),
        y: Math.round(subjectBox.y),
        width: Math.round(subjectBox.width),
        height: Math.round(subjectBox.height)
      },
      targetImage: { width: 452, height: 796 },
      placementPoint: {
        x: Math.round(placementPoint.x),
        y: Math.round(placementPoint.y)
      }
    };
    const adjustRes = await axios.post('http://localhost:8000/adjust-image', adjustPayload);
    const timestamp = new Date().getTime();
    setOutputImageUrl(
      'http://localhost:8000/output-image/' +
      adjustRes.data.outputImagePath.split('/').pop() +
      '?t=' + timestamp
    );
  };

  return (
    <Container fluid className="app-container">
      <h1 className="mt-2 text-center">Image Adjuster UI</h1>
      <Tabs defaultActiveKey="source" id="image-tabs" className="mb-3" fill>
        <Tab eventKey="source" title="Source">
          <div className="tab-pane-container">
            <Form.Group controlId="formSourceImage" className="mb-3">
              <Form.Label>Upload Source Image</Form.Label>
              <Form.Control type="file" onChange={handleSourceUpload} />
            </Form.Group>
            {sourceFile && <SourceCanvas file={sourceFile} setSubjectBox={setSubjectBox} />}
          </div>
        </Tab>
        <Tab eventKey="target" title="Target">
          <div className="tab-pane-container">
            <Form.Group controlId="formTargetImage" className="mb-3">
              <Form.Label>Upload Target Image</Form.Label>
              <Form.Control type="file" onChange={handleTargetUpload} />
            </Form.Group>
            {targetFile && <TargetCanvas
              file={targetFile}
              placementPoint={placementPoint}
              setPlacementPoint={setPlacementPoint}
              subjectBox={subjectBox}
            />
            }
          </div>
        </Tab>
        <Tab eventKey="output" title="Output">
          <div className="tab-pane-container">
            <Button onClick={handleSend} className="mb-3">Send to Backend</Button>
            {outputImageUrl && (
              <div className="output-image-container">
                <img src={outputImageUrl}
                  alt="Output"
                  style={{
                    maxWidth: '100%',
                    maxHeight: '80vh',
                    objectFit: 'contain',
                    border: '1px solid gray'
                  }}
                />
              </div>
            )}
          </div>
        </Tab>
      </Tabs>
    </Container>
  );
};

export default App;
