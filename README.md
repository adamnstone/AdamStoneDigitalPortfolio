# AdamStoneProgrammingPortfolio
This is Adam Stone's computer programming portfolio of my favorite projects that I have created.

# 1] ReportingConsolidator

A laundromat chain wanted to automate data collection and dispersal about sales and other statistics in their stores. Several emails would come through with different statistics in varying formats (from HTML to plan text to .rtf files, etc.) that come from all different systems (emails, websites, text/csv files, etc.), and employees would sift through the data, transfer select pieces of information into Zoho Sheets and Google Sheets, and send a summary email to the owners. This program also generates graphs that help analyze customer trends. Using Python 3, I created a program that automates all of these processes, and it is still running to help this business. Additionally, I learned how to authenticate and use multiple APIs (Zoho Sheets, Google Sheets, etc.), retrieve and send emails via SSL, graph with MatPlotLib, webscrape with BeautifulSoup, and much more. I originally ran the program on a Linux server at my home, but for security reasons with port-forwarding and risk of power outages, I decided to rent a VM (Virtual Machine) Linux Debian server from Google Cloud (console.cloud.google.com) and set up the program there. (I have also changed all sensititve information into "XXXXXX" in the code in this repo for security purposes).

# 2] ChessAI

I am not exceptional at chess, so I decided to create an AI that plays chess using C# and the Unity game engine. This program uses a minimax algorithm with alpha-beta pruning and varying fitness functions, as well as recursion and back-tracing, to play chess at a superhuman level.

# 3] LaundromatMachineSystem

