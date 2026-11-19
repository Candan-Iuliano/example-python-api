# Code Metal Take-Home: 3-Hour Execution Strategy

## Objective

Deliver a working, understandable Python application that:

1. Reads the supplied JSON data and ingests valid records into PostgreSQL.
2. Persists the core entities and analysis results using SQLAlchemy.
3. Exposes read-only REST endpoints for the stored data and analysis.
4. Runs repeatable geospatial analysis and persists its results.
5. Uses structured logging and has enough tests to demonstrate correctness.

**Timebox:** 3 hours. Prioritize a complete vertical slice over polishing every feature. Get one end-to-end path working early, then expand it.

---

## Before the clock starts

- Read the entire prompt and inspect every supplied data file.
- Identify required entities, fields, relationships, analyses, and API outputs.
- Write down assumptions and any unclear requirements.
- Check the available database connection details.
- Do not assume the practice `locations.json` dataset or its schema matches the actual take-home data.
- Create the project structure using `PROJECT_SETUP_CHEATSHEET.md`.

## Three-hour implementation plan

### 0:00–0:15 — Understand the input and establish the skeleton

- Inspect the JSON files: top-level structure, field names, data types, optional fields, and examples.
- Identify required vs optional fields and likely invalid records.
- Create the app, data, tests, and migrations directories.
- Set up dependencies and database configuration.
- Create a minimal FastAPI health endpoint.
- Confirm the app imports and starts.

**Deliverable:** project starts; input format and data model are understood.

### 0:15–0:40 — Define database models and migrations

- Create SQLAlchemy models for the core input entities.
- Add primary keys, appropriate types, nullable fields, and constraints.
- Add foreign keys and ORM relationships only where the data model needs them.
- Create the database and configure the connection.
- Initialize/configure Alembic and generate the initial migration.
- Apply the migration and verify the tables exist.

**Deliverable:** database schema is created and reproducible through Alembic.

**Keep it simple:** model the data you need to satisfy the prompt. Avoid speculative tables and abstractions.

### 0:40–1:10 — Build repeatable ingestion

- Write a function that reads the provided JSON file.
- Validate each record before constructing ORM objects:
  - required fields exist;
  - values have the expected types;
  - strings are not blank where names/identifiers are required;
  - numeric values are in valid ranges;
  - malformed records are skipped and logged with a reason.
- Decide how to handle duplicate records. Make repeated ingestion safe.
- Add valid records to the database and commit in a controlled batch.
- Run ingestion twice and verify the second run does not create unwanted duplicates.
- Test validation independently from database access where practical.

**Deliverable:** ingestion works, reports skipped records, and is safe to rerun.

### 1:10–1:45 — Implement the required analysis

- Implement the required geospatial calculations as small, independently testable functions.
- Keep calculation logic separate from database queries and persistence.
- Use the formulas supplied in the prompt or trusted references; do not spend time deriving advanced spherical geometry from scratch.
- Validate inputs and handle edge cases (identical points, invalid coordinates, no matching records, no intersection).
- Create a service/function that:
  1. retrieves the required input records;
  2. calls the calculation function;
  3. creates an analysis-result record;
  4. commits the result.
- Store structured output in a suitable column (for example, JSON/JSONB) if the result has multiple fields.
- Run one or two known examples and inspect the persisted results.

**Deliverable:** at least one complete analysis path calculates and persists a result correctly. Then add the remaining required calculations.

### 1:45–2:20 — Expose the read-only REST API

- Define Pydantic response schemas separately from SQLAlchemy models.
- Add endpoints for the core records and analysis results.
- Include detail endpoints by ID if required.
- Return appropriate 404 responses for missing individual records.
- Return an empty list for collection endpoints with no records.
- Use eager loading (`joinedload` or `selectinload`) when returning related ORM objects so relationships are available while the session is open.
- Keep database sessions reliably closed, including on errors.
- Check the endpoints in `/docs` and verify response shapes.

**Deliverable:** client-facing endpoints return the expected stored data.

### 2:20–2:45 — Test the end-to-end paths and failure cases

Prioritize tests that protect important behavior:

- valid input is accepted;
- missing or invalid fields are rejected/skipped as intended;
- duplicate ingestion does not duplicate rows;
- geospatial functions return expected values for known examples;
- analysis results are persisted;
- API collection endpoints return data;
- detail endpoints return 404 for unknown IDs.

Run the tests and fix failures. Also manually exercise the health, data, and analysis endpoints.

**Deliverable:** a small, meaningful test suite and verified application flow.

### 2:45–3:00 — Final reliability pass

- Run the app from a clean terminal using the documented command.
- Apply migrations from the current revision.
- Run ingestion once more and check counts.
- Run tests.
- Check logs for useful event names, levels, and failure reasons.
- Remove debug prints, dead code, and unused imports.
- Add a concise README with setup, migration, ingestion, test, and server commands.
- Make sure secrets are not committed or hard-coded in deliverables.

**Deliverable:** someone else can understand how to configure, run, and test the project.

---

## Prioritization if time runs short

Use this order:

1. Database models and migration.
2. Validated, repeatable ingestion.
3. At least one required analysis path, including persistence.
4. Read-only API for stored data and results.
5. Tests for the critical paths.
6. Structured logging and documentation polish.

Do not spend the final hour refactoring a working solution or adding optional infrastructure. A smaller working application is better than a broad unfinished one.

## Delegating work to AI agents

Use agents for bounded tasks with explicit inputs and outputs. Keep the integration and final review under your control.

### Higher-capability agent

Best for work with ambiguity, multiple requirements, or tricky reasoning:

- Review the prompt and produce a requirements checklist.
- Propose the database schema and relationships based on the actual JSON.
- Review geospatial formulas and edge cases.
- Review the overall architecture for missing requirements.
- Diagnose difficult bugs from exact tracebacks and relevant code.

Ask it to explain assumptions and identify edge cases. Do not ask it to rewrite the whole project without reviewing the changes.

### Lower-cost/faster agent

Best for narrow, well-defined tasks:

- Draft a simple SQLAlchemy model from a field list.
- Generate straightforward Pydantic schemas.
- Draft a basic endpoint matching an existing pattern.
- Write focused pytest cases for a specified function.
- Explain a traceback or review a small code snippet.

Give it the relevant model/schema/function and ask for a minimal change only.

### Good delegation prompt

> Work only on the task described below. Use the existing file structure, naming, SQLAlchemy/Pydantic patterns, and code style. Do not invent fields or requirements. Do not refactor unrelated code. First list the files you would change and why. Then provide the smallest implementation and focused tests. Explain assumptions and any edge cases.

### Token/time discipline

- Do not spend tokens asking agents to restate the whole prompt repeatedly.
- Give each agent only the relevant requirements, files, and error output.
- Ask for a review or a focused implementation, not an entire application.
- Verify every generated change locally; the agent's answer is not proof that code runs.

---

## Final checklist

- [ ] App starts successfully.
- [ ] Database connection works.
- [ ] Alembic migration creates the required schema.
- [ ] Supplied JSON can be ingested.
- [ ] Invalid records are handled and logged.
- [ ] Re-running ingestion is safe.
- [ ] Required analyses calculate correctly.
- [ ] Analysis results are persisted.
- [ ] Read-only API endpoints return expected response models.
- [ ] Related objects are loaded before sessions close.
- [ ] Missing detail records return 404.
- [ ] Critical tests pass.
- [ ] README explains setup and execution.
- [ ] No secrets are committed.
