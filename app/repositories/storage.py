import pyrebase
import os
import mimetypes
from loguru import logger
from fastapi.responses import FileResponse
from fastapi import status, Response, HTTPException
from .import file_names_processing
from PIL import Image, ImageOps
from dotenv import load_dotenv
load_dotenv()



config:dict = {
    "apiKey": os.getenv('API_KEY'),
    "authDomain": os.getenv('AUTH_DOMAIN'),
    "project_id": os.getenv('PROJECT_ID'),
    "storageBucket": os.getenv('STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('MESSAGING_SENDER_ID'),
    "appId": os.getenv('APP_ID'),
    "measurementId": os.getenv('MEASUREMENT_ID'),
    "databaseURL": os.getenv('DATABASE_URL'),
    "serviceAccount": 'service-account.json'
}


firebase= pyrebase.initialize_app(config)
storage= firebase.storage()


UPLOAD_DIR= os.path.join("app/media")
file_extensions:list= [".gltf", ".glb", ".fbx", ".stl", ".obj", ".dae", ".ifc"]
async def upload_model_zip(folder_id, folder_path):
    try:
        model_name_and_path= None
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                filename_and_path= f"models/{folder_id}/{local_file_path}"
                filename_and_path= filename_and_path.replace('\\', '/')

                logger.info(f"Uploading {local_file_path} to storage")
                storage.child(filename_and_path).put(local_file_path)
                if os.path.splitext(filename_and_path.split('\\')[0])[1] in file_extensions:
                    model_name_and_path= filename_and_path

        if not model_name_and_path:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= "Could not upload model file, something went wrong, also make sure you have good internet connection.")
        
        logger.info("Getting the file link")
        access_link= storage.child(model_name_and_path).get_url(None)
        return access_link
 
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= "Could not upload model file, something went wrong, also make sure you have good internet connection.")




async def upload_model_file_only(file, bucket_folder_path):
        filename= file.filename
        filename_and_path= f"models/{bucket_folder_path}/model_file/{filename}"

        logger.info(f"Uploading {filename_and_path} to storage")  
        readFile= file.file.read()    

        # Get content type 
        contentType:str = file.content_type
        
        storage.child(filename_and_path).put(readFile, content_type= contentType)

        logger.info("Getting the file link")
        access_link= storage.child(filename_and_path).get_url(None)
        return access_link



async def upload_model_picture(file, bucket_folder_path):
        filename= await file_names_processing.names_process(file)
        filename_and_path= f"models/{bucket_folder_path}/picture_cover/{os.path.splitext(filename)[0]}.webp"
        
        #++++++IMAGE COMPRESSING BEFORE UPLOAD++++++++
        logger.info("Compressing model picture")
        img = Image.open(file.file)
        try:
            img= ImageOps.exif_transpose(img)
        except:
            pass
        img.save("compressed_img.webp", format="webp", quality=15)

            
        storage.child(filename_and_path).put("compressed_img.webp")
 
        # Clean up the temporary and compressed images
        logger.info("Cleaning up temporary image")
        os.remove("compressed_img.webp")
        
        logger.info("Getting the image link")
        access_link= storage.child(filename_and_path).get_url(None)
        return access_link




async def upload_profile_picture(file, bucket_folder_path):

        filename= await file_names_processing.names_process(file)
        
        filename_and_path= f"profile_picture/{bucket_folder_path}/{os.path.splitext(filename)[0]}.webp"
        #++++++IMAGE COMPRESSING BEFORE UPLOAD++++++++
        logger.info("Compressing profile picture")
        img = Image.open(file.file)
        try:
            img= ImageOps.exif_transpose(img)
        except:
            pass
        img.save("compressed_img.webp", format="webp", quality=15)

            
        storage.child(filename_and_path).put("compressed_img.webp")
 
        # Clean up the temporary and compressed images
        logger.info("Cleaning up temporary image")
        os.remove("compressed_img.webp")
        
        logger.info("Getting the image link")
        access_link= storage.child(filename_and_path).get_url(None)
        return access_link
    
    
    
    
    
# TO DOWNLOAD, YOU SPECIFY THE FILENAME AND THE NAME YOU WANT TO SAVE IT AS ON YOUR LOCAL
# storage.download(filename_and_path, filename)    