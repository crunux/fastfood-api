## Store API



#Migrate DB

- Finally,running
```sh 
 alembic revision --autogenerate -m "your message"
```

- should generate a new .py file in versions folder with your changes.

```sh
 alembic upgrade head
```
or 
```sh
alembic stam head
```

- Applies your changes to DB.