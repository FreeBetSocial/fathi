
from typing import Dict, Optional
from fastapi import FastAPI,Path,UploadFile,File
from pydantic import BaseModel
import json, graph, fire,os
from fastapi.middleware.cors import CORSMiddleware

description = """
## REST API для нахождения оптимального пути и нахождения пожара 🚀

Описание функционала
"""

class Items(BaseModel):
    title: str=Path(title="Название базы данных",default="Name")
    items: list =Path(default=[])

    def __str__(self) -> str:
        return json.dumps({
            "title":self.title,
            "items":self.items
        },indent=4)

app = FastAPI(
    title="REST API ФАТХИ",
    description=description,
    version="0.0.5",
    contact={
        "name": "Дмитрий Владимирович Фатхи",
        "url": "https://ff.xox.su"
    },

    docs_url="/api/rest",
    openapi_url="/api/openapi.json"
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
try:
    with open("data.json") as f:
        item_data = json.loads(f.read())
except:
    item_data  ={}
 
@app.post("/api/upload/")
async def upload_file(uploaded_file: Optional[UploadFile] = File(default="",title="Картинка с пожаром")):
    file_location = f"files/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    ff = fire.Fire(file_location)
    ff.add([18, 50, 50],[35, 255, 255] )
    result = []
    for i in ff.find():
        result.append(i)
    try:
        os.remove(file_location)
    except:
        pass
    return {"result": result}


@app.post("/api/math_graph")
def math_graph(_from:str, _to:str, _block:list):
    global item_data
    nodes = []
    init_graph = {}
    for i in item_data["items"]:
        
        if i["from"] not in nodes and i["from"] not in _block:
            nodes.append(i["from"])
        if i["to"] not in nodes and i["to"] not in _block:
            nodes.append(i["to"])
    for node in nodes:
        init_graph[node] = {}
    for i in item_data["items"]:
        if i["from"] not in nodes or i["to"] not in nodes:
            continue
        init_graph[i["from"]][i["to"]] = i["value"]
    _graph = graph.Graph(nodes, init_graph)
    previous_nodes, shortest_path = graph.dijkstra_algorithm(graph=_graph, start_node=_from)
    result = graph.print_result(previous_nodes, shortest_path, start_node=_from, target_node=_to)
    return {
        "result":result
    }

@app.post("/api/update")
def update_data(items:Items):
    global item_data
    item_data =json.loads(str(items))
    with open("data.json","w") as f:
        f.write(str(items))
    return {
        "state":1
    }

@app.post("/api/get",response_model=Items)
def get_data():
    return item_data
