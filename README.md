Job Portal Backend API :
This is a production-focused REST API built to handle the core logic of a job board. It manages the entire lifecycle of a job post—from a recruiter creating the listing to a seeker submitting their application—all wrapped in a secure, role-based permission system.
while building this,Implemented strict server-side authorization to prevent role-spoofing or unauthorized data access from the client side. 

Key Functionalities :-
Identity & Access Management: Secure signup and login flow using JWT. I’ve implemented Role-Based Access Control (RBAC) to strictly separate what Admins, Recruiters, and Seekers can do.
Security & Implementation Details   When building out the backend, my main priority was ensuring that the API remains the single source of truth for security. I didn't want to rely on the frontend to hide buttons or restrict views; instead, I enforced strict permission checks at the controller level.

Job Management: Recruiters have full CRUD access to their own listings. I’ve added backend checks to ensure a recruiter can’t accidentally (or intentionally) modify another firm's posts.

Application Logic: Built-in validation to prevent duplicate applications. Once a seeker applies, the recruiter can track and manage those submissions.

Performance & Security: * Bcrypt for industry-standard password hashing.

Pagination on all major GET endpoints to keep the API responsive even as the database grows.

Ownership Enforcement: Permissions are validated at the database level to ensure data integrity.

Tech Stack
Backend :-Framework  FastAPI (for its speed and automatic Swagger documentation)

Database: MySQL with SQLAlchemy as the ORM

Migrations: Alembic (for version-controlled schema changes)

Auth: JWT via python-jose and passlib for hashing

Security:bcrypt,role-based authorization

Project Structure
The project follows a modular layout to keep the codebase maintainable:

/app: Main logic container.

/models: SQLAlchemy database models.

/schemas: Pydantic models for request/response validation.

/routers: Cleanly separated API endpoints (auth, jobs, applications).

/core: Global configs like security settings and DB engine.

/migrations: Managed by Alembic for tracking schema updates.