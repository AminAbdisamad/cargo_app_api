from fastapi import APIRouter, Depends, HTTPException,Header


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


cargo = APIRouter(
    prefix="/cargo",
    tags=["cargo"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@cargo.get("/")
def get_cargo():
    return 'cargo list'
