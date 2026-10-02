# Use AI without losing the test's purpose

AI assistance is available from Day 1 through chat or your editor. Special agent infrastructure is not a prerequisite for Python Playwright tests.

## Tutor prompt

> Work as my Playwright Python tutor. This repo uses pytest-playwright's sync API. Give me one small task at a time. Explain why a change belongs in tests, POM, fixtures, config or test data. Let me try first, then review my patch. Do not generate the remaining four days of framework code at once.

## Scenario brainstorming prompt

> For Toolshop's product search, propose five cases covering a positive search, no results, input boundaries and an interrupted request. For each, state the requirement we must confirm, the input, the observable expected result and the best layer to test it. Do not invent behavior or selectors. Ask me to choose one case before writing code.

## Small patch prompt

> Using the supplied live locator evidence and the chosen requirement, propose a minimal pytest-playwright sync test. Use existing fixtures/page objects, put business assertions in the test and avoid fixed sleeps. Explain every changed file and what failure the assertion would catch.

## Failure investigation prompt

> Here is the failing assertion and redacted trace/request evidence. Separate confirmed observations from hypotheses. Suggest one diagnostic step before changing a locator or timeout. Do not delete the assertion, skip the test, add a blanket retry or use broad exception handling to make the run pass.

## Review before committing

- Is the scenario based on a real requirement or verified API contract?
- Were selectors confirmed against the actual page?
- Does the assertion fail when the intended business behavior is broken?
- Does the test use isolated data/session state?
- Do imports and methods match Python's sync API?
- Did the actual test run pass, and can I explain the patch?

On Day 5, encode these project rules in the instruction file your chosen editor/agent actually reads. `AGENTS.md` is guidance for compatible agents, not a Python executable. A `SKILL.md` can describe a reusable workflow for a supporting tool; pytest does not run it automatically. Add either only with a clear consumer and purpose.

Playwright's documented planner/generator/healer tooling uses Playwright Test's Node runner. It should not be presented as a native pytest feature. MCP can support site inspection in a compatible editor; it does not replace the Python suite's assertions or CI exit code.
