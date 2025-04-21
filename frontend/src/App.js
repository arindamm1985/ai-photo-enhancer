import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

function App() {
  const [imageURL, setImageURL] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000";

  const { getRootProps, getInputProps } = useDropzone({
    accept: { 'image/*': [] },
    onDrop: async (files) => {
      setLoading(true);
      setErrorMsg("");
      setImageURL(null);

      try {
        const formData = new FormData();
        formData.append("photo", files[0]);
        formData.append("model", "real-esrgan");

        const res = await axios.post(`${API_BASE}/upload`, formData);
        if (res.data.enhanced_url) {
          setImageURL(res.data.enhanced_url);
        } else {
          setErrorMsg("Failed to enhance image.");
        }
      } catch (err) {
        console.error(err);
        setErrorMsg("Upload failed or server error.");
      } finally {
        setLoading(false);
      }
    }
  });

  return (
    <div className="App" style={{ padding: 20, maxWidth: 600, margin: 'auto' }}>
      <h1>AI Photo Enhancer</h1>
      <div {...getRootProps()} style={{ border: '2px dashed #ccc', padding: 40, textAlign: 'center' }}>
        <input {...getInputProps()} />
        <p>Drag & drop a photo here, or click to select</p>
      </div>

      {loading && <p>⏳ Enhancing your image… please wait.</p>}
      {errorMsg && <p style={{ color: 'red' }}>{errorMsg}</p>}
      {imageURL && (
        <div style={{ marginTop: 20 }}>
          <h3>Enhanced Image:</h3>
          <img src={imageURL} alt="Enhanced" style={{ maxWidth: '100%' }} />
          <p><a href={imageURL} target="_blank" rel="noreferrer">Download Image</a></p>
        </div>
      )}
    </div>
  );
}

export default App;
