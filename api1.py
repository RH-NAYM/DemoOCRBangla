from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from typing import List, Union
from main1 import *
import uvicorn
from datetime import datetime
import pytz
import torch

app = FastAPI()

class Item(BaseModel):
    url: str

def get_bd_time():
    bd_timezone = pytz.timezone("Asia/Dhaka")
    time_now = datetime.now(bd_timezone)
    current_time = time_now.strftime("%I:%M:%S %p")
    return current_time


async def process_item(item: Item):
    try:
        result = await mainDet(item.url)
        result = json.loads(result)
        return result
    finally:
        torch.cuda.empty_cache()
        pass

async def process_items(items: Union[Item, List[Item]]):
    print(type(items))
    if type(items)==list:
        coroutines = [process_item(item) for item in items]
        results = await asyncio.gather(*coroutines)
        print("multi : ",results)
    else:
        results = await process_item(items)
        print("single : ", results)
    return results



@app.get("/status")
async def status():
    return "AI Server in running"

@app.post("/nagad")
async def create_items(items: Union[Item, List[Item]]):
    try:
        results = await process_items(items)
        print("Result Sent to User:", results)
        print("###################################################################################################")
        print(items)
        print("Last Execution Time : ", get_bd_time())
        return results
    except Exception as e:
        return {"AI": f"Error: {str(e)}"}
    finally:
        torch.cuda.empty_cache()
        pass

if __name__ == "__main__":
    try:
        # del nbrtuModel
        uvicorn.run(app, host="127.0.0.1", port=4444)
    finally:
        torch.cuda.empty_cache()
