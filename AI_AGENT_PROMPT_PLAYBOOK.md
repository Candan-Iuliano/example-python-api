# AI Agent Prompt Playbook — Code Metal Take-Home

Use this as a prompt reference when working with your lower-cost/faster model and your higher-capability model.

## The goal

Use AI to accelerate specific tasks while keeping the engineering decisions and integration under your control.

A good workflow is:

1. You inspect the requirements and existing code.
2. You decide what needs to be built next.
3. You ask the model for a focused explanation, review, or small implementation.
4. You inspect the proposed changes and ask questions about anything you do not understand.
5. You run the code and tests yourself.
6. You keep or revise the changes based on the actual result.

**Do not ask an agent to build the entire project in one shot.** That makes it harder to understand, debug, and verify the result.

---

# 1. Prompts for the higher-capability model

Use this model for ambiguous requirements, architecture decisions, tricky bugs, and independent reviews.

## A. Analyze the take-home requirements

Use this near the beginning, after you have read the prompt and inspected the supplied data.

> Review the take-home requirements and the supplied input files. Do not write code yet.
>
> Produce:
> 1. A checklist of explicit requirements.
> 2. The entities and fields that appear to be needed, based on the actual input data.
> 3. The relationships between those entities, if any.
> 4. The required ingestion, analysis, and API workflows.
> 5. Important edge cases and unclear requirements.
> 6. A suggested implementation order for a three-hour time limit.
>
> Separate facts from assumptions. Do not invent fields or requirements. Keep the plan minimal and prioritize a working end-to-end solution.

## B. Review my proposed database design

> Review the SQLAlchemy models below against the take-home requirements and actual input data.
>
> Check:
> - primary keys and column types;
> - nullable vs required fields;
> - foreign keys and relationship definitions;
> - whether the relationships are ambiguous;
> - whether any fields or tables are unnecessary;
> - whether the schema can store the required analysis results.
>
> Do not rewrite the models yet. First identify specific issues and explain why they matter. Suggest only the smallest necessary changes.
>
> [Paste relevant models and requirements.]

## C. Explain a difficult concept without taking over

> I am implementing [specific task]. I understand [what I already understand], but I am unsure about [specific question].
>
> Explain the concept using the code and data model I provide. Do not write the full implementation. Give me a short explanation and, if useful, a small example that is separate from my project. Then give me one question I can answer to check my understanding.
>
> [Paste relevant code.]

## D. Diagnose a difficult bug

> Help me diagnose this bug. Do not immediately rewrite the code.
>
> Expected behavior: [what should happen]
> Actual behavior: [what happens]
> Error/traceback: [paste the complete relevant traceback]
> Relevant code: [paste the smallest relevant section]
>
> Identify the most likely cause, explain the evidence, and suggest the smallest change to test first. Mention other plausible causes only if they are genuinely relevant. Do not invent project files, fields, or functions.

## E. Review the geospatial approach

> Review my approach to implementing [specific geospatial calculation].
>
> The required inputs are: [list inputs].
> The expected output is: [describe output].
> The formula or reference supplied by the prompt is: [paste formula, if provided].
> My implementation is: [paste code].
>
> Check units, degrees vs radians, coordinate ordering, edge cases, and numerical stability. Do not replace the required formula with a different approach without explaining why. Identify test cases I should run. Focus on correctness and integration rather than advanced mathematical theory.

## F. Perform a final requirements review

> Review the current project against this take-home requirements checklist.
>
> Do not make code changes. Identify:
> 1. Requirements that appear complete.
> 2. Requirements that are missing or only partially implemented.
> 3. Likely runtime or integration risks.
> 4. The three highest-value fixes I can realistically make with the time remaining.
>
> Base your review only on the requirements and files I provide. Do not assume unshown code works.
>
> [Paste requirements checklist and relevant project tree/code.]

---

# 2. Prompts for the lower-cost/faster model

Use this model for narrow tasks with clear inputs and expected outputs.

## A. Draft a small function from a clear specification

> Help me implement only this function:
>
> Function purpose: [purpose]
> Inputs: [types and meaning]
> Expected output: [type and meaning]
> Rules: [validation and edge cases]
>
> Before writing code, give me a short outline of the steps. Then provide a minimal implementation that matches my existing code style. Do not add helper functions, classes, dependencies, or unrelated refactoring.

## B. Draft focused pytest tests

> Write focused pytest tests for the function below.
>
> Cover:
> - one normal valid case;
> - one invalid input;
> - relevant boundary cases;
> - expected exceptions, if applicable.
>
> Use fixtures only if they reduce repetition. Do not change the function being tested. Briefly explain what each test verifies.
>
> [Paste function.]

