from fastapi.templating import Jinja2Templates
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import  FileResponse
from models import Base, User, Post

SQLALCHEMY_DATABASE_URL = "sqlite:///lab93.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base.metadata.create_all(bind=engine)


app = FastAPI()

templates = Jinja2Templates(directory="front")

def get_db():
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/get_users")
def get_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("AllUsers.html", {"request": request, "users": users})

@app.get("/create_user")
def get_create_user_page():
    return FileResponse("front/CreateUser.html")

@app.post("/users/create")
def add_user(username = Form(), email = Form(), password = Form(), db: Session = Depends(get_db)):
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return "Пользователь добавлен"

@app.get("/update_user")
def get_update_user_page():
    return FileResponse("front/UpdateUser.html")

@app.post("users/update")
def update_user(id = Form(), username = Form(), email = Form(), password = Form(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    user.username = username
    user.email = email
    user.password = password
    db.commit()
    db.refresh(user)
    return "Пользователь изменен"


@app.get("/users/delete/{id}")
def delete_user(id, db: Session = Depends(get_db)):
    id = int(id)
    del_user = db.query(User).filter(User.id == 1).first()
    posts = del_user.posts
    for post in posts:
        db.delete(post)
        db.delete(del_user)
        db.commit()       
    return "Пользователь удалён"



@app.get("/get_posts")
async def get_posts_page(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse("AllPosts.html", {"request": request, "posts": posts})

@app.get("/posts/get")
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()


@app.get("/create_post")
def get_create_post_page():
    return FileResponse("front/CreatePost.html")

@app.post("/posts/create")
def add_posts(title =Form(), content = Form(), user_id= Form(), db: Session = Depends(get_db)):
    post = Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return "Пост добавлен"

@app.get("/update_post")
def get_update_post_page():
    return FileResponse("front/UpdatePost.html")

@app.post("/posts/update")
def update_posts(id = Form(), title =Form(), content = Form(), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    post.title = title
    post.content = content
    db.commit()
    db.refresh(post)
    return "Пост изменён"


@app.get("/posts/delete/{id}")
def delete_posts(id , db: Session = Depends(get_db)):
    id = int(id)
    post = db.query(Post).filter(Post.id == id).first()
    db.delete(post)
    db.commit()
    return "Пост удалён"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)