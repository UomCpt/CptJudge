import React, { useState } from "react";
import './TypesOfSolution.css';

export default function TypesOfSolution() {
  const [file, setFile] = useState(null);

  const [selected, setSelected] = useState("WriteCodeHere");

  const [uploaded, setUploaded] = useState(false);
 

  
  const handleSelect = (event)=>{
    setSelected(event.target.value);
    
  }
  
  
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
 
  };

  const handleUpload = () => {
    if (!file) return;
    console.log("Ανεβάζουμε:", file);
    setUploaded(true);
    
  };



  return (
    <div id="body-types-of-solution">
     
      <div id="div-select"  onChange={handleSelect}>
        <p id="p-type">Type of the Solution</p>
        <select id="select-type" >
          <option value="WriteCodeHere">Write Code Here</option>
          <option value="UploadFile">Upload File</option>
        </select>
      </div>

        {selected=="WriteCodeHere"&& 
        <div id="page-editor" className="center"> 
          <p>ksdaskldaklsndfnf lngjrfgnjng jn  gkmjrtkhkrthn </p>
          <input type="text" />
          

          
          
          


        </div>
        

        }
        
        
        
        
        
        
        {selected=="UploadFile" && 

         <div id="file-uploader" className="center">
        {!uploaded &&<input type="file" onChange={handleFileChange} />}
        { !uploaded&& file && <p>Selected File: {file.name}</p>}
        {!uploaded && <button onClick={handleUpload}>Submit</button>}
        {uploaded && <p>🟢 You have succesfully uploaded the file: {file.name}</p>}
      </div>}
      
    </div>
  );
}