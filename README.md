# CodeWiz Search Engine
Welcome to the CodeWiz Search Engine repository! This project provides a web application that allows users to search for coding questions and find relevant answers from various online coding platforms. Currently, it supports searching questions from LeetCode (LC) and Codeforces (CF), but it can be expanded to include other platforms in the future.

## Prerequisites
Before building the code locally, ensure that you have the following prerequisites installed on your machine:

1. Python (version 3.6 or above)
2. Flask (Python package)
3. Visual Studio Code (or any preferred code editor/IDE)
4. Google Chrome browser (latest version)
5. Chrome WebDriver (latest version)

Please make sure to have the latest version of Google Chrome browser and Chrome WebDriver installed on your machine. The Chrome WebDriver version should match the Chrome browser version to ensure compatibility.
You can download the latest version of Chrome WebDriver from the official Selenium website (https://www.selenium.dev/documentation/webdriver/driver_requirements/). Choose the appropriate WebDriver version based on your Chrome browser version and install it on your machine.

## Getting Started
1. Clone this repository to your local machine using the following command:
`git clone https://github.com/viralBot/cp-search-engine.git`

2. Open the project directory in your preferred code editor/IDE, such as Visual Studio Code.

3. Install the required Python packages using pip. Run the following command:
`pip install -r requirements.txt`
This will install the necessary packages, including Selenium, Flask, Flask-WTF, chardet, and bs4.

4. Next, we need to scrape questions from LeetCode and Codeforces. Run the following command to scrape the questions:
`python leetcode_scrape.py`
This will scrape the question titles and problem statements from both platforms. Make sure you are in the correct directory(LC_SCRAPE in this case) before running the command.

5. Next, filter the relevant information by running the cleaner script:
`python lc_cleaner.py`
The cleaner script will process the scraped data and filter out the relevant information.

6. After cleaning the data, run the explore script to store the filtered question data into separate question files:
`python lc_explore.py`
The explore script will store the filtered question data, URLs, and titles in the QDATA folder.

7. Repeat the same process for scraping cf questions(Running codeforces_scrape.py in the CF_SCRAPE folder and when it finishes, running the cf_explore.py script)

**Note**: The exploring process might take a while as it involves processing a large amount of data.

8. Now, we need to create the TF-IDF data required for searching. Run the prepare script:
`python prepare.py`
The prepare script will generate the TF-IDF values, including vocabulary, documents, inverted indices, and IDF values for both LeetCode and Codeforces question data.

9. Finally, run the Flask app using the following command in the terminal:
`flask --app app run`
Wait for about a minute, and then the Flask app will run on the development server.
Open your web browser and navigate to the generated link (e.g., http://127.0.0.1:5000) to access the application.

## Contributing
If you'd like to contribute to the CodeWiz Search Engine project, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make your changes in the branch and commit them.
4. Push the branch to your forked repository.
5. Submit a pull request to the main branch of the original repository, describing your changes in detail

**Thank you for your interest in our project! Happy coding!**
