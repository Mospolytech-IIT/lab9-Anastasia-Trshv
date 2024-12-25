import sqlalchemy
from sqlalchemy import create_engine
from models import Base, Post, User
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///lab9.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

user1 = User(username="Jack", email="email@mail.ru", password="111")
user2 = User(username="Arina", email="e@mail.ru", password="222")
user3 = User(username="Nastya", email="em@mail.ru", password="333")
db.add_all([user1, user2, user3])
db.commit()

post1 = Post(title="Title", content="content", user_id=1)
post2 = Post(title="Title", content="content", user_id=2)
post3 = Post(title="Title", content="content", user_id=3)
db.add_all([post1, post2, post3])
db.commit()


#Извлечение данных
print(f"Все пользователи:\n")
users = db.query(User).all()
for user in users:
    print(f"{user.id}, {user.username}, {user.email}, {user.password}")
print(f"\n")

print(f"Все посты:\n")
results = db.query(Post, User).join(User, User.id == Post.user_id).all()
for post, user in results:
    print(f"Post: {post.id}, {post.title}, {post.content} User: {post.user_id}, {user.username}, {user.email}")
print(f"\n")

print(f"Все посты пользователя 1:\n")
posts = db.query(Post).where(Post.user_id == 1).all()
for post in posts:
    print(f"{post.id}, {post.title}, {post.content}")
print(f"\n")

#Обновление данных
print(f"Обновление почты пользователя:\n")
updating_user = db.query(User).filter(User.id == 1).first()
print("Старая почта: " + updating_user.email)
updating_user.email = "mmm@mail.ru"
db.commit()
print("Новая почта: " + updating_user.email + "\n")

print(f"Обновление контента поста:\n")
updating_post = db.query(Post).filter(Post.user_id == 2).first()
print("Старый контент: " + updating_post.content)
updating_post.content = "newcontent"
db.commit()
print("Новый контент: " + updating_post.content + "\n")


#Удаление данных
print("Удаление поста 3: \n")
del_post = db.query(Post).filter(Post.id == 3).first()
db.delete(del_post)
db.commit()
results = db.query(Post, User).join(User, User.id == Post.user_id).all()
for post, user in results:
    print(f"Post: {post.id}, {post.title}, {post.content} User: {post.user_id}, {user.username}, {user.email}")
print(f"\n")


print("Удаление пользователя 1 и его постов: \n")
del_user = db.query(User).filter(User.id == 1).first()
posts = del_user.posts
for post in posts:
    db.delete(post)
db.delete(del_user)
db.commit()
print(f"Все пользователи:\n")
users = db.query(User).all()
for user in users:
    print(f"{user.id}, {user.username}, {user.email}, {user.password}")
print(f"\n")

print(f"Все посты:\n")
results = db.query(Post, User).join(User, User.id == Post.user_id).all()
for post, user in results:
    print(f"Post: {post.id}, {post.title}, {post.content} User: {post.user_id}, {user.username}, {user.email}")
print(f"\n")