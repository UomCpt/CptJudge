import React, { useState } from "react";
import './TypesOfSolution.css';

export default function TypesOfSolution() {
  const [file, setFile] = useState(null);

  const [selected, setSelected] = useState("WriteCodeHere");

  
  const handleSelect = (event)=>{
    setSelected(event.target.value);
    
  }
  
  
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = () => {
    if (!file) return;
    console.log("Ανεβάζουμε:", file);
  };



  return (
    <div id="body-types-of-solution">
     
      <div id="div-select" onChange={handleSelect}>
        <p id="p-type">Type of the Solution</p>
        <select id="select-type">
          <option value="WriteCodeHere">Write Code Here</option>
          <option value="UploadFile">Upload File</option>
        </select>
      </div>

        {selected=="UploadFile" && 

         <div id="file-uploader">
        <input type="file" onChange={handleFileChange} />
        {file && <p>Επιλεγμένο αρχείο: {file.name}</p>}
        <button onClick={handleUpload}>Upload</button>
      </div>}
    </div>
  );
}