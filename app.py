import os
from datetime import timedelta, datetime
from typing import List

import aiofiles
import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, UploadFile, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseSettings
from sqlalchemy.orm import Session
from tensorflow.keras.preprocessing.image import load_img

from model.base import Base, engine
from model.meal import Meal
from model.prediction import Prediction
from model.user import Token, User
from repository.repository import DbMealRepository
from repository.user_repository import DbUserRepository
from utils.auth_utils import authenticate_user, create_access_token, get_current_user, get_password_hash
from utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.dependencies import get_crypt_context, get_db, get_meal_db, get_model, get_user_db


class Settings(BaseSettings):
    uploadLocation: str = 'C:\\Users\\RADU\\Desktop\\food-api\\input_images'

Base.metadata.create_all(bind=engine)

settings = Settings()

app = FastAPI()
classes = []


def getClasses():
    with open("classes.txt") as f:
        for string in f.readlines():
            food_details = string.strip().split(',')
            food_name = food_details[0]
            food_name_prettified = " ".join([f'{substr[0].upper()}{substr[1:].lower()}' for substr in food_name.split("_")])
            classes.append(Prediction(food_name_prettified, kcal=int(food_details[1]), carbs=int(food_details[2]), protein=int(food_details[3]), fat=int(food_details[4])))

getClasses()

@app.post("/uploadfile/")
async def predict(
        file: UploadFile,
        model=Depends(get_model)
):
    try:
        async with aiofiles.open(os.path.join(settings.uploadLocation, file.filename), 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)
            img = np.array(load_img('\\'.join([settings.uploadLocation, file.filename])))
            img = cv2.resize(img, (224, 224))
            x = model.predict(np.array([img]))[0]
            index = np.argmax(x)
            prediction = classes[index]
            if x[index] < 0.6:
                raise HTTPException(status_code=400, detail="Food not detected")
            rez = prediction.to_map()
    finally:
        os.remove(os.path.join(settings.uploadLocation, file.filename))
    return rez


@app.post("/login", response_model=Token)
async def login_for_access_token(user: User,
                                 db: Session = Depends(get_db),
                                 users_repo: DbUserRepository = Depends(get_user_db), 
                                 crypt_context: CryptContext = Depends(get_crypt_context)):
    user = authenticate_user(db, users_repo, user.username, user.password, crypt_context)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}


@app.post("/register", response_model=Token)
async def register_for_access_token(user: User,
                                    db: Session = Depends(get_db),
                                    users_repo: DbUserRepository = Depends(get_user_db),
                                    crypt_context: CryptContext = Depends(get_crypt_context)
                                    ):
    user.password = get_password_hash(crypt_context, user.password)
    user = users_repo.add_user(db, user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}

@app.get("/meal", response_model=List[Meal])
async def get_meals(datetime: datetime, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), meal_repo: DbMealRepository = Depends(get_meal_db)) -> List[Meal]:
    return meal_repo.filter_by_date(db, datetime, current_user)

@app.post("/meal")
async def add_meal(
        meal: Meal,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        meal_repo: DbMealRepository = Depends(get_meal_db)):
    meal.user = current_user
    meal_repo.add(db, meal)
