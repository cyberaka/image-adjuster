
import React, { useState } from 'react';
import { Container, Row, Col, Button, Form } from 'react-bootstrap';
import SourceCanvas from './SourceCanvas';
import TargetCanvas from './TargetCanvas';
import axios from 'axios';

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
      subjectBox,
      targetImage: { width: 452, height: 796 },
      placementPoint
    };
    console.log('Payload:', adjustPayload);
    const adjustRes = await axios.post('http://localhost:8000/adjust-image', adjustPayload);
    setOutputImageUrl('http://localhost:8000/' + adjustRes.data.outputImagePath);
  };

  return (
    <Container>
      <h1 className="mt-4">Image Adjuster UI</h1>
      <Row className="mt-4">
        <Col>
          <Form.Group controlId="formSourceImage">
            <Form.Label>Upload Source Image</Form.Label>
            <Form.Control type="file" onChange={handleSourceUpload} />
          </Form.Group>
        </Col>
        <Col>
          <Form.Group controlId="formTargetImage">
            <Form.Label>Upload Target Image</Form.Label>
            <Form.Control type="file" onChange={handleTargetUpload} />
          </Form.Group>
        </Col>
      </Row>
      <Row className="mt-4">
        <Col>{sourceFile && <SourceCanvas file={sourceFile} setSubjectBox={setSubjectBox} />}</Col>
        <Col>{targetFile && <TargetCanvas file={targetFile} placementPoint={placementPoint} setPlacementPoint={setPlacementPoint} />}</Col>
      </Row>
      <Row className="mt-4">
        <Col><Button onClick={handleSend}>Send to Backend</Button></Col>
      </Row>
      {outputImageUrl && (
        <Row className="mt-4">
          <Col><h3>Output Image</h3><img src={outputImageUrl} alt="Output" style={{ maxWidth: '100%' }} /></Col>
        </Row>
      )}
    </Container>
  );
};

export default App;
