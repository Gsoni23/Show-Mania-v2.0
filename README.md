First cd into Web_app and start main.py by command python main.py
start redis server in WSL using command "service redis-server start"
then again go in web_app and start celery worker server by command "celery -A main:cel worker -l INFO -P gevent"
then make another terminal and start celery beat server by command "celery -A main:cel beat -l INFO"

Now make sure all 4 servers running properly that is flask server, redis server, celery worker server, celery beat server

now go to frontend and start vue server by command "npm run dev"
now you can go to website "localhost:5173" and boom you started the project properly.