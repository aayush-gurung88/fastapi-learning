from datetime import datetime

class Todo:
    id: int
    title: str
    description: str
    is_completed: bool
    priority: int
    created_at: datetime

    def __init__(self, id , title , description, is_completed, priority):
        self.id = id
        self.title = title
        self.description = description
        self.is_completed = is_completed
        self.priority = priority
        self.created_at = datetime.now()