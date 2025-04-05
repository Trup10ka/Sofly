# Sofly Insurance Simulation 🛋️

Sofly is a web application designed to simulate the operations of an insurance company, allowing users to interact with fictional insurance products. The project aims to demonstrate web development skills and the integration of machine learning into a web application.

## Features

- **Insurance Policy Management**: Create, view, and manage fictional insurance policies.
- **Claims Processing**: Simulate the submission and processing of insurance claims.
- **Machine Learning Integration**: Utilizes machine learning models to assess risk and predict claim outcomes.

### ML Model Parameters

The underlying ML model considers the following parameters to estimate sofa value/risk:

| Feature    | Description                                      | Type (Example)   |
|:-----------|:-------------------------------------------------|:-----------------|
| Dimensions | The overall size of furniture                    | Numeric          |
| Is sofa    | Whether the furniture is sofa                    | Boolean (0 or 1) |
| Is chair   | Whether the furniture is a chair                 | Boolean (0 or 1) |
| Is table   | Whether the furniture is a table                 | Boolean (0 or 1) |
| Is leather | Whether the furniture is leather                 | Boolean (0 or 1) |
| Is fabric  | Whether the furniture is fabric                  | Boolean (0 or 1) |
| Is none    | Whether the furniture has uncategorized material | Boolean (0 or 1) |

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

# License

This project is licensed under the MIT License.
See the [LICENSE](https://github.com/Trup10ka/Sofly/blob/main/LICENSE) file for details.

# Disclaimer

Sofly is a fictional application created for educational and demonstration purposes only. It is not intended for actual insurance operations or real-world use.

