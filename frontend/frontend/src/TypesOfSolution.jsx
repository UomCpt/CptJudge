import React, { useState } from "react";
import './TypesOfSolution.css';

export default function TypesOfSolution({description}) {
  const [file, setFile] = useState(null);

  const [selected, setSelected] = useState("WriteCodeHere");

  const [uploaded, setUploaded] = useState(false);

  const [codeText, setCodeText] = useState("");

  const [submited, setSubmited] = useState(false);
 
  
  
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

  const handleSubmit= () =>{
    console.log(codeText);
    setSubmited(true);


  };

  const handlechangeCode= (event) =>{
    setCodeText(event.target.value);
    



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



        {selected=="WriteCodeHere"&& !submited && 
        <div id="editorContainer" >
          <div id="description-div">

           <p>Problem Explanation</p>  
          <p id="description">{description}</p> 
          <button id="submit-text" onClick={handleSubmit}>Submit your code</button></div>
          
          
          
          <textarea id="code-editor" onChange={handlechangeCode} />

          

          
          
          


        </div>
        

        }

        {selected=="WriteCodeHere" && submited &&
        <div className="center">
          <p>🟢 You have succesfully submited your code</p>
         
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