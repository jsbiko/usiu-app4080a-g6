# usiu-app4080a-g6
This is a simple peer programming project at USIU-Africa, App4080A class for fall 2025. Welcome aboard!
Creating a Saas

## 📋 Prerequisites

- **Python 3.8+** installed

---

## 🔧 Quick Setup 

### Step 1: Clone the Repository

```bash
git clone https://github.com/jsbiko/usiu-app4080a-g6.git
cd usiu-app4080a-g6
```

### Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize the Database

```bash
cd server
python seed.py
cd ..
```

### Step 5: Start the Server

```bash
cd server
python app.py
```

**Server should now be running at: http://localhost:5000**

---
