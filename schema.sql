-- Projects table
CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'INIT',
    current_stage TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Stages table
CREATE TABLE stages (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'NOT_STARTED',
    start_date TEXT,
    end_date TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Tasks table
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    stage_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'TODO',
    priority INTEGER CHECK (priority BETWEEN 1 AND 5),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (stage_id) REFERENCES stages(id) ON DELETE SET NULL
);

-- Task assignees table
CREATE TABLE task_assignees (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    assignee_id TEXT NOT NULL,
    assignee_type TEXT NOT NULL CHECK (assignee_type IN ('USER', 'AGENT')),
    role TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- Project members table
CREATE TABLE project_members (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    member_id TEXT NOT NULL,
    member_type TEXT NOT NULL CHECK (member_type IN ('USER', 'AGENT')),
    role TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Indexes for better performance
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_stages_project ON stages(project_id);
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_members_project ON project_members(project_id);
