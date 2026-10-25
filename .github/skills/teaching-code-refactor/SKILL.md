---
name: teaching-code-refactor
description: "Refactor code for teaching and learning, prioritizing readability and correctness over production hardening, clever abstractions, deduplication, or optimization. Use for teaching-friendly code, educational code, tutorial-ready examples, learning-oriented or learning-focused code, beginner-friendly code, pedagogical or didactic refactoring, classroom or workshop demos, onboarding walkthroughs, explainable code, and requests to make code easy to follow, learn from, teach, or explain. Invoke with /teaching-code-refactor."
---

# Teaching code refactor

Make the code itself a useful explanation. A learner should be able to find the
entry point, follow the important work in order, and see what each step consumes,
produces, and can fail on. Readability and correct behavior are the goals, not
maximum performance, minimum line count, or production-grade extensibility.

## Recall and scope

Invoke as:

- `/teaching-code-refactor <file or feature>`
- `/teaching-code-refactor <file> using <reference file> as the style`
- "Make this code teaching-friendly / tutorial-ready / easy to learn from."
- "Clean this up for a workshop, classroom demo, onboarding, or code walkthrough."
- "Refactor for educational clarity, learnability, or pedagogical readability."

Work on the named files or one bounded end-to-end flow. Ask only when the target,
audience, or intended behavior is materially ambiguous. Use the user's style
reference when supplied; otherwise follow the repository's clearest comparable
example. Assume learners know the language basics but not this application's
architecture unless the user specifies otherwise.

For an assessment-only request, report the rubric and suggested reading path
without editing. Otherwise, implement the bounded refactor and verify it.
This is not permission to deploy, publish, change dependencies, or rewrite the
whole project.

## Attributes of code that teaches well

| Attribute | What to look for |
| --- | --- |
| Visible entry point | One obvious place to start, with the main lifecycle stated briefly. |
| Sequential story | The normal path reads top to bottom in execution order. |
| Meaningful stages | Short, named domain steps such as read inputs, generate, validate, and save. |
| Low navigation burden | Essential behavior is not hidden behind chains of single-use wrappers. |
| Explicit data handoffs | Descriptive variables, parameters, return values, and types show what moves between steps. |
| Visible side effects | Network calls, model calls, persistence, resource ownership, and cleanup are apparent. |
| Correct failure behavior | Validation, errors, deadlines, recovery, and uncertain outcomes remain visible and accurate. |
| Purposeful explanation | Comments explain a boundary or a non-obvious reason, not each line's syntax. |
| Proportionate structure | Helpers have a concrete purpose; abstractions do not overwhelm the concept being taught. |

Do not turn the rubric into an invented numeric score or a function-length
quota. A longer linear method can teach better than many short methods, but a
giant method with unrelated responsibilities is not the goal.

## Workflow

### 1. Establish the reading path and behavior

1. Read repository instructions, the index when present, the target, its style
   reference, and directly relevant tests and call sites.
2. Identify the entry point and describe the actual lifecycle in one sentence.
3. Note concrete friction: wrapper hops, hidden side effects, vague names,
   compressed expressions, deep nesting, or stages scattered out of order.
4. Identify behavior to preserve: outputs and public signatures, validation,
   authorization, exceptions, resource lifetime, persistence order, and recovery.
5. Use existing tests to establish a baseline. Preserve unrelated dirty changes.

Do not mistake defensive code for unnecessary complexity. Understand why a
check or journal exists before moving it.

### 2. Choose the simplest teachable shape

Default to a linear entry method with a few meaningful stages inline. Numbered
comments such as `# STAGE 1: Read the assigned inputs.` are useful for a real
lifecycle, not for every small function.

- Inline single-use orchestration helpers when they only obscure the sequence.
- Keep helpers for genuinely shared correctness rules, substantial reusable
  operations, resource management, or real framework/checkpoint boundaries.
- When distinct stages warrant methods, let the entry method call them directly.
  Put them immediately below it in execution order, with explicit handoffs.
  Avoid stages calling other stages or hiding the next step.
- Prefer domain names such as `requirements`, `design`, and `review` over
  generic `data`, `value`, `handle`, or `process` when the distinction matters.
- Prefer ordinary statements and clear branches over clever comprehensions,
  nested ternaries, callback machinery, or packed multi-assignment.
- Use early returns to expose completed, invalid, or held states without
  burying the normal path.
- Accept a little local duplication when it makes separate roles understandable.
  Do not duplicate shared validation or authorization rules.
- Keep useful type information and use the repository's existing types.
  Do not introduce a pipeline framework, service layer, registry, base class,
  generic state bag, or configuration switch just for this refactor.

### 3. Refactor without changing the lesson's truth

Keep the important work visible at the point where it happens. For example:

```python
async def create_design(assignment, store, model):
    # STAGE 1: Read the exact inputs assigned to this operation.
    requirements = await store.read_requirements(assignment.requirements_ref)

    # STAGE 2: Generate a design from those requirements.
    design = await model.design(requirements)

    # STAGE 3: Validate before publishing the result.
    validate_design(design, assignment)
    return await store.save_design(design, assignment)
```

This is a structural illustration, not a drop-in implementation or permission
to remove a real application's resource, authorization, or recovery handling.

Preserve these boundaries in real code:

- Keep checks before the operations they protect.
- Keep write-ahead records before remote effects and observed IDs before recovery.
- Preserve locks, ETags, transactions, immutable writes, and checkpoint semantics.
- Keep known-response recovery distinct from a new request; never replay an
  unknown side effect to make an example look successful.
- Keep cancellation, timeouts, exception scope, and cleanup behavior intact.
- Do not replace real errors with broad catches, silent defaults, fake success,
  unchecked casts, or a hidden local/mock implementation.
- Keep required contracts and compatibility behavior. Do not rename public APIs
  solely to make the example prettier.

Use a short lifecycle docstring and only the stage comments or explanations
that help a reader. Avoid line-by-line narration and long tutorial essays
embedded in the code. Update directly related navigation or documentation.

### 4. Verify both correctness and learnability

Run the smallest relevant existing checks, then any repository-required suite.
Add focused tests where moved branches or sequencing need protection, especially
early returns, failures, cleanup, and resume without duplicate effects.
Do not weaken existing assertions or install tooling without a demonstrated need.

Walk the final entry path as a learner:

1. Can I locate where execution starts?
2. Can I describe the main stages in order without chasing wrapper chains?
3. Can I see the inputs, outputs, external calls, writes, and cleanup?
4. Can I tell why a result is accepted, rejected, recovered, or held?
5. Did the refactor reduce conceptual burden rather than just move it elsewhere?

Inspect targeted code only when a concrete question remains; do not repeatedly
reread the full diff. Confirm behavior with tests, not a readability claim.

## Completion response

Return a short summary containing:

- The reading path and specific teaching attributes improved, linked to the code.
- The important behavior and correctness boundaries preserved.
- Exact checks run, their results, and any unverified or blocked conditions.

For an assessment, use a compact attribute / evidence / proposed change table.
Do not claim production readiness, deployment, performance gains, or verified
behavior beyond the evidence collected.
