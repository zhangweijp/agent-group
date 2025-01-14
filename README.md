# Project Management API

A FastAPI-based project management system with SQLite backend.

## Features

- Project management (create, read, update, delete)
- Stage management within projects
- Task management within projects
- Member/Agent management within projects
- RESTful API endpoints
- SQLite database for easy setup

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your configuration (see `.env.example`)
4. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

## API Documentation

The API documentation will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DB_PATH | Path to SQLite database file | database.db |
| SECRET_KEY | Secret key for security | your-secret-key |

## API Endpoints

### Projects
- `POST /api/projects` - Create a new project
- `GET /api/projects` - List all projects

### Stages
- `POST /api/projects/{project_id}/stages` - Create a new stage

### Tasks
- `POST /api/projects/{project_id}/tasks` - Create a new task
- `POST /api/tasks/{task_id}/assignees` - Add an assignee to a task
- `GET /api/tasks/{task_id}/assignees` - Get all assignees for a task
- `PUT /api/tasks/{task_id}/assignees/{assignee_id}` - Update an assignee's role
- `DELETE /api/tasks/{task_id}/assignees/{assignee_id}` - Remove an assignee from a task

### Members
- `POST /api/projects/{project_id}/members` - Add a member/agent

### Example: Assigning a task to an Agent
```bash
# Create task
POST /api/projects/{project_id}/tasks
{
  "name": "Implement feature X",
  "description": "Add new API endpoints",
  "assignees": [
    {
      "assignee_id": "agent-123",
      "assignee_type": "AGENT",
      "role": "developer"
    }
  ]
}

# Add another assignee
POST /api/tasks/{task_id}/assignees
{
  "assignee_id": "user-456",
  "assignee_type": "USER",
  "role": "reviewer"
}

# Get all assignees
GET /api/tasks/{task_id}/assignees
```

## Testing

To run tests:
```bash
pytest
```

## License

MIT License
