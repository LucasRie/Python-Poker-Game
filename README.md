# Texas Hold'em Poker Simulation

<img width="1532" height="815" alt="image" src="https://github.com/user-attachments/assets/552fa8a5-44fb-443f-8339-11bae2348212" />

**Disclaimer:** This code is part of a formal assessment. If you are a student, do not copy this code for your own coursework. It is published here for portfolio and educational demonstration purposes only. Plagiarism checkers will identify this code. 

## Overview
This application is a comprehensive simulation of Texas Hold'em Poker, featuring a fully interactive Graphical User Interface (GUI) and a statistical probability engine.

Unlike simple console-based card games, this project focuses on Object-Oriented Programming (OOP) principles to manage complex game states, including the Pre-flop, Flop, Turn, and River betting rounds. The player will face off against three computer controlled "bots" driven by decision-making algorithms.

## Technical Highlights
- **Object-Oriented Design:** strict separation of concerns between Game Logic, User Authentication, and UI Rendering.
- **Custom Probability Engine:** Real-time calculation algorithms that advise the user on their hand's statistical strength relative to the board.
- **Algorithmic Hand Evaluation:** A robust evaluator that identifies hand rankings from High Card to Royal Flush.
- **Custom Data Security:** Implemented a unique hashing algorithm from scratch (utilizing binary conversion and padding) to demonstrate understanding of data obfuscation and storage.

## Gameplay Features
- **Single Player Mode:** Play against 3 AI bots with unique betting behaviors and risk profiles.
- **Full Game Loop:** Complete implementation of Texas Hold'em stages (Pre-flop, Flop, Turn, River, Showdown).
- **Dynamic Betting System:** Supports Checking, Calling, Betting, Raising and Folding.
- **Pot Management:** Accurate calculation of main pots and split pots during multi-way all-ins.

## User Experience (UX)
- **User Accounts:** Registration and Login system with JSON storage.
- **Leaderboard:** Tracks user chip counts and displays top ranking players locally.
- **Customization:** Includes changeable color schemes (Green, Blue, Orange, Pink) and setting toggles.

## Technologies Used
- **Language:** Python 3
- **GUI:** Tkinter
- **Image Handling:** Pillow (PIL)
- **Data Storage:** JSON (Flat-file database)