For the same laundromat chain as my "ReportingConsolidator" project, I needed to create a system that allows employees to turn on washing machines from their phones, tracks which washing machines that have been turned on by customers and employees and the number of activations, and provide a secure website where business owners can access this information. The API/Website is a Python3 program with a Flask framework that tracks incoming POST requests that carry data about which machines have been activated and by whom. It also hosts a website where this information is privately displayed. Next, in each washing machine, a RaspberryPi hosts an API on the local network (also using Python3 and Flask) that sends out signals to various GPIO ports (using the RPi.GPIO library) that turn on the washing machine. It also sends a signal to the overarching API that tracks activations. Lastly, I used Unity to create an android app that allows employees to turn on the machines. On the app, the employees can either scan a QR code (that corresponds to each RaspberryPi's local, public IP address) or type it in manually. Then, they can adjust several settings on the wash and click a button that sends an HTTP request to the RaspberryPi's local API, initiating the sequence I described previously. (For this project, I also blurred out sensitive information).

Here is a link to a video demonstration of this project: https://drive.google.com/file/d/1n6fg-BSeNWjQV3yXyDuWa8qOCz46Z9AU/view?usp=sharing

# 4] ProgrammingLanguageTranspilerGenerator

I love creating esoteric programming languages, so I built a tool using C/C++ that creates programming languages out of user-specified parameters. First, the user creates a ".tdsn" file where they lay out parameters for their language (see "example/example.tdsn"). Then, the program generates an EXE file that acts as a transpiler for their languages (all user-defined programming languages compiled, not interpreted, because they transpile to C++ and are then compiled and run as an EXE). Next, the user can either:
- Write a program in their language and use the command "example_transpiler.exe to file_in_their_language.example output_destination.exe" (see "example/create_transpiler.bat"). This will compile and run a program they wrote in their language.
- Take a C++ program they have written and transpile it into their own programming language using the command "example_transpiler.exe from cpp_file_they_wrote.cpp output_destination.example" (see "example/create_transpiler.bat").
I also provided an example where I made a programing language similar to Emojicode called "Emojicode++" (see the "Emojicode++" folder).

# 5] YoutubeRater

I am always worried that my two younger brothers will come across inappropriate content on Youtube, so I programmed a chrome extension (with HTML, JS, and CSS) and a website (HTML, JS, and CSS) with a Python 3 backend (using the Flask framework) that blocks inappropriate content. The kids install the chrome extension on their devices, and parents create an account for each child. They input what the child is allowed to watch (by listing bad words that the kids are not allowed to hear). Then the chrome extension uses the child's google account information to look up the settings the parent has applied for the child. Then, everytime the child watches a youtube video, it sends an API request for the video's transcription, and if bad words are found, it disables the video and notifies the parent. The parent can configure email notification settings for different "levels of badness" for different words. The fontend GUI of this project is not completely finished, but everything else is working perfectly.

# 6] DebateEvidenceFinder

In debate, there is a "wiki" page where students somtimes upload their arguments. I wanted to find the most efficient way of collecting evidence, so I created a program that scans the "wiki" for all pieces of evidence that debaters use in their cases, creates a database storing all of this information, and hosts a search-engine website where you can search keywords and it will bring up all evidence related to your search. You can then download this evidence as a word file or preview it in the browser. Also, all users are required to sign up for an account using their emails. This way, the search engine can be sold as a service for profit. Additionally, I implemented different password-authentication and reset features that can be seen in the code. I used HTML, JS, and CSS for the frotend, and a Python3 backend using the Flask framework. 
When you first run this file, it will start downloading cases from the "wiki." I have configured it so that it will stop after a couple of documents, because it would take years to download everything from the "wiki."

# 7] WordleWebsiteGenerator

With the massive success of the recent Wordle trend, I decided to program my own version of Wordle. Unfortunately, created one Wordle game alone is time consuming, so if I wanted to make multiple versions, it would be unmanagable. Thankfully, I made a program that lets you specify the number of letters and word bank, and it will generate a Python3 Flask app with HTML, JS, and CSS frontend. To use this program, import the "generate_wordle()" function from the module generate_wordle.py, and call the function with the specified parameters. Doing so will create a new directory with a full-fledged Flask application. Then, run the "main.py" file from inside this newly-created directory and type the URL that it logs into a search engine. This directory can also be put on a web server and the website can be accessed from any computer or network.

# 8] ZoomFaker

During COVID, we have all been bored out of our minds on Zoom meetings. Luckily, I created ZoomFaker, a program that lets you display a fake, looping video of yourself instead of your live camera feed on a Zoom meeting. For this program to run, you also need to install OBS studio. To use this program, you have to start running the Python 3 file (or compiled EXE). Then, open a Zoom meeting. Briefly turn off your video. Click the "b" key on your keyboard to begin recording yourself, and select the "OBS virtual camera" video input device. This lets you turn your camera on while recording. When you are done recording yourself, click "s" and the recording will automatically start playing instead of your camera feed. If you need to switch back (for example, if someone asks you a question on the meeting), you can simply change your video input device back to your computer's camera, then go back to the virtual camera to continue the recording. Also, clicking "f" toggles the flip-recording setting. If this setting is on, the video you recorded will play forward then backwards seamlessly, so that there is no cut when the recording ends. Lastly, pressing "p" starts the recording over from the beginning, and "r" deletes the current recording. (Also this projcet is not limited to Zoom - it will function on all virtual meeting platforms where you can change your video input source).

# 9] GoogleMeetAutomation

I was fully virtual during my 8th grade year of school because of COVID. Because I didn't want to be late to my classes, I created a Python3 program using the library PyAutoGUI that automatically opens google chrome whenever it is time for class, types in the URL for Google Meet, enters the class code based on the time of day it is, and logs onto the meeting.

# 10] JPGInject

As I was researching different types of encoding for different impact formats (.jpg, .png, etc.), I learned that, in a JPG file, program ignore all text after a certain flag. Therefore, information can be stored there unbeknownst to users, and the image will still function well. So, it is possible to embed text, code, and even other JPGs in JPG files. I created a program using the Tkinter Python3 library for that lets users select a programming language and embed code in a JPG/run code from a JPG that has already been embeded with code. (Also, a "g++" (cpp compiler) must be installed if you plan to embed C++ in JPG files).

# 11] NinjaCube

Unlike my other Unity project, "ChessAI," this game was more focused on graphics, controls, and GUI rather than backend functionality. This is simply an indie game I created where you are playing as a little cube trying to collect coins and kill enemies. The tutorial is self-explanatory.

# 12] RobotArm

As my final personal project in my Innovation & Design II class, I created a 3D printed robot arm controlled via Arduino and an Android app that communicates over Bluetooth. The app, built with MIT App Inventor, lets users connect to the robot arm, and they can then control where the robot moves, as well as open and close the grabber.

Here is a link to a video demonstration of this project: https://drive.google.com/file/d/13n5guYjNXJcvuO59gaFe6DnuKAseFgSW/view?usp=sharing
