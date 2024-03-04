import React, { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css';
import Stack from 'react-bootstrap/Stack';
import ListGroup from 'react-bootstrap/ListGroup';

function Settings() {
    const [selectedDirectory, setSelectedDirectory] = useState(null);
    const [responseText, setResponseText] = useState('');
    const [files, setFiles] = useState([]);

    const handleDirectoryChange = (event) => {
        console.log('handleDirectoryChange called')
        setSelectedDirectory(event.target.files);
        var arr = []; 
        Array.from(event.target.files).forEach((file) => {
            // Perform operations on each file
            arr.push(file.name)
        },
        setFiles(arr));
        console.log(files);
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
                .then(response => response.text())
                .then(data => {
                    // Handle the response data
                    console.log(data);
                    setResponseText(data); // Set the response text in state
                })
                .catch(error => {
                    // Handle any errors
                    console.error(error);
                });
        }
    };

    return (
        <Stack gap={4}>
            <div className='p-2'><h3>Settings</h3></div>
            <hr/>
            <div className='p-2'>
                <p>Upload a directory - Ability to upload multiple files. Once uploaded use command <b>/search</b> to query the data</p>
                <Form.Control type="file" onChange={handleDirectoryChange} directory="" webkitdirectory="" />
            </div>
            <div className='p-2'>
                {files.length > 0 && <p>Files to be uploaded</p>}
                <ListGroup>
                    {
                        files.map((file) => (
                            <ListGroup.Item>{file}</ListGroup.Item>
                        ))
                    }
                </ListGroup>
            </div>
            <div className='p-2'>
                <Button onClick={handleUpload}>Upload</Button>
            </div>
            <div className='p-2'>
                {responseText && <p><b>{responseText}</b></p>} {/* Display the response text */}
            </div>
        </Stack>
    );
}

export default Settings;