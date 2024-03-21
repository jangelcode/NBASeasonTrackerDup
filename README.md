NBAWebApp
Welcome to NBAWebApp, a Flask-based web application designed for NBA enthusiasts. This app provides real-time information and statistics for NBA teams, along with features like playoff status checks, next game schedules, team rankings, and a playoff outcome simulator.

Features
Team Information: Access detailed statistics and information about any NBA team, including performance metrics and standings.
Playoff Status: Check whether your favorite team is set to make the playoffs, participate in the play-in tournament, or miss the playoffs.
Next Game Schedule: Find out when your favorite team's next game is and who they will be playing against.
Team Rankings: View current NBA team rankings based on win-loss records.
Simulate Playoffs: Utilize our simulation tool to predict the outcome of the playoffs using current team data.
Tech Stack
Frontend: HTML, Bootstrap
Backend: Flask
Database: PostgreSQL
APIs: External NBA-related APIs for fetching real-time data
Setup and Installation
Ensure you have Python 3.8+, pip, and PostgreSQL installed on your machine.

Clone the repository:
bash
Copy code
git clone <repository-url>
cd NBAWebApp
Create a Python virtual environment and activate it:
On Unix or MacOS:
bash
Copy code
python3 -m venv env
source env/bin/activate
On Windows:
bash
Copy code
python -m venv env
.\env\Scripts\activate
Install the required Python packages:
bash
Copy code
pip install -r requirements.txt
Set up the PostgreSQL database:
Update the app.py and database.py with your PostgreSQL credentials.

Run the application:
bash
Copy code
flask run
Navigate to http://127.0.0.1:5000/ in your web browser to access the application.

Running Tests
This project includes unit tests for various components. To run the tests, navigate to the project directory and execute:

bash
Copy code
pytest
Make sure to configure your test environment correctly, referring to the test files for any specific setup.

Contributing
Contributions to NBAWebApp are welcome! Feel free to fork the repository, make changes, and submit pull requests. If you're suggesting new features or changes to existing functionality, please open an issue for discussion.

License
This project is licensed under the MIT License - see the LICENSE.md file for details.
