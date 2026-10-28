from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import Session

from models import Base, User, Post

engine = create_engine("sqlite:///app.db", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    user = User(username="ivan", email="ivan@mail.ru", bio="студент")
    session.add(user)
    session.commit()
    print("создали юзера:", user.id)

    users = [
        User(username="alice", email="alice@mail.ru"),
        User(username="bob", email="bob@mail.ru"),
    ]
    session.add_all(users)
    session.commit()

    post = Post(title="первый пост", body="какой-то текст", user_id=user.id)
    session.add(post)
    session.commit()
    print("создали пост")

with Session(engine) as session:
    user = session.get(User, 1)
    print("нашли по id:", user.username)

    stmt = select(User).where(User.username == "alice")
    user = session.execute(stmt).scalar_one_or_none()
    print("нашли alice:", user)

    stmt = select(User)
    users = session.execute(stmt).scalars().all()
    print("всего юзеров:", len(users))

with Session(engine) as session:
    user = session.get(User, 1)
    if user:
        user.bio = "уже не студент"
        session.commit()
        print("обновили bio")

    stmt = update(User).where(User.email.like("%@mail.ru")).values(bio="новый bio")
    session.execute(stmt)
    session.commit()

with Session(engine) as session:
    user = session.get(User, 2) 
    if user:
        session.delete(user)
        session.commit()
        print("удалили alice")

    stmt = delete(User).where(User.username == "bob")
    session.execute(stmt)
    session.commit()
    print("удалили bob")

print("готово и четко")
