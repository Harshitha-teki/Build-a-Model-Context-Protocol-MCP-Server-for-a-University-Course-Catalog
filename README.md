# MCP Course Catalog

## Overview
The MCP Course Catalog project is designed to expose a university's course catalog to Large Language Model (LLM) assistants through a Model Context Protocol (MCP) server. This server allows AI-powered applications to interact with and reason about domain-specific knowledge, providing students with an AI-driven academic advisor.

## Project Structure
```
mcp-course-catalog
├── data
│   ├── catalog.db          # SQLite database containing seeded course catalog data
│   └── seed_script
│       └── seed.py        # Script to populate the database with initial data
├── src
│   ├── main.py            # Entry point for the FastAPI server
│   ├── mcp_server.py      # MCP server setup and configuration
│   ├── api
│   │   ├── tools.py       # Definitions of MCP tools
│   │   └── resources.py    # Definitions of MCP resources
│   ├── db
│   │   ├── models.py      # SQLAlchemy models for database tables
│   │   └── session.py     # Database session management
│   ├── schemas
│   │   └── pydantic_models.py # Pydantic models for input/output validation
│   └── utils
│       └── graph.py       # Utility functions for managing prerequisite graphs
├── Dockerfile              # Docker image build configuration
├── docker-compose.yml      # Docker Compose orchestration file
├── .env.example            # Environment variable documentation
└── requirements.txt        # Project dependencies
```

## Setup Instructions
1. **Clone the Repository**
   ```
   git clone <repository-url>
   cd mcp-course-catalog
   ```

2. **Install Dependencies**
   Ensure you have Python 3.8+ and Docker installed. Then, install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. **Seed the Database**
   Run the seed script to populate the SQLite database with initial data:
   ```
   python data/seed_script/seed.py
   ```

4. **Run the Application**
   Use Docker Compose to build and run the application:
   ```
   docker-compose up
   ```

5. **Access the MCP Server**
   The MCP server will be accessible at `http://localhost:8080`.

## MCP Tools
- **search_courses**: Searches for courses by keyword and optional department.
- **get_prerequisites**: Retrieves direct prerequisites for a given course code.
- **lookup_instructor**: Finds an instructor's details by their name.
- **get_prerequisite_graph**: Returns the full prerequisite dependency graph for a course.

## Example Queries
- To search for courses related to "Introduction":
  ```
  {"query": "Introduction"}
  ```

- To get prerequisites for a course:
  ```
  {"course_code": "CS101"}
  ```

- To look up an instructor:
  ```
  {"instructor_name": "Dr. Smith"}
  ```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.