from fastapi import FastAPI 
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app=FastAPI()

my_posts=[{"title":"Title of Post 1","content":"content of post1","id":1},{"title":"Favourite Foods","content":"I like Pizza","id":2}]

class Post(BaseModel):## we use this class to define how our post properties (post schema) note extends BaseModel
    title:str
    content:str
    published:bool=True
    rating:Optional[int]=None

@app.get("/")
def read_root():
    return {"message": "Hello Worlds"}

@app.get("/posts")
def get_posts():
    return{"data":my_posts}

@app.post("/posts")
def create_posts(post:Post):##whatever data we giving api will be converted to python dict Body
    post_dict=post.dict();
    post_dict['id']=randrange(0,10000000)
    my_posts.append(post_dict);
    ##easily conver pydantic object to dict and add to our array
    return{"message":"Successfully added"} ##extracting data


@app.get("/posts/{id}")##This time we getting the path parameter id in order to retrieve the post
def get_post(id):
    for post in my_posts:
        if post['id']==2:
            print(post)

    return{"message":f"Printing out post with id : {id}"}
    
        