# Python Project for CST1510
 Student Name: Ayush Mani Tripathi
 Student ID: M01071841
 Course: CST1510 -CW2 -  Multi-Domain Intelligence Platform 

 # Week 7: Secure Authentication System

## Project Description
 A command-line authentication system implementing secure password hashing
 This system allows users to register accounts and log in with proper pass
 ## Features
 -Secure password hashing using bcrypt with automatic salt generation
 -User registration with duplicate username prevention
 -User login with password verification
 -Input validation for usernames and passwords
 -File-based user data persistence
 ## Technical Implementation
 -Hashing Algorithm: bcrypt with automatic salting
 -Data Storage: Plain text file (`users.txt`) with comma-separated values
 -Password Security: One-way hashing, no plaintext storage
 -Validation: Username (More than 3 characters long and must be of valid type), Password (More than 8 characters long)

--------------------------------------------------------------------------------------
  # Week 8: Database Management System Implementation

 ## Creating a proper folder structure 
 - Improve modularity of the codes
 - Easy structure to work with

 ## Implementing CRUD operations
 -CRUD operations (Create, Read, Update, Delete) implemented on database tables.

 ## Exporting CSV files
-To get values to store in the database
--------------------------------------------------------------------------------------
  # Week 9: Streamlit implementation
## Applying streamlit design concepts to Week 8 work
-Interactive dashboards for users, datasets, and tickets.

-Dynamic metrics and charts for visualization.

-Forms for adding, updating, and deleting records.
---------------------------------------------------------------------------------------

  # Week 10 : API Integration
## Using Gemini API to integrate chatbot and carry out the assessment of the different dashboards 
-AI-assisted ticket and dataset analysis.

-Chatbot-like interface to provide insights, recommendations, and troubleshooting.

-Real-time AI evaluation embedded within Streamlit dashboards.

## How to use local API to run the Gemini API
## API Setup Instructions

1. Create a folder called `.streamlit`
2. Inside it, create a file called `secrets.toml`
3. Add the following content:

GEMINI_API_KEY = "your_api_key_here"


  # Week 11 : OOP implementation
## Refactoring existing codes with some new codes to improve modularity with OOP
-Use of classes for datasets (Dataset), CyberIncidents and IT tickets (IT_Ticket).

-Methods for CRUD operations integrated into class instances.

-Database interactions handled via a DatabaseManager class.

-Enhanced maintainability and reusability of code across the platform.

  # How to run the streamlit web page
  - Use the follwing command on terminal -> streamlit run Home.py
  