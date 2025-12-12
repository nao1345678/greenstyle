from typing import List
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from models.user import User, UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
async def create_user(payload: UserCreate) -> UserOut:
    payload.hash_password()
    user = User(**payload.model_dump())
    await user.insert()
    return UserOut(id=str(user.id), username=user.username, firstname=user.firstname, email=user.email)


@router.get("/", response_model=List[UserOut])
async def list_users() -> List[UserOut]:
    users = await User.find_all().to_list()
    return [UserOut(id=str(u.id), username=u.username, firstname=u.firstname, email=u.email) for u in users]


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: PydanticObjectId) -> UserOut:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(id=str(user.id), username=user.username, firstname=user.firstname, email=user.email)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: PydanticObjectId, data: UserUpdate) -> UserOut:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.password:
        data.hash_password()

    await user.set(data.model_dump(exclude_unset=True))
    return UserOut(id=str(user.id), username=user.username, firstname=user.firstname, email=user.email)


@router.delete("/{user_id}")
async def delete_user(user_id: PydanticObjectId) -> dict:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    return {"message": "User deleted"}
