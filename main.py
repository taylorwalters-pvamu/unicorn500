# PLEASE READ ALL COMMENTS BELOW THIS LINE___________________________________________________________________________________
# use PIP install for the following packages below.
# make sure you have python installed and added to path if on windows. You can also download python from the microsoft store.

# to run this app follow the steps below (first ensure you completed the above instructions):
# - in terminal type: Uvicorn main:app --reload
# - copy the url found in the terminal into a browser of you choice
# - append /docs to the url
# message in the team chat for any assistance needed. Yepppp good lookin yall. 

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import shutil
import tempfile
import os
from qvd import qvd_reader

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
    """_summary_
        The below function is an api path named "/upload_file" this path allows the user to upload a qvd file for the function to then convert to JSON.
        The JSON will be passed to the appropriate "visualization" function.
        
        arguments: 
            name: file | type: UploadFile | description: the QVD file
            name: visualization | type: str | description: the 
            
        returns:
            null
        
        remember, this function does not need to return anything. Its job is to
        JSON serialize (to convert to json) the QVD file then pass that to PowerBI or another visualization tool
    """
@app.post("/upload_file")
async def create_upload_file(file: UploadFile, visualization: str):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            shutil.copyfileobj(file.file, temp)
            temp.flush()
            temp.seek(0)
            df_read = qvd_reader.read(temp.name)
            df = pd.DataFrame(df_read)
            json_data = df.to_json(orient='index')
            json_response = JSONResponse(content=json_data, status_code=200)
            
            if visualization == "power_bi":
                json_to_powerbi(json_response)
            else:
                return {"message": "complete"}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"ValueError: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

async def json_to_powerbi(json_data):
    print("TODO: work on json_to_powerbi")

#need to have the json_data hit power bi's endpoint to create a dataset
#route for the batch processing that you can require a folder or zip for
    
    '''# Create a temporary file to save the uploaded QVD file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_file_path = tmp_file.name
    
    # Now, use qvd_reader to read the QVD file into a pandas DataFrame
    try:
        df_read = qvd_reader.read(tmp_file_path)
        df = pd.DataFrame(df_read)
        
        # Convert the DataFrame into JSON
        json_data = df.to_json(orient="records")
        
        # Clean up the temporary file
        os.unlink(tmp_file_path)
        
        return JSONResponse(content=json_data, media_type="application/json")
    except Exception as e:
     os.unlink(tmp_file_path)
     print(f"Error: {str(e)}")  # Add logging or printing for debugging
     return JSONResponse(content={"error": str(e)}, status_code=500)
     '''