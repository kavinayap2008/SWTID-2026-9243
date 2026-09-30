from pathlib import Path

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)

from fastapi.templating import Jinja2Templates

from pydantic import ValidationError


from .database import (
    delete_user,
    get_all_users,
    get_original_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)

from .schemas import (
    FeedbackRequest,
    UserInput,
)

from .services.gemini_generator import (
    generate_workout_gemini,
)

from .services.gemini_flash_generator import (
    generate_nutrition_tip_with_flash,
)

from .services.updated_plan import (
    update_workout_plan,
)


# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------

router = APIRouter()


# ---------------------------------------------------------
# JINJA2
# ---------------------------------------------------------

templates = Jinja2Templates(
    directory=str(
        Path(__file__).parent / "templates"
    )
)


# ---------------------------------------------------------
# VALIDATION ERROR FORMATTER
# ---------------------------------------------------------

def _validation_message(
    exc: ValidationError,
) -> str:

    return "; ".join(
        f"{'.'.join(map(str, error['loc']))}: "
        f"{error['msg']}"
        for error in exc.errors()
    )


# =========================================================
# HOME PAGE
# =========================================================

@router.get(
    "/",
    response_class=HTMLResponse,
)
def home(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


# =========================================================
# GENERATE WORKOUT
# =========================================================

@router.post(
    "/generate-workout",
    response_class=HTMLResponse,
)
def generate_workout(
    request: Request,

    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):

    try:

        # -----------------------------------------------
        # VALIDATE INPUT
        # -----------------------------------------------

        data = UserInput(
            user_id=user_id,
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity.lower(),
        )

        # -----------------------------------------------
        # GENERATE WORKOUT
        # -----------------------------------------------

        plan = generate_workout_gemini(
            data.age,
            data.weight,
            data.goal,
            data.intensity,
        )

        # -----------------------------------------------
        # GENERATE NUTRITION TIP
        # -----------------------------------------------

        tip = generate_nutrition_tip_with_flash(
            data.goal
        )

        # -----------------------------------------------
        # SAVE USER
        # -----------------------------------------------

        save_user(
            **data.model_dump()
        )

        # -----------------------------------------------
        # SAVE PLAN
        # -----------------------------------------------

        save_plan(
            data.user_id,
            plan,
        )

        # -----------------------------------------------
        # DISPLAY RESULT
        # -----------------------------------------------

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": data,
                "workout_plan": plan,
                "nutrition_tip": tip,
                "updated": False,
            },
        )

    except ValidationError as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": _validation_message(exc)
            },
            status_code=422,
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(exc)
            },
            status_code=500,
        )


# =========================================================
# SUBMIT FEEDBACK
# =========================================================

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse,
)
def submit_feedback(
    request: Request,

    user_id: int = Form(...),
    feedback: str = Form(...),
):

    try:

        # -----------------------------------------------
        # VALIDATE FEEDBACK
        # -----------------------------------------------

        data = FeedbackRequest(
            user_id=user_id,
            feedback=feedback,
        )

        # -----------------------------------------------
        # GET USER
        # -----------------------------------------------

        user = get_user(
            data.user_id
        )

        # -----------------------------------------------
        # GET ORIGINAL PLAN
        # -----------------------------------------------

        original = get_original_plan(
            data.user_id
        )

        if not user or not original:

            raise HTTPException(
                status_code=404,
                detail=(
                    "No user/plan found "
                    "for that User ID."
                ),
            )

        # -----------------------------------------------
        # GENERATE UPDATED PLAN
        # -----------------------------------------------

        revised = update_workout_plan(
            original,
            data.feedback,
        )

        # -----------------------------------------------
        # SAVE UPDATED PLAN
        # -----------------------------------------------

        update_plan(
            data.user_id,
            revised,
            data.feedback,
        )

        # -----------------------------------------------
        # GENERATE NUTRITION TIP
        # -----------------------------------------------

        tip = generate_nutrition_tip_with_flash(
            user.goal
        )

        # -----------------------------------------------
        # SHOW RESULT
        # -----------------------------------------------

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "workout_plan": revised,
                "nutrition_tip": tip,
                "updated": True,
            },
        )

    except ValidationError as exc:

        raise HTTPException(
            status_code=422,
            detail=_validation_message(exc),
        ) from exc


# =========================================================
# ADMIN - VIEW ALL USERS
# =========================================================

@router.get(
    "/view-all-users",
    response_class=HTMLResponse,
)
def view_all_users(
    request: Request,
):

    users = get_all_users()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users
        },
    )


# =========================================================
# ADMIN - DELETE USER
# =========================================================

@router.post(
    "/delete-user/{user_id}"
)
def remove_user(
    user_id: int,
):

    delete_user(user_id)

    return RedirectResponse(
        url="/view-all-users",
        status_code=303,
    )


# =========================================================
# REST API
# =========================================================

@router.post(
    "/api/workouts"
)
def api_generate_workout(
    data: UserInput,
):

    try:

        plan = generate_workout_gemini(
            data.age,
            data.weight,
            data.goal,
            data.intensity,
        )

        tip = generate_nutrition_tip_with_flash(
            data.goal
        )

        save_user(
            **data.model_dump()
        )

        save_plan(
            data.user_id,
            plan,
        )

        return {
            "user": data.model_dump(),
            "workout_plan": plan,
            "nutrition_tip": tip,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


# =========================================================
# FEEDBACK API
# =========================================================

@router.post(
    "/api/feedback"
)
def api_feedback(
    data: FeedbackRequest,
):

    user = get_user(
        data.user_id
    )

    original = get_original_plan(
        data.user_id
    )

    if not user or not original:

        raise HTTPException(
            status_code=404,
            detail=(
                "No user/plan found "
                "for that User ID."
            ),
        )

    try:

        revised = update_workout_plan(
            original,
            data.feedback,
        )

        update_plan(
            data.user_id,
            revised,
            data.feedback,
        )

        return {
            "user_id": data.user_id,
            "updated_plan": revised,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


# =========================================================
# GET USERS API
# =========================================================

@router.get(
    "/api/users"
)
def api_users():

    users = get_all_users()

    return [
        {
            "user_id": user.id,
            "username": user.username,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,

            "original_plan":
                user.plan.original_plan
                if user.plan
                else None,

            "updated_plan":
                user.plan.updated_plan
                if user.plan
                else None,
        }

        for user in users
    ]