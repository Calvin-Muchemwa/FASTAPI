from fastapi import FastAPI ,Response,status,HTTPException
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


def find_post(id):
    for post in my_posts:
        if post['id']==id:
            return post

def find_post_index(id):
    for i , post in enumerate(my_posts):
        if post["id"]==id:
            return i


@app.get("/")
def read_root():
    return {"message": "Hello Worlds"}

@app.get("/posts")
def get_posts():
    return{"data":my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):##whatever data we giving api will be converted to python dict Body
    post_dict=post.dict();
    post_dict['id']=randrange(0,10000000)
    my_posts.append(post_dict);
    ##easily convert pydantic object to dict and add to our array
    return{"message":"Successfully added"} ##extracting data


@app.get("/posts/{id}")##This time we getting the path parameter id in order to retrieve the post
def get_post(id:int,response:Response):###id:int automatically validate it to int
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=404,detail=f"post with {id} does not exist")##raise error as exception, specify status code and detail message
       
    print(post)
    return{"post_detail":post}
    
            
@app.delete("/posts/{id}",status_code=204)
def delete_post(id:int):
    i=find_post_index(id)
    if not i:
        raise HTTPException(status_code=404,detail=f"post with {id} does not exist")
    my_posts.pop(i)
    return{"message":f"post with ID: {id} has successfully been deleted"}

@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)##put request when updating post
def update_post(id:int,post:Post):
    i=find_post_index(id)
    post_dict=post.dict()
    my_posts[i]=post_dict
    return{"message":"Post successfully updated"}