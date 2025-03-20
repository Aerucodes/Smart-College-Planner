# Smart College Planner

A modern, feature-rich college planner application with a beautiful GUI, dark mode support, and intuitive drag-and-drop interface.

## Features

- Clean and modern user interface
- Dark mode and light mode toggle
- Calendar integration for deadline management
- Task priority levels (Low, Medium, High)
- Drag-and-drop task organization
- Smooth animations
- Persistent storage using SQLite
- Responsive design

## Requirements

- Python 3.8 or higher
- PyQt6
- SQLite3

## Installation

### Option 1: Using the Executable (Recommended)

1. Download the latest release from the releases page
2. Extract the zip file
3. Run `SmartCollegePlanner.exe`

### Option 2: Running from Source

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python college_planner.py
```

### Option 3: Building the Executable

If you want to build the executable yourself:

1. Install the requirements:
```bash
pip install -r requirements.txt
```

2. Run the build script:
```bash
python build.py
```

3. The executable will be created in the `dist` folder as `SmartCollegePlanner.exe`

## Usage

### Adding Tasks

1. Enter a task title in the input field
2. Select a priority level from the dropdown
3. Choose a deadline using the calendar
4. Click "Add Task" to create the task

### Managing Tasks

- Tasks are displayed in the right panel
- Drag and drop tasks to reorder them
- Click the moon/sun icon to toggle between dark and light modes

## Data Storage

All tasks are automatically saved to a SQLite database (`college_planner.db`) in the same directory as the application.

## Copyright

© 2025 Aerucodes. All rights reserved. 