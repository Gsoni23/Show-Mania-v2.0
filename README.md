# Project: Show-Mania-v2.0

Welcome to Your Project Name! This project involves multiple components, including a Flask web application and Vue.js frontend. To start the project, follow these steps:

## Prerequisites

Before you begin, ensure you have the following prerequisites installed:

- Python 3.x
- Redis (for Celery)
- Node.js (for Vue.js)

## Getting Started

1. First, navigate to the `Web_app` directory of the project:

   ```bash
   cd Web_app
   
2. Start the Flask application by running the following command:
  
   ```bash
   python main.py

3. In Windows Subsystem for Linux (WSL), start the Redis server with the following command:

   ```bash
   service redis-server start
   
4. Return to the Web_app directory:

   ```bash
   cd Web_app

5. Start the Celery worker server by running:

   ```bash
   celery -A main:cel worker -l INFO -P gevent

6. Open another terminal and start the Celery beat server:

   ```bash
   celery -A main:cel beat -l INFO

7. Ensure that all four servers are running properly: Flask server, Redis server, Celery worker server, and Celery beat server.

8. Now, navigate to the frontend directory:

   ```bash
   cd ../frontend

9. Start the Vue.js development server by running:

   ```bash
   npm run dev

10. You can now access the website at localhost:5173 and explore the project.

 Congratulations! You have successfully started the project with all the necessary servers running.
 
