# SLCSP

This repository contains the Python solution to the [SLCSP problem](https://homework.adhoc.team/slcsp/). The goal of this project is to calculate the second lowest cost silver plan (SLCSP) for a set of ZIP codes.

## Prerequisites

- Python 3.x

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Setting Up Your Environment

It's recommended to use `virtualenv` to create an isolated environment for Python projects. This ensures that the project dependencies do not interfere with other Python projects on your system.

1. **Install `virtualenv` if it's not installed:**

   ```bash
   pip install virtualenv
   ```

2. **Create a Virtual Environment:**

   Navigate to the project directory and run:

   ```bash
   python3 -m virtualenv venv
   ```

3. **Activate the Virtual Environment:**

   On macOS and Linux:

   ```bash
   source venv/bin/activate
   ```

   On Windows:

   ```bash
   .\venv\Scripts\activate
   ```

### Installing Dependencies

Install all required packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Running the Application

Once the environment is set up and dependencies are installed, you can run the application using:

```bash
python3 run.py
```

## Running Tests

To run tests, use the following command:

```bash
python3 test_run.py
```