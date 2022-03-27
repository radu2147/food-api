import cv2
import os
from datetime import datetime
from datetime import timedelta
from typing import List

import aiofiles
import numpy as np
import uvicorn
from fastapi import FastAPI, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseSettings
from tensorflow.keras.preprocessing.image import load_img

from model.meal import Meal
from model.prediction import Prediction
from model.user import Token, User
from repository.repository import Repository
from repository.user_repository import UserRepository
from utils.auth_utils import authenticate_user, create_access_token, get_current_user
from utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.dependencies import get_meal_db, get_model, get_user_db


class Settings(BaseSettings):
    uploadLocation: str = 'C:\\Users\\RADU\\Desktop\\food-api\\input_images'



settings = Settings()

app = FastAPI()

classes = []


def getClasses():
    with open("classes.txt") as f:
        for el in f.readlines():
            classes.append(el.strip())


getClasses()


@app.get("/meal")
async def get_meals(datetime: datetime, current_user: User = Depends(get_current_user), meal_repo: Repository = Depends(get_meal_db)) -> List[Meal]:
    return meal_repo.filter_by_date(datetime, current_user)

@app.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/meal")
async def add_meal(meal: Meal, current_user: User = Depends(get_current_user), meal_repo: Repository = Depends(get_meal_db)):
    meal.user = current_user
    meal_repo.add(meal)


@app.delete("/meal/{id}")
async def delete_meal(id: int, _: User = Depends(get_current_user), meal_repo: Repository = Depends(get_meal_db)):
    meal_repo.remove(id)


@app.post("/uploadfile/")
async def predict(
        file: UploadFile,
        model=Depends(get_model)
):
    async with aiofiles.open(os.path.join(settings.uploadLocation, file.filename), 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)
        img = np.array(load_img('\\'.join([settings.uploadLocation, file.filename])))
        img = cv2.resize(img, (224, 224))
        x = model.predict(np.array([img]))[0]
        index = np.argmax(x)
        prediction = Prediction(float(x[index]), classes[index])
        rez = prediction.to_map()
    os.remove(os.path.join(settings.uploadLocation, file.filename))
    return rez


@app.post("/login", response_model=Token)
async def login_for_access_token(user: User,
                                 users_db: UserRepository = Depends(get_user_db)):
    user = authenticate_user(users_db, user.username, user.password)
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
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=Token)
async def register_for_access_token(user: User,
                                    users_db: UserRepository = Depends(get_user_db)):
    user = users_db.add_user(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(app, host="10.152.3.114", port=8000)
