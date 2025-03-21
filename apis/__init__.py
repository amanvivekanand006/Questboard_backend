from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel,EmailStr,Field
from typing import Optional,List
from fastapi.routing import APIRouter
import uuid
from fastapi.middleware.cors import CORSMiddleware


api_router = APIRouter()

mongo_uri = "mongodb+srv://amanvivekanand:aman994909@cluster0.nszektx.mongodb.net/"
