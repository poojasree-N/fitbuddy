from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from app.gemini_generator import generate_workout_gemini
from app.updated_plan import update_workout_plan
from app.database import SessionLocal
from app.models import User

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/all-users")
def all_users(request: Request):
    db = SessionLocal()
    users = db.query(User).all()
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"users": users}
    )


@router.post("/generate-workout")
def generate_workout(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    workout_plan = generate_workout_gemini(
        name, age, weight, goal, intensity
    )

    db = SessionLocal()

    user = User(
        name=name,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
        workout_plan=workout_plan
    )

    db.add(user)
    db.commit()

    user_id = user.id

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "name": name,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "user_id": user_id
        }
    )


@router.post("/update-plan")
def update_plan(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):
    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()

    updated_plan = update_workout_plan(
        user.name,
        user.age,
        user.weight,
        user.goal,
        user.intensity,
        feedback
    )

    user.workout_plan = updated_plan

    db.commit()

    name = user.name
    age = user.age
    weight = user.weight
    goal = user.goal
    intensity = user.intensity
    workout_plan = user.workout_plan

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "name": name,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "user_id": user_id
        }
    )