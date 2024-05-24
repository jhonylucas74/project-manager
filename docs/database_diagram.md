# Database Schema

## Document
A document represents a file attached to a project. It contains a name, an extension (e.g., "pdf", "docx"), the actual file, and timestamps for creation and update.

## Project
A project has a name and a description. It may have a status, such as "Backlog", "In Progress", or "Completed". Additionally, a project can have a start date and an end date. Projects can be associated with multiple documents using a Many-to-Many relationship. Lastly, a project has timestamps for creation and update.

## Milestone
A milestone is a significant milestone in a project. It has a name and an optional description. It belongs to a specific project and has a status, such as "Not Started", "In Progress", or "Completed". Additionally, a milestone may have a start date and an end date. Milestones have timestamps for creation and update.

## Task
A task is a specific activity that is part of a project or milestone. It has a name and an optional description. A task belongs to a project and may be associated with a specific milestone. Additionally, a task may have an owner, who is a user responsible for its completion. Tasks have a status, such as "Backlog", "In Progress", or "Completed". Lastly, tasks have timestamps for creation and update.

## Reference from DBeaver

![Exemplo de imagem](/docs/image_1.png)
