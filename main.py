from fastapi import FastAPI
from basic_statistic import controller as bc
from semantic_search import contorller as sc
from dictionary_sentimental import controller as dc
from machine_learning_sentimental import controller as mc

app = FastAPI()

app.include_router(bc.router)
app.include_router(sc.router)
app.include_router(dc.router)
app.include_router(mc.router)
