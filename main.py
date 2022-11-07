import imp
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
import glob
import shutil

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/input", StaticFiles(directory="input"), name="input")
templates = Jinja2Templates(directory=".")

def typedir_maker(text: str):
    # text = 'image/png'
    category_list = text.split('/')
    print(category_list)
    category_layer = []
    for i in category_list:
        category_layer.append(i)
        layer = 'input/' + '/'.join(category_layer)
        print(layer)
        if not os.path.exists(layer):
            os.mkdir(layer)

def type_getter(text: str):
    # text = 'image/png'
    category_list = text.split('/')
    print(category_list)
    return category_list[0]

@app.get("/")
async def root(request: Request):
    # return {'message': 'hello world'}
    return templates.TemplateResponse('index.html', {"request": request, "num": 12, "video": "input/video/mp4/2022-05-22 20-53-01.mp4", "audio": "input/audio/wav/asano.wav"})

@app.post("/")
async def root(request_file: UploadFile, request: Request):
    input_file_type = request_file.content_type
    input_file_name = 'input/' + input_file_type + '/' + request_file.filename
    print(input_file_name, input_file_type)
    print(input_file_name, input_file_type, type(input_file_name), type(input_file_type))
    typedir_maker(input_file_type)
    with open(f'{input_file_name}', 'w+b') as buffer:
            shutil.copyfileobj(request_file.file, buffer)
    if type_getter(input_file_type) == 'video':
        print("this is video file !!")
        return templates.TemplateResponse('video-viewer.html', {"request": request, "video": input_file_name})
    elif type_getter(input_file_type) == 'audio':
        print("this is audio file !!")
        return templates.TemplateResponse('audio-viewer.html', {"request": request, "audio": input_file_name})
    else:
        print("this is other file !!")
        return FileResponse(f'{input_file_name}')

@app.get("/sub")
async def root(request: Request):
    # return {'message': 'hello world'}
    return templates.TemplateResponse('sub.html', {"request": request})

@app.get("/sub/{id}")
async def root(id):
    return {"id": id}