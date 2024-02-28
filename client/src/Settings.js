import React, { useState } from 'react';
import './index.css';
import { v4 as uuidv4 } from 'uuid';

function Settings() {
    const [selectedDirectory, setSelectedDirectory] = useState(null);

    const handleDirectoryChange = (event) => {
        setSelectedDirectory(event.target.files);
    };

    const handleUpload = () => {
        if (selectedDirectory) {
            console.log(selectedDirectory);
            const formData = new FormData();
            const uniqueId = uuidv4();
            formData.append('requestId', uniqueId);
            console.log(uniqueId);
            formData.append('file', selectedDirectory);
            Array.from(selectedDirectory).forEach((file) => {
                // Perform operations on each file
                console.log(file.name);
                formData.append('file', file);
            });
            fetch('http://localhost:8000/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    // Handle the response data
                    console.log(data);
                })
                .catch(error => {
                    // Handle any errors
                    console.error(error);
                });
        }
    };

    return (
        <div>
            <h3>Settings</h3>
            <input type="file" onClick={handleDirectoryChange} directory="" webkitdirectory="" />
            <button onClick={handleUpload}>Upload</button>
        </div>
    );
}

export default Settings;