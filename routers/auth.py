from fastapi import APIRouter


router = APIRouter()

@router.get('/auth')
async def get_user():
    return {'message': 'User authenticated successfully'}
