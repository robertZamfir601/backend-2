from ..db.db import database, User, Website, Product, CartedProd
from app.backend.utils import get_password_hash

async def add_user():
    True
    ### This is for clean up, DELETES all tables ###
    await CartedProd.objects.delete(each=True)
    await Product.objects.delete(each=True)
    await Website.objects.delete(each=True)
    await User.objects.delete(each=True)
    
    u1 = await User.objects.get_or_create(email="andrei@test.com", password=get_password_hash("andrei"))
    b = await User.objects.get_or_create(email="bogdan@test.com", password=get_password_hash("bogdan"))
    ds = await User.objects.get_or_create(email="dragoS@test.com", password=get_password_hash("dragoS"))
    da = await User.objects.get_or_create(email="drAgos@test.com", password=get_password_hash("drAgos"))
    l = await User.objects.get_or_create(email="lucian@test.com", password=get_password_hash("lucian"))
    r = await User.objects.get_or_create(email="robert@test.com", password=get_password_hash("robert"), token="")


    ### websites in here ###
    emag = await Website.objects.get_or_create(base_url="https://www.emag.ro/search/", name="emag", category="All")
    pc_garage = await Website.objects.get_or_create(base_url="https://www.pcgarage.ro/", name="pc-garage", category="IT")

    ### products emag here ###
    p1 = await Product.objects.get_or_create(website_id=emag[0], product_name="Laptop Lenovo", category="IT", 
                                        image="https://s13emagst.akamaized.net/products/44251/44250473/images/res_2eb9525bba64a13da8e95b10335115f7.jpg",
                                        price="1.598,17")
    p2 = await Product.objects.get_or_create(website_id=emag[0], product_name="Laptop Apple", category="IT", 
                                        image="https://s13emagst.akamaized.net/products/41188/41187834/images/res_4c98933b07a8fd01207cc338b1e2d225.jpg",
                                        price="9.899,99")
    p3 = await Product.objects.get_or_create(website_id=emag[0], product_name="Masina de spalat rufe", category="House", 
                                        image="https://s13emagst.akamaized.net/products/32582/32581589/images/res_7379489e021c4df6b1c82cb9270ddbfd.jpg",
                                        price="2.579,99")


    ## products pc-garage here ###
    p4 = await Product.objects.get_or_create(website_id=pc_garage[0], product_name="Monitor LED ViewSonic", category="IT", 
                                        image="https://4.grgs.ro/images/products/1/8561/2541843/full/gaming-xg2431-238-inch-fhd-ips-05-ms-240-hz-hdr-freesync-blur-busters-approved-20-e44ff332e4f3e411d630dd9b34ccd2f1.jpg",
                                        price="1.499,99")
    p5 = await Product.objects.get_or_create(website_id=pc_garage[0], product_name="Monitor LED GIGABYTE", category="IT", 
                                        image="https://2.grgs.ro/images/products/1/2216/2531995/full/gaming-m28u-ae-28-inch-uhd-ips-1-ms-144-hz-usb-c-hdr-freesync-premium-pro-ac94fc1a5d9eb096ec28bc264d821713.jpg",
                                        price="3.757,98")
                                        
    ### add products in users carts here ###
    await CartedProd.objects.get_or_create(user_id=r[0], product_id=p1[0])
    await CartedProd.objects.get_or_create(user_id=r[0], product_id=p2[0])
    await CartedProd.objects.get_or_create(user_id=r[0], product_id=p3[0])
    await CartedProd.objects.get_or_create(user_id=r[0], product_id=p4[0])
