# 🎮 Tetris GUI Application

A feature-rich **Tetris GUI application** built with Python, combining the classic Tetris gameplay with a database system, data visualization, customizable audio settings, and a user-friendly graphical interface.

Unlike a basic Tetris implementation, this project provides a complete application ecosystem where users can register, play multiple game sessions, store their results, review their gaming history, analyze their performance through visualizations, and customize their gaming experience.

---

## ✨ Features

### 🎮 Tetris Game

* Classic Tetris gameplay.
* Interactive graphical interface.
* Game sessions and scores are automatically recorded.
* Music and sound effects integrated into the gameplay.

### 👤 User Management

* Players can register their own usernames.
* Each player's game sessions are associated with their account.
* Previously recorded sessions can be accessed through the application.

### 📊 Game History

The **History** page allows users to:

* View previously recorded game sessions.
* Review their gaming data.
* Update existing records.
* Delete records when necessary.

### 📈 Statistics & Data Visualization

The **Stats** page provides visual representations of the player's recorded game data.

Using **Matplotlib**, the application can generate different types of graphs to help users analyze their gameplay and performance over time.

### 🎵 Audio & Sound Effects

The application includes:

* Background music.
* Gameplay sound effects.
* Customizable audio settings.

Users can configure their audio preferences through the **Options** page.

### ⚙️ Options

The **Options** page allows users to customize different aspects of their gaming experience, particularly music and sound effects.

---

## 🛠️ Technologies Used

| Technology     | Purpose                                   |
| -------------- | ----------------------------------------- |
| **Python**     | Main programming language                 |
| **Tkinter**    | GUI and application interface             |
| **Pygame**     | Tetris gameplay, music, and sound effects |
| **MySQL**      | Database management and storage           |
| **SQL**        | Database queries and data manipulation    |
| **Matplotlib** | Data visualization and statistics         |

---

## 🏗️ Application Architecture

The project combines several components into a single GUI application:

```text
                    ┌─────────────────────┐
                    │    Tetris GUI App   │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       ┌───────────┐     ┌────────────┐    ┌─────────────┐
       │  Tetris   │     │  Database  │    │   Options   │
       │  Gameplay │     │   System   │    │    /Audio   │
       └─────┬─────┘     └─────┬──────┘    └─────────────┘
             │                 │
             │                 ▼
             │          ┌──────────────┐
             │          │ Game History │
             │          └──────┬───────┘
             │                 │
             │                 ▼
             │          ┌──────────────┐
             └─────────►│    Stats     │
                        │  Matplotlib  │
                        └──────────────┘
```

---

## 📂 Project Structure

A possible project structure is:

```text
Tetris/
│
├── menu_v1.py
├── testing.sql
│
├── [other Python source files]
├── [game assets]
│   ├── music/
│   └── sounds/
│
└── README.md
```

> The exact structure may vary depending on the organization of the project files.

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Install Python Dependencies

Make sure you have Python installed on your system.

Install the required libraries using:

```bash
pip install pygame matplotlib mysql-connector-python
```

**Tkinter** is included with most standard Python installations. On some Linux distributions, it may need to be installed separately.

---

### 3. Set Up MySQL

The application requires a running **MySQL server**.

Start your local MySQL server using your preferred environment, such as:

* XAMPP
* WAMP
* MySQL Server
* Another local MySQL environment

---

### 4. Import the Database

The project contains the database file:

```text
testing.sql
```

Import this file into your local MySQL server.

For example, using MySQL:

```bash
mysql -u <username> -p <database_name> < testing.sql
```

Alternatively, you can import `testing.sql` through a database management tool such as **phpMyAdmin**.

---

### 5. Configure Database Connection

Make sure the database connection settings in the Python project correspond to your local MySQL configuration.

Typical configuration parameters include:

```python
host = "localhost"
user = "your_username"
password = "your_password"
database = "your_database"
```

Update these values according to your local MySQL setup.

---

## ▶️ Running the Application

After starting your local MySQL server and importing the database, run:

```bash
python menu_v1.py
```

The main GUI application should then launch.

---

## 🕹️ How to Use

### 1. Register a Username

Enter a username to create or access a player's profile.

### 2. Play Tetris

Start a game and play using the available controls.

Your game session and relevant statistics are recorded in the database.

### 3. View History

Navigate to the **History** page to review previously recorded game sessions.

You can also update or delete stored records.

### 4. View Statistics

Open the **Stats** page to visualize your recorded gameplay data using different graphs.

### 5. Customize Options

Use the **Options** page to customize music and sound-effect settings.

---

## 💾 Database

The application uses **MySQL** to persist player and gameplay information.

The database is responsible for storing information such as player identities and game-session records, allowing data to remain available between application runs.

This persistent storage also provides the foundation for the application's **History** and **Stats** functionality.

---

## 📊 Data Visualization

Gameplay data stored in the database can be processed and visualized using **Matplotlib**.

The visualization component allows users to examine their gameplay data graphically rather than relying solely on raw database records.

This makes it possible to analyze performance and identify trends across multiple game sessions.

---

## 🎵 Audio System

The application uses **Pygame** to handle its audio functionality.

It supports both:

* Background music
* Gameplay sound effects

Audio preferences can be customized through the application's **Options** page.

---

## 🎯 Project Goals

The main goals of this project are to:

* Implement a functional Tetris game.
* Develop a complete GUI-based desktop application.
* Integrate a relational database with a Python application.
* Store and manage persistent user/game data.
* Provide CRUD functionality for game history.
* Visualize gameplay data using graphs.
* Integrate customizable music and sound effects.
* Demonstrate the integration of multiple technologies into one application.

---

## 📚 Concepts Demonstrated

This project demonstrates practical experience with:

* Object-oriented and procedural Python programming
* GUI development
* Event-driven programming
* Database connectivity
* SQL queries
* CRUD operations
* Persistent data storage
* Data visualization
* Game development
* Audio handling
* Application configuration
* Integration of multiple Python libraries

---

## 🔮 Possible Future Improvements

Potential improvements could include:

* 🏆 Global leaderboard
* 👥 Multiple-player support
* 🔐 Password-based accounts
* 🎨 Additional themes and visual customization
* 📊 More advanced statistics
* 📅 Filtering statistics by date
* 💾 Exporting statistics to CSV
* 🌐 Online multiplayer functionality
* 🧩 Additional Tetris game modes
* ⏱️ More detailed performance tracking

---

## 👨‍💻 Author

**Arsen Pinachyan**

This project was developed as a Python-based GUI application demonstrating the integration of **game development, databases, and data visualization**.

---

## 📄 License

This project is intended for educational and personal use.
