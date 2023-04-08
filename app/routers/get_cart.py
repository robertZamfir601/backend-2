from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from ..db.db import database, User, CartedProd, Product, Website

router = APIRouter()
##https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/


@router.post("/get_cart")
async def get_cart(payload: dict):
    username = payload['username']
    sites = payload['sites']
    order = payload['order']
    token = payload['token']
    
    # # Verificăm dacă utilizatorul este autentificat
    # # if not validate_cookie(cookie):
    # #     raise HTTPException(status_code=401, detail="Not logged in")
    
    if order not in ['PriceDesc', 'PriceCresc']:
        return JSONResponse(content={
        "code": "2",
        "msg": "querry params are bad",
    })

    webs = await Website.objects.all()
    websites = [web.name for web in webs]

    count = 0
    for string in sites:
        if string not in websites:
            count = count + 1

    if count == len(sites):
        return JSONResponse(content={
        "code": "1",
        "msg": "querry params are bad",
    })
    
    #
    # Obținem produsele din baza de date
    user = await User.objects.get(email=username)
    websites = await Website.objects.filter(name__in=sites).all()
    website_ids = [web.id for web in websites]

    carted_prods = await CartedProd.objects.filter(user_id=user).all()
    product_ids = [p.product_id.id for p in carted_prods]

    carted_prods_json = []
    for curr_id in website_ids:
        products = await Product.objects.filter(website_id=curr_id, id__in=product_ids).all()
        website = await Website.objects.get(id=curr_id)
        carted_prods_json += [prod.to_json(website) for prod in products]

    if(order == 'PriceCresc'):
        carted_prods_json.sort(key=lambda x: float(x['price'].replace(',', '')))
    elif(order == 'PriceDesc'):
        carted_prods_json.sort(key=lambda x: float(x['price'].replace(',', '')), reverse=True)
    
    # product_ids = [p.id for p in products]
    #print(products[0])

    #products = await Product.objects.filter(website_id=website, id__in=product_ids).select_related("website_id").all()

    # carted_prods = await CartedProd.objects.filter(user_id=user, product_id__in=product_ids).all()

    # Returnăm un răspuns JSON
    return JSONResponse(content={
        "code": "0",
        "msg": "This is your product list",
        "products": carted_prods_json
    })