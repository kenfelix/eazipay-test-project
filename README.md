# EAZIPAY TEST PROJECT

Contains 2 services with:
- one setup for basic GraphQL backend service
- and the other used for MongoDB schema Models and Graphql Type definitions updates.

The Graphql service has basic Auth endpoints(e.g. Signup & Login), however Schema and Types definitions are updated in the other service, and at all times the current file versions in the second service are automatically added to the Graphql service on deployment trigger(should be able to test locally as well).

## Table of Contents

- [Project Name](#project-name)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Configuration](#configuration)
  - [Usage](#usage)
  - [License](#license)



## Prerequisites

Python >=3.10.

## Getting Started

Explain how to set up the project on a local development environment.

### Installation

Provide step-by-step instructions for installing the project and its dependencies.

```bash
# Clone the repository
git clone https://github.com/kenfelix/eazipay-test-project.git

# Change to the project directory
cd eazipay-test-project

# Change to the graphql-backend service directory

cd graphql-backend

# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate

# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Install project dependencies
pip install -r requirements.txt
```

### Configuration

create a .env file in the root of current directory and put the follow fields:

DB_URL=monogodb-atlas-connection-str e.g mongodb+srv://kenfelix:12345@kenfelix.ziwhr6r.mongodb.net/?retryWrites=true&w=majority

## Usage

Provide instructions on how to run and use your application.

```bash
# Start the development server
uvicorn app.main:app --reload
```

on your browser go to: localhost:8000/graphql


## License

Specify the license under which your project is released. For example:

This project is licensed under the [MIT License](LICENSE.md).