## C. Draft a Pydantic response schema

> Based on this SQLAlchemy model and the API response I need, draft the smallest appropriate Pydantic response schema.
>
> Use Pydantic v2 syntax. Explain whether `from_attributes=True` is needed and how nested relationships should be represented. Do not modify the SQLAlchemy model.
>
> [Paste model and desired JSON response.]

## D. Draft a straightforward API endpoint

> I need one FastAPI endpoint with this behavior:
>
> Method/path: [e.g. GET /locations/{location_id}]
> Expected response: [describe response]
> Missing-record behavior: [e.g. HTTP 404]
> Existing patterns in my project: [paste a similar endpoint]
>
> Draft only this endpoint. Follow the existing session-management and response-schema patterns. Do not add unrelated routes or refactor other files.

## E. Explain a traceback

> Explain this Python error in plain language.
>
> Error/traceback:
> [paste traceback]
>
> Relevant code:
> [paste code]
>
> Tell me what operation failed, why it likely failed, and the smallest change I should try. Do not rewrite the whole file.

## F. Review a small code section

> Review this code for correctness and obvious edge cases.
>
> Focus on:
> - incorrect logic;
> - type or validation problems;
> - resource/session cleanup;
> - unnecessary complexity.
>
> Do not redesign the application. List issues by severity and explain the smallest useful correction.
>
> [Paste code.]

---

# 3. Ask the model to teach, not just produce code

These prompts are useful when you want to demonstrate that you understand the implementation.

### Ask for a plan before code

> Before providing code, describe the implementation steps in plain language. Wait for me to attempt the code before giving me a complete solution.

### Ask for hints only

> I want to solve this myself. Give me one hint at a time. Do not reveal the full implementation unless I explicitly ask.

### Ask for a code review rather than a rewrite

> Review my implementation. Preserve my structure and naming. Point out the specific lines or logic that need attention. Do not replace the entire implementation.

### Ask for a verbal explanation check

> Ask me three short questions about this implementation, one at a time. Evaluate my answers and correct misunderstandings. Do not give me the answers before I try.

### Ask what you should test

> Based on this function and its requirements, suggest the most important test cases. Do not write the tests yet. Explain what behavior each test is intended to verify.

---

# 4. A standard instruction to include with coding requests

Copy this into coding requests when appropriate:

> Work within my existing project structure and conventions. Use only fields, functions, and classes that exist in the code or are explicitly required. Do not invent architecture or requirements. Avoid unnecessary helper functions, dependencies, abstractions, and broad refactoring. Make the smallest change that solves the stated task. Explain assumptions and identify anything I need to verify locally.

---

# 5. What to give an agent

Give the model enough context to do the task, but not the entire project every time.

For most requests, include:

- the exact requirement being implemented;
- the relevant input-data example or expected API response;
- the file or function being changed;
- directly related models/schemas, if needed;
- the error traceback, if debugging;
- any constraints, such as read-only API or repeatable ingestion.

Avoid sending passwords, API keys, database credentials, or other secrets.

---

# 6. How to divide work between the two models

| Task | Preferred model | Why |
|---|---|---|
| Interpret ambiguous requirements | Higher-capability | Requires reasoning across the prompt |
| Propose/check database relationships | Higher-capability | Design choices affect multiple parts |
| Review geospatial edge cases | Higher-capability | More subtle reasoning |
| Diagnose a complex integration failure | Higher-capability | Needs broader context |
| Final requirements/code review | Higher-capability | Cross-checks the whole solution |
| Draft a small validator | Lower-cost/faster | Narrow, well-defined task |
| Generate basic pytest cases | Lower-cost/faster | Clear expected behavior |
| Draft a simple response schema | Lower-cost/faster | Small scope |
| Draft a repetitive endpoint | Lower-cost/faster | Existing pattern can be copied |
| Explain a simple Python error | Lower-cost/faster | Limited reasoning required |

This is a guideline, not a strict rule. If the lower-cost model handles a task accurately, there is no reason to escalate it.

---

# 7. Three rules for staying in control

1. **You define the task.** Read the requirement and decide what component you are implementing before asking an agent.
2. **You understand the change.** If you cannot explain what generated code does, ask for an explanation or simplify it before integrating it.
3. **You verify the result.** Run the application, inspect the database/API response, and run tests. Never treat generated code or an agent's confidence as proof that it works.

The best use of AI in a three-hour take-home is to shorten research and implementation time—not to hand over ownership of the project.
