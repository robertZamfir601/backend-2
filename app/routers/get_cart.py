from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from ..db.db import database, User, CartedProd

router = APIRouter()
##https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/


@router.get("/get_cart")
async def get_cart():
    username = "robert@test.com"
    sites = ["emag"]
    order = "PriceDesc"
    # Verificăm dacă utilizatorul este autentificat
    # if not validate_cookie(cookie):
    #     raise HTTPException(status_code=401, detail="Not logged in")
    
    if order not in ["PriceDesc", "PriceCresc"]:
        raise JSONResponse(content={
        "code": "2",
        "msg": "querry params are bad",
    })

    my_list = ["emag", "pc-garage"]
    count = 0
    for string in sites:
        if string not in my_list:
            count = count + 1

    if count == len(my_list):
        raise JSONResponse(content={
        "code": "2",
        "msg": "querry params are bad",
    })
            
    # Obținem produsele din baza de date
    user = await User.objects.get(email="robert@test.com")
    carted_prods = await CartedProd.objects.filter(user_id=user).all()
    carted_prods_json = [prod.to_json() for prod in carted_prods]

    # Returnăm un răspuns JSON
    return JSONResponse(content={
        "code": "0",
        "msg": "This is your product list",
        "products": carted_prods_json
    })