from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/pics", StaticFiles(directory="pics"), name="pics")

@app.get("/", response_class=HTMLResponse)
async def hello_page(request: Request):
    with open("users.json", "r") as f:
        users = json.load(f)
    
    with open("locations.json", "r") as f:
        locations = json.load(f)
    
    with open("dates.json", "r") as f:
        dates = json.load(f)
    
    logged_in_user = request.cookies.get("login")
    
    return templates.TemplateResponse("hello.html", {
        "request": request,
        "users": users["users"],
        "locations": locations["locations"],
        "dates": dates["dates"],
        "logged_in_user": logged_in_user
    })

@app.post("/login")
async def login(user_data: dict, response: Response):
    with open("users.json", "r") as f:
        users = json.load(f)
    
    username = user_data.get("username")
    if username in users["users"]:
        response.set_cookie(key="login", value=username)
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid user"}

@app.post("/date")
async def update_date(date_data: dict):
    day = date_data.get("day")
    user = date_data.get("user")
    
    with open("dates.json", "r") as f:
        dates = json.load(f)
    
    if day in dates["dates"]:
        if user in dates["dates"][day]:
            dates["dates"][day] = [x for x in dates["dates"][day] if x != user]
        else:
            dates["dates"][day].append(user)
    
    with open("dates.json", "w") as f:
        json.dump(dates, f)
    
    return dates

@app.post("/location")
async def add_location(location_data: dict):
    location = location_data.get("location")
    
    with open("locations.json", "r") as f:
        locations = json.load(f)
    
    if location and location not in locations["locations"]:
        locations["locations"].append(location)
    
    with open("locations.json", "w") as f:
        json.dump(locations, f)
    
    return locations

