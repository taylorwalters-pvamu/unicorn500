# PLEASE READ ALL COMMENTS BELOW THIS LINE___________________________________________________________________________________
# use PIP install for the following packages below.
# make sure you have python installed and added to path if on windows. You can also download python from the microsoft store.

# to run this app follow the steps below (first ensure you completed the above instructions):
# - in terminal type: Uvicorn main:app --reload
# - copy the url found in the terminal into a browser of you choice
# - append /docs to the url
# message in the team chat for any assistance needed. Yepppp good lookin yall. 

from fastapi import FastAPI, File, UploadFile, HTTPException
import httpx
from fastapi.responses import JSONResponse
import requests
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
                json_response = {
                  "name": "SalesMarketing",
                  "defaultMode": "Push",
                  "tables": [
                    {
                      "name": "Product",
                      "columns": [
                        {
                          "name": "ProductID",
                          "dataType": "Int64"
                        },
                        {
                          "name": "Name",
                          "dataType": "string"
                        },
                        {
                          "name": "Category",
                          "dataType": "string"
                        },
                        {
                          "name": "IsCompete",
                          "dataType": "bool"
                        },
                        {
                          "name": "ManufacturedOn",
                          "dataType": "DateTime"
                        },
                        {
                          "name": "Sales",
                          "dataType": "Int64",
                          "formatString": "Currency"
                        }
                      ]
                    }
                  ]
                }
                return await powerbi_postdatasets(json_data)
            else:
                return {"message": "complete"}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"ValueError: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
async def test():
    return {"message":"This is a test message"}


async def powerbi_postdatasets(json_data):
    
    bearer_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlhSdmtvOFA3QTNVYVdTblU3Yk05blQwTWpoQSIsImtpZCI6IlhSdmtvOFA3QTNVYVdTblU3Yk05blQwTWpoQSJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvZjQ4ZGE5ZGUtOTg5Yi00YjIzLThhODItZDkyMDZiN2QzM2QzLyIsImlhdCI6MTcxMDk1Mjg3NSwibmJmIjoxNzEwOTUyODc1LCJleHAiOjE3MTA5NTc4NjYsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBVlFBcS84V0FBQUFMSG15dkJ5MGE2WXNrVWZzcGpUd2FuVFVBTmwvclE1RHc1UVVCNHlONWo3eTNLMVdLSjFXUDJIeGlXNDhLUllRbTJ3ay9FZkxySXdsMVcwbmlvS2o5RjV4aGJxN1dwUlpVQ0Z6Q0hhbm5rUT0iLCJhbXIiOlsicHdkIiwibWZhIl0sImFwcGlkIjoiMThmYmNhMTYtMjIyNC00NWY2LTg1YjAtZjdiZjJiMzliM2YzIiwiYXBwaWRhY3IiOiIwIiwiZmFtaWx5X25hbWUiOiJBZ3VidXpvIiwiZ2l2ZW5fbmFtZSI6Ik1heGltdXMiLCJpcGFkZHIiOiIyNjAwOjE3MDA6ZjcxOmJlYzA6NmQwNzo5OGVlOjg5MjE6OTJkMiIsIm5hbWUiOiJNYXhpbXVzIElrZW5uYSBBZ3VidXpvIiwib2lkIjoiZGUwZDhhMDEtOTliNy00YzQ4LThhNWEtM2UzMmU5OTc3MzkxIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTMwMjA1MTE4ODctNzkxMTAxODA3LTQyNzA3NzkxMTgtMjE3MjMyIiwicHVpZCI6IjEwMDMyMDAwOUI5NDM3MEQiLCJyaCI6IjAuQVJJQTNxbU45SnVZSTB1S2d0a2dhMzB6MHdrQUFBQUFBQUFBd0FBQUFBQUFBQUFTQUY0LiIsInNjcCI6IkFwcC5SZWFkLkFsbCBDYXBhY2l0eS5SZWFkLkFsbCBDYXBhY2l0eS5SZWFkV3JpdGUuQWxsIENvbnRlbnQuQ3JlYXRlIERhc2hib2FyZC5SZWFkLkFsbCBEYXNoYm9hcmQuUmVhZFdyaXRlLkFsbCBEYXRhZmxvdy5SZWFkLkFsbCBEYXRhZmxvdy5SZWFkV3JpdGUuQWxsIERhdGFzZXQuUmVhZC5BbGwgRGF0YXNldC5SZWFkV3JpdGUuQWxsIEdhdGV3YXkuUmVhZC5BbGwgR2F0ZXdheS5SZWFkV3JpdGUuQWxsIEl0ZW0uRXhlY3V0ZS5BbGwgSXRlbS5SZWFkV3JpdGUuQWxsIEl0ZW0uUmVzaGFyZS5BbGwgT25lTGFrZS5SZWFkLkFsbCBPbmVMYWtlLlJlYWRXcml0ZS5BbGwgUGlwZWxpbmUuRGVwbG95IFBpcGVsaW5lLlJlYWQuQWxsIFBpcGVsaW5lLlJlYWRXcml0ZS5BbGwgUmVwb3J0LlJlYWRXcml0ZS5BbGwgUmVwcnQuUmVhZC5BbGwgU3RvcmFnZUFjY291bnQuUmVhZC5BbGwgU3RvcmFnZUFjY291bnQuUmVhZFdyaXRlLkFsbCBUZW5hbnQuUmVhZC5BbGwgVGVuYW50LlJlYWRXcml0ZS5BbGwgVXNlclN0YXRlLlJlYWRXcml0ZS5BbGwgV29ya3NwYWNlLkdpdENvbW1pdC5BbGwgV29ya3NwYWNlLkdpdFVwZGF0ZS5BbGwgV29ya3NwYWNlLlJlYWQuQWxsIFdvcmtzcGFjZS5SZWFkV3JpdGUuQWxsIiwic2lnbmluX3N0YXRlIjpbImttc2kiXSwic3ViIjoieC1Xd1dHVzY1OXlXaUFqOS13aEFRRmZUeXVaWGVPX0NtNTNFWm5LSEY3VSIsInRpZCI6ImY0OGRhOWRlLTk4OWItNGIyMy04YTgyLWQ5MjA2YjdkMzNkMyIsInVuaXF1ZV9uYW1lIjoibWFndWJ1em9AcHZhbXUuZWR1IiwidXBuIjoibWFndWJ1em9AcHZhbXUuZWR1IiwidXRpIjoicWpNMEJBLUliRXFOQ193YkwzeEJBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il19.BcI5niYG4r-pR5blZW2v9aa4O_79Bf9vqza1QksX4wg52oZPSZPLYIwyXP9ZtQdUK2BKF2VgKEVmcWb86oM9v57Gv3Avct1GatzSz7fPzPP0TPjWN3JuRjbe4ykdRq1Ep-p65nO0931KLynOzqEjoQ-5_IadaxsMCnqdQ5uEI9qCtPQ1S17sVXZAs84K-lftgrYQWI81sGOcC98mKlx1GQPAoivBua91DcfgDQyH2V09p0mJrwaGRWmuY2ZtmRHRgI9DnOjJUUxhGUaWjOQZGCL6KP9oJY7uuxmOE0Yru5DRZ5o-Y-F6QZwjqgsJ0QspqPamfOrBuD1p8lvU58kazQ"
    url = "https://api.powerbi.com/v1.0/myorg/datasets"
    
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        json_data
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=json_data)
        if response.status_code == 200:
            return {"message": "Data posted successfully to Power BI"}
        else:
            # raise HTTPException(status_code=response.status_code, detail=response.text)
            return {"status_code": response.status_code, "detail": response.text}
    
    