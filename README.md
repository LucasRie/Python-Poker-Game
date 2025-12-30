This is a comprehensive Python-based simulation of Texus Hold'em Poker, featuring a graphical userinterface (GUI) and a statistical probability engine used to determine the action of bots. This project was developed as part of the Computer Science A-Level NEA. 

Disclaimner: This code is part of a formal assessment. If you are a student, do not copy this code for your own coursework. It is published here for portfolio and educational demonstration purposes only. Plagiarism checkers will identify this code. 

Overview:
This application simulates a full game of Texas Hold'em against three computer-controlled "Bots." Unlike simple console games, this project features a fully interactive GUI built with Tkinter. It manages complex game states including Pre-flop, Flop, Turn, and River betting rounds, and utilizes custom algorithms to determine hand strength and winner allocation.

The project focuses on object-oriented programming (OOP) principles, separating game logic, user authentication, and UI rendering.

Gameplay Features:
Single Player Mode: Play against 3 AI bots with unique betting behaviors.
Game Loop: Full implementation of Texas Hold'em stages (Pre-flop, Flop, Turn, River, Showdown).
Betting System: Support for Checking, Calling, Betting, Raising, and Folding.
Pot Management: accurate calculation of main pots and split pots

Logic and Algorithms Features:
Hand Evaluation: A robust algorithm that identifies hand rankings (from High Card to Royal Flush).
Statistical Tips: Real-time probability calculation advising the user on their hand's strength relative to possible opponent hands.
Custom Security: A unique hashing algorithm (using binary conversion and padding) to secure user passwords.

User Experience features:
User Accounts: Registration and Login system with persistent storage (JSON).
Leaderboard: Tracks user chip counts and displays top players.
Customization: Changeable color schemes (Green, Blue, Orange, Pink) and settings toggles.


Technologies Used:
Language: Python 3.12
GUI: Tkinter
Image Handling: Pillow (PIL)
Data Storage: JSON
Web: webbrowser
