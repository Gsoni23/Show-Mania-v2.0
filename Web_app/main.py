from Backend import create_app
from Backend.worker import create_celery_app

app = create_app()
cel = create_celery_app(app)

if __name__ == '__main__':
    app.run(debug = True)