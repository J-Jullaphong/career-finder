# Career Finder

Explore exciting career opportunities and find your dream job.

Join us today and take the next step in your career journey.

## Installation

> **NOTE:** For the commands below, if you have the "**zsh: command not found: python**" problem on **macOS**, please change "**python**" to "**python3**".

1. Clone the repository from GitHub.
   ``` 
   git clone https://github.com/J-Jullaphong/career-finder.git
   ```
   
2. Change directory to Career Finder.
   ``` 
   cd career-finder 
   ```
   
3. Create a virtual environment.
   ```
   python -m venv venv
   ```
   
4. Activate the virtual environment.
   - Linux and macOS
   ``` 
   source venv/bin/activate 
   ```
   - Windows
   ```  
   .\venv\Scripts\activate
   ```

5. Install Dependencies for required python modules.
   ```
   pip install -r requirements.txt
   ```

6. Run migrations to apply database migrations.
   ```
   python manage.py migrate
   ```

7. Install data from the data fixtures.
   ```
   python manage.py loaddata data/demo.json
   ```

## How to run

Before running the server, please make sure that the installation is completed.

1. Activate the virtual environment before using the application.
   - Linux and macOS
   ``` 
   source venv/bin/activate 
   ```
   - Windows
   ```  
   .\venv\Scripts\activate
   ```

2. Start the server. (If it doesn't work, please use `python3` instead of `python`)
   ```
   python manage.py runserver
   ```
   
3. To use this application, go to this link in your browser.
   ```
   http://localhost:8000
   ```

4. To close the running server, press `Ctrl+C` in your terminal or command prompt. 

5. After finish using the application, deactivate the virtual environment.
   ```
   deactivate
   ```
   
## Demo Users

Use these demo accounts to log in for testing.

|      Username      | Password  |
|:------------------:|:---------:|
|  **demo_seeker**   | @Demo_123 |
| **demo_recruiter** | @Demo_123 |
|  **demo_company**  | @Demo_123 |
