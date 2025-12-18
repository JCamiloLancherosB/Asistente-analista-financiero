import React, { useState } from 'react';
import { uploadAPI } from '../services/api';
import './FileUpload.css';

function FileUpload({ onUploadSuccess }) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      setError('Por favor selecciona un archivo CSV');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const result = await uploadAPI.uploadCSV(file);
      onUploadSuccess(result);
      e.target.value = ''; // Reset input
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar el archivo');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-upload">
      <label htmlFor="csv-upload" className="upload-label">
        {uploading ? 'Cargando...' : '📁 Cargar CSV'}
      </label>
      <input
        id="csv-upload"
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        disabled={uploading}
        style={{ display: 'none' }}
      />
      {error && <div className="upload-error">{error}</div>}
    </div>
  );
}

export default FileUpload;
