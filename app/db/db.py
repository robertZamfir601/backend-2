
import databases
import ormar
import sqlalchemy
import datetime
from .config import settings
from typing import Optional
import json

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "Users"

    id: int = ormar.Integer(primary_key=True, auto_increment=True)                                       # auto-increment automatically set to True
    email: str = ormar.String(max_length=100, unique=True, nullable=False)
    password: str = ormar.String(max_length=300, nullable=True, default="")        	# can have this of token_google, but not both
    token_google: str = ormar.String(max_length=300, nullable=True, default="")     # can have this of password, but not both
    creted_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)	# set to crt datetime each time you call an endpoint
    token: str = ormar.String(max_length=500, nullable=True, default="")

class Website(ormar.Model):
    class Meta(BaseMeta):
        tablename = "Websites"
    
    id: int = ormar.Integer(primary_key=True, auto_increment=True)
    base_url: str = ormar.String(max_length=500, nullable=False, unique=True)
    name: str = ormar.String(max_length=100, nullable=True)
    category: str = ormar.Text(nullable=False)
    xpath: str = ormar.Text(nullable=False)
    domain: str = ormar.String(max_length=100, nullable=True)
    country: str = ormar.Text(nullable=False) ##country where website is used or countrys where website is used all(for all countrys)

class Product(ormar.Model):
    class Meta(BaseMeta):
        tablename = "Products"

    id: int = ormar.Integer(primary_key = True, auto_increment=True)
    website_id: Optional[Website] = ormar.ForeignKey(Website)
    product_name: str = ormar.String(max_length = 300, nullable=False)
    category: str = ormar.String(max_length = 300, nullable=True)
    image: str = ormar.String(max_length = 1000, nullable = True)
    price: str = ormar.String(max_length = 30, nullable=False)

    def to_json(self, website):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'price': self.price,
            'image': self.image,
            'website_base_url': website.base_url if website is not None else None
        }
   
    

# ormar has a functionality to automatically create
# ManyToMany dependencies, we have to check it out
# in the future
class CartedProd(ormar.Model):
    class Meta(BaseMeta):
        tablename = "Carts"
    
    entry_id: int = ormar.Integer(primary_key = True, auto_increment=True)
    user_id: Optional[User] = ormar.ForeignKey(User)
    product_id: Optional[Product] = ormar.ForeignKey(Product)

    def to_json(self):
        return {
            'entry_id': self.entry_id,
            'user_id': self.user_id.id if self.user_id is not None else None,
            'product_id': self.product_id.id if self.product_id is not None else None
        }


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)