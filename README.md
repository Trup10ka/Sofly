# Sofly Insurance Simulation 🛋️

Sofly is a web application simulating an insurance company website. This platform allows users to interact with fictional insurance products, potentially specializing in or heavily featuring sofas.

## Project Description

This repository contains the source code for the Sofly website, a demonstration project simulating the operations of an insurance company. The primary goal of this project might be to showcase web development skills, demonstrate the integration of machine learning into a web application, or simulate insurance quoting processes.

A key feature of the Sofly platform is its use of a **Machine Learning model** to predict the value or risk associated with sofas based on their characteristics. This prediction likely influences the insurance quotes provided to users.

### ML Model Parameters

The underlying ML model considers the following parameters to estimate sofa value/risk:

| Feature           | Description                                                 | Type (Example)       |
|:------------------|:------------------------------------------------------------|:---------------------|
| Length            | The overall length of the sofa (e.g., in cm)                | Numeric              |
| Width             | The overall width (or depth) of the sofa (e.g., in cm)      | Numeric              |
| Depth             | The seating depth of the sofa (e.g., in cm)                 | Numeric              |
| Cover material    | The primary material of the upholstery                      | Categorical          |
| Sit height        | The height from the floor to the seat cushion (e.g., in cm) | Numeric              |
| Contains metal    | Whether the sofa frame or legs contain metal                | Boolean (True/False) |
| Contains hardwood | Whether the sofa frame uses hardwood                        | Boolean (True/False) |

*Note: The website's input forms should ideally guide the user to provide data matching the format and units the model expects.*

## Key Features (Example)

* User registration and authentication.
* Browse fictional insurance products.
* Generate insurances
* User dashboard to view policies or quotes.

## Technology Stack

* **Backend:** Python, Flask, Poetry
* **Machine Learning:** Scikit-learn, Pandas, NumPy
* **Frontend:** HTML, CSS, JavaScript
* **Database:** MariaDB / MySQL
* **Deployment:** Poetry, Python environment

## Getting Started

These instructions will help you set up and run the Sofly website on your local machine for development and testing.

### Prerequisites

* Python (Version 3.8+ recommended)
* [Poetry](https://python-poetry.org/) for backend dependency management.
* MariaDB or MySQL for the database.

### Installing Poetry

This project uses [Poetry](https://python-poetry.org/) for managing Python dependencies. If you don't have Poetry installed, the recommended way is using `pipx`:

1.  **Install pipx:** If you don't have pipx, follow the [official pipx installation guide](https://pipx.pypa.io/stable/installation/).
2.  **Install Poetry:**
    ```bash
    pipx install poetry
    ```
    *Verify the installation:*
    ```bash
    poetry --version
    ```

### Installation

1. **Clone the repository:**
    ```bash
    git clone [https://github.com/Trup10ka/Sofly.git](https://github.com/Trup10ka/Sofly.git)
    ```
2. **Navigate to the project directory:**
    ```bash
    cd Sofly
    ```
3. **Install Backend Dependencies:**
    ```bash
    poetry install
    ```

## Running the Application Locally

Once dependencies are installed and the environment is configured, you can run the development web server:

```bash
  poetry run python -m run
```