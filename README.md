# UI Screen Parser 🔍

An intelligent AI-powered tool that analyzes UI screenshots and answers natural language queries about component layouts, positions, and relationships.



## 🚀 Features

- **🔍 Smart Component Detection**: Uses computer vision and OCR to identify UI elements (buttons, text fields, images, etc.)
- **🗣️ Natural Language Queries**: Ask questions like "Where is the search bar?" or "How many buttons are there?"
- **📊 Spatial Relationship Mapping**: Understands relationships between components (above, below, left, right)
- **🎯 High Accuracy Analysis**: Advanced algorithms for reliable UI element detection
- **💻 Interactive Query Mode**: Real-time Q&A about your UI layouts
- **📄 Structured Output**: Exports detailed analysis as JSON with component positions and relationships

## 🎯 Use Cases

- **UI/UX Testing**: Automated analysis of interface layouts
- **Accessibility Auditing**: Understanding component relationships for screen readers
- **Design Documentation**: Generate structured descriptions of UI layouts
- **Quality Assurance**: Verify UI component positioning across different screens
- **Research**: Analyze UI patterns and design trends

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Quick Start

1. **Clone the repository:**
git clone https://github.com/yourusername/ui-screen-parser.git

3. **Create and activate virtual environment:**
python -m venv venv
.\venv\Scripts\activate

5. **Install dependencies:**
pip install -r requirements.txt

6. **Verify installation:**
python src/main.py examples/sample_screens/test_image.png



### Query Mode

Ask specific questions about your UI:

python src/main.py examples/sample_screens/test_image.png "where is the search bar?"



### Interactive Mode

Enter interactive mode for multiple queries:


Then type queries like:
- `"how many buttons are there?"`
- `"where is the blue text?"`
- `"what is above the login form?"`
- `"find the shopping cart icon"`

### Example Queries

**Component Counting:**
- "How many components are there?"
- "How many buttons can you find?"

**Location Queries:**
- "Where is the search bar?"
- "Find the text 'Login'"
- "Locate the blue button"

**Relationship Queries:**
- "What is above the main content?"
- "What components are to the left of the sidebar?"

**Color-based Queries:**
- "Where are the red elements?"
- "Find orange buttons"

## 📊 Sample Output
<img width="1763" height="127" alt="image" src="https://github.com/user-attachments/assets/14af5fcc-247a-4526-bf20-55348f053732" />
<img width="1799" height="117" alt="image" src="https://github.com/user-attachments/assets/276942ca-18d0-4113-9cfe-0c682409f619" />


