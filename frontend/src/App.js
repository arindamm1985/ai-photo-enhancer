import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

function App() {
  const [taskId, setTaskId] = useState(null);
  const [imageURL, setImageURL] = useState(null);

  const { getRootProps, getInputProps } = useDropzone({
    accept: { 'image/*': [] },
    onDrop: async (files) => {
      const formData = new FormData();
      formData.append("photo", files[0]);
      formData.append("model", "real-esrgan");

      const res = await axios.post('/upload', formData);
      setTaskId(res.data.task_id);

      const poll = setInterval(async () => {
        const statusRes = await axios.get(`/status/${res.data.task_id}`);
        if (statusRes.data.status === 'SUCCESS') {
          clearInterval(poll);
          setImageURL(statusRes.data.result);
        }
      }, 3000);
    }
  });

  return (
    <div className="App" style={{ padding: 20 }}>
      <h1>AI Photo Enhancer</h1>
      <div {...getRootProps()} style={{ border: '2px dashed #ccc', padding: 40 }}>
        <input {...getInputProps()} />
        <p>Drag & drop a photo here or click to select</p>
      </div>
      {taskId && <p>Task ID: {taskId} (Processing...)</p>}
      {imageURL && <img src={imageURL} alt="enhanced" style={{ maxWidth: '100%' }} />}
    </div>
  );
}

export default App;
