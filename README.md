# AdamStoneProgrammingPortfolio
This is Adam Stone's computer programming portfolio of my favorite projects that I have created.

# 1] Reporting Consolidator

A laundromat chain wanted to automate data collection and dispersal about sales and other statistics in their stores. Several emails would come through with different statistics, and an employees would sift through the data, transfer select pieces of information into ZohoSheets, and send a summary email to the owners. This program also generates graphs that help analyze customer trends. Using Python 3, I created a program that automates all of these processes, and it is still running to help this business. (I have also changed all sensititve information into either environment variables or "XXXXXX" in the code for security purposes).

# 2] ChessAI

I am not exceptional at chess, so I decided to create an AI that plays chess using C# and the Unity game engine. This program uses a minimax algorithm with alpha-beta pruning and varying fitness functions to play chess at a superhuman level.

# 3] ProgrammingLanguageTranspilerGenerator

I love creating esoteric programming languages, so I built a tool using C/C++ that creates programming languages out of user-specified parameters. First, the user creates a ".tdsn" file where they lay out parameters for their language (see "example/example.tdsn"). Then, the program generates an EXE file that acts as a transpiler for their languages (all user-defined programming languages compiled, not interpreted, because they transpile to C++ and are then compiled and run as an EXE). Next, the user can either:
- Write a program in their language and use the command "example_transpiler.exe to file_in_their_language.example output_destination.exe" (see "example/create_transpiler.bat"). This will compile and run a program they wrote in their language.
- Take a C++ program they have written and transpile it into their own programming language using the command "example_transpiler.exe from cpp_file_they_wrote.cpp output_destination.example" (see "example/create_transpiler.bat").
I also provided an example where I made a programing language similar to Emojicode called "Emojicode++" (see the "Emojicode++" folder).
