from fastapi import APIRouter, Depends
from app.api.deps import get_current_user, require_role
from app.models.user import UserRole, User

router = APIRouter()


@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
    }


@router.get("/admin-only")
def admin_only(
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    return {"message": "Welcome Admin"}
