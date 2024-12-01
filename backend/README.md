## Requirements

- Python 3.6 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```
### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

### 4. Run the Application

```bash
python app.py
```