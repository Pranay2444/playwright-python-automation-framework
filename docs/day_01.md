# Day 1: think about the layers, then run the smallest useful flow

Today's task is complete only after you can run, debug, explain and commit the UI and API smoke checks. Reading this page alone is preparation.

## 1. Brainstorm before opening the code - 15 minutes

Write one or two sentences for each question in `learning_log.md` before reading the suggested answers below.

1. The UI URL changes from QA to staging. Which files should change? Why?
2. Ten tests use the same product search selector. Where should it live tomorrow?
3. Why do two cart tests need separate browser contexts?
4. Does a page click prove a product was added to a cart? What would prove it?
5. The API returned product ID `X` yesterday and `Y` today. What should the test do?
6. What belongs in JSON test data, what belongs in environment config and what comes from an API response?
7. Who creates the `page` parameter? Must you create a browser in every test?
8. If a test fails in CI, which evidence would you inspect before changing a timeout?

Suggested reasoning, after you try:

| Question | Reasoning |
| --- | --- |
| Environment change | Change an environment value. Tests read config/fixtures, so URLs should not be repeated in every function. |
| Shared selector | A verified locator belongs in `CatalogPage`, with an action such as `search(term)`. |
| Cart isolation | Contexts have independent cookies/storage. Shared mutable sessions can make the next test depend on the previous one. |
| Click vs result | A click is an action. An assertion on the cart's product ID/name, quantity and price checks the business result. |
| Changing ID | Read current product data from the API or setup fixture. Assert the business rule without assuming yesterday's ID is stable. |
| Data categories | Search examples in JSON; base URLs in env/config; product/cart IDs from the running service; secrets in ignored env/CI Secrets. |
| `page` | `pytest-playwright` provides the fixture. pytest injects it because the test names it as a parameter. |
| Failure evidence | Inspect the failing assertion, trace snapshot, locator matches and relevant request/response or server status. |

## 2. Understand the Day 1 files - 15 minutes

- `requirements.in`: chosen packages. `requirements.txt`: exact resolved versions for repeatable installs.
- `pytest.ini`: tells pytest where tests live, which markers exist and which browser artifact options to apply.
- `.env.example`: committed public defaults. `.env`: your local overrides, ignored by Git.
- `config/settings.py`: reads config once. `load_dotenv(..., override=False)` means environment values from CI win over a local file.
- `conftest.py`: shared setup. pytest discovers it; you do not import it into tests.
- `tests/ui/test_catalog_smoke.py`: a user-visible catalogue check.
- `tests/api/test_products_smoke.py`: a request/response catalogue check.
- `.vscode/`: Python test discovery and two debug configurations.

Only these layers run today. POM, datasets, models, API clients and CI are introduced when we need them.

## 3. Set up and run - 20 minutes

Extract the archive, open `playwright-python-ecommerce` itself in VS Code and follow the README installation commands. Select the virtual environment interpreter.

```bash
python -m pytest --collect-only -q
python -m pytest tests/api -v
python -m pytest tests/ui -v --headed
```

Collection should identify two tests. A collected test has not executed. A successful installation has not proved the business behavior. Read the actual run summary.

If Chromium is missing, run `python -m playwright install chromium` in the same virtual environment. If the public site presents an error page, capture evidence and diagnose availability before editing assertions. Never change the expected behavior to match an unavailable site.

## 4. Explain the first UI test

```python
def test_catalog_displays_products(page: Page) -> None:
    page.goto("/", wait_until="domcontentloaded")
    expect(page).to_have_title(re.compile("Toolshop", re.IGNORECASE))
    products = page.locator('[data-test^="product-"]')
    expect(products.first).to_be_visible()
    assert products.count() > 0
```

