from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, sessionlocal, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='fastapi', 
                            user='postgres', password='tnpdnem12', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection success!')
        break
    except Exception as error:
        print('Connection Failed')
        print('Error', error)
        time.sleep(2)    




my_posts = [
    {'title': 'title of post 1',
    'content': 'content of post1',
    'id': 1},
    {'title': 'favorite of post 2',
    'content': 'pizza 2',
    'id': 2}
]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get('/')
def root():
    return {'message': "hello world"}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT IN TO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    #better way
    new_post = models.Post(**post.dict())

    #new_post = models.Post(title = post.title, content = post.content, published = post.published)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'data': new_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""select * from posts where id = %s  RETURNING * """, (str(id), ))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")
                                
    return {'post_detail': post}


@app.delete('/posts/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    #cursor.execute("""delete * from posts where id = %s RETURNING * """, str((id), ))
    #delete_post =cursor.fetchone()
    #conn.commit()
    delete_post = db.query(models.Post).filter(models.Post.id == id)

    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f" post with {id} does not exist")

    delete_post.delete(synchronize_session= False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post, db: Session = Depends(get_db)):

    #cursor.execute("""UPDATE posts set title = %s, content= %s, published = %s where id = %s """, (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f" post with {id} does not exist")
    
    post_query.update(post.dict(), synchronize_session= False)

    db.commit()
    
    return {'data': post_query.first()}


