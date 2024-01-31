import json
import pandas as pd
from PIL import Image
from aiohttp import ClientSession
from io import BytesIO
import asyncio
from data.data import *
from data.model import cropModel
import random

async def getImage(img_url, session):
    async with session.get(img_url) as response:
        img_data = await response.read()
        return BytesIO(img_data)
    

async def detection(model,img_content):
    cropData = []
    img = Image.open(img_content)
    result = model(img)
    detection = {}
    data = json.loads(result[0].tojson())
    for item in data:
        if "name" in item and "box" in item:
            name = item["name"]
            coordinates = item["box"]
            data = {name:coordinates}
            cropData.append(data)
    return cropData

def cropImages(imgData,coordinates_list):
    try:
        images = []

        for items in coordinates_list:
            for name,location in items.items():
                x1 = location["x1"]
                y1 = location["y1"]
                x2 = location["x2"]
                y2 = location["y2"]
        crop = Image(imgData).crop(x1,y1,x2,y2)
        crop.save(f"{name}.jpg")
    except Exception as e:
        print({"Error":str(e)})
    return crop


    


async def mainDet(url):
    async with ClientSession() as session:
        image = await asyncio.create_task(getImage(url, session))
        croppedData = await asyncio.create_task(detection(cropModel, image))
        allImages = cropImages(image,croppedData)
        # for i, cropped_image in enumerate(allImages):
        #     label, image = list(cropped_image.items())[0]
            
        

        
        return