- `def` defines a function. The `test_` prefix lets pytest discover it.
- `page` is a fixture parameter: pytest requests it from the plugin. `Page` is a type hint, and `-> None` means this function does not return a result.
- `page.goto("/")` resolves against the `base_url` supplied by our `browser_context_args` fixture.
- `domcontentloaded` means the document is parsed. It does not prove the asynchronous product request has finished.
- `expect(...).to_be_visible()` retries until the state is true or its assertion timeout expires. This is why we do not add a fixed sleep.
- `[data-test^="product-"]` is a CSS attribute-prefix locator. The product collection can contain multiple matches.
- `.first` selects the first matching locator; Python uses a property here.
- `count()` is an immediate count. We wait for a product to be visible first, then assert the collection is non-empty. Do not use an immediate count by itself to wait for loading.
- UI assertions are in the test. Tomorrow the locator/action will move into `CatalogPage` while the expectations stay here.

Browser means browser process. Context means isolated session with its own cookies/storage. Page means a tab in that context. The plugin typically reuses a browser for the session while providing a fresh context/page for each test.

## 5. Explain the API fixture and test

`api_context` is our fixture, not a standard pytest-playwright fixture name. It depends on the plugin's `playwright` fixture, then creates a standalone `APIRequestContext`.

Before `yield`, it prepares a request context with the API base URL, JSON Accept header and request timeout. At `yield`, pytest hands that object to the test. After the test finishes, the `finally` block calls `dispose()`, even when an assertion fails.

The default function scope means a fresh request context for each API test. It does not automatically share cookies with a browser context. Later we can deliberately use `context.request` for a browser-authenticated request or supply storage state to a standalone context; first understand the difference.

The API test calls `get("/products")`, checks `response.status`, parses `response.json()` and checks the `data` collection and product fields. `assert` is right for these already-returned Python values. A status of 200 alone does not guarantee a correct response body.

The API JSON is actual data from the application. It is not an expected dataset that we wrote to make the test pass.

## 6. Debug, then make one controlled failure - 20 minutes

First debug the API test:

1. Put a breakpoint on `body = response.json()`.
2. Select **Day 1: debug API test** in VS Code's Run and Debug panel and press F5.
3. Step over that line. Inspect `response.status`, `body.keys()` and `body["data"][0]`.
4. Explain why the API run does not launch a browser.

Then use Inspector and a UI trace:

```bash
PWDEBUG=1 python -m pytest tests/ui/test_catalog_smoke.py -s
python -m pytest tests/ui --tracing on -v
```

Inspect a product card's real attributes. The fixture configures `data-test` for `get_by_test_id()` because Toolshop's markup uses that name. The CSS locator in today's test works independently of that setting; tomorrow's page-object locators will rely on it.

Open the actual `trace.zip` under `test-results/`:

```bash
python -m playwright show-trace <actual-path-to-trace.zip>
```

Temporarily replace the title regex with `Definitely Wrong Title`. Run again using normal failure retention. Find the failing assertion and its snapshot in the trace. Restore the expectation and rerun. Record the cause and fix; do not commit the intentionally wrong expectation.

Optional stretch: temporarily assert that API status is 201. Observe the failure message, then restore 200. Explain why changing the assertion back is valid here: you intentionally broke a known contract check.

## 7. Use AI as a tutor - 10 minutes

Ask:

> Explain this conftest.py one fixture at a time. For each fixture, tell me who creates it, who receives it, when it runs and how cleanup works. Ask me a recall question after each explanation. Do not rewrite the project.

Then ask:

> Review my two smoke tests. Identify which assertion proves a business behavior and which check is only a basic availability check. Suggest one improvement, explain its purpose, and wait while I implement it.

Run and review any code suggestion yourself. A plausible explanation is not a passing test run.

## 8. Commit and explain - 10 minutes

Use the README's Git commands for a new empty repository, or clone your existing repository and work on a branch. Inspect `git diff --cached` before committing.

Complete the learning log. Say this aloud:

> I started with pytest-playwright's isolated page fixture for the UI and a separate APIRequestContext fixture for the API. I put environment settings in config, runner settings in pytest.ini and cleanup in conftest.py. The UI test proves the catalogue renders, while the API test validates status and basic product fields. I use web-first assertions for dynamic UI state and ordinary assertions for returned API values. Tomorrow I will extract repeated UI actions into a page object and parameterize search cases from JSON.

Before moving to Day 2, send your actual test results, four short brainstorming answers and, if available, your GitHub repository URL.
