from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
from fastapi.routing import APIRouter
import uuid


mongo_uri = "mongodb+srv://amanvivekanand:aman994909@cluster0.nszektx.mongodb.net/"
api_router = APIRouter()