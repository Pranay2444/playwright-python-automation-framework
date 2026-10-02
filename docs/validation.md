# Preparation validation

Checked on 30 September 2026 with Python 3.12.14, Playwright 1.63.0, pytest 9.1.1 and pytest-playwright 0.9.0.

| Check | Result |
| --- | --- |
| Python source syntax | All five Python source files parsed successfully |
| VS Code config | All three JSON files parsed successfully |
| Dependency file | 19 resolved packages pinned in `requirements.txt` |
| pytest discovery from the project folder | Two tests collected; registered marks recognized without warnings |
| Live API response | GET `/products` returned the expected catalogue object and product fields |
| API test through the environment's explicit HTTP proxy | `1 passed` |
| UI runtime and recorded UI trace | Not verified in this preparation environment |
| GitHub commit/push and CI | Not performed; repository URL was not supplied |

The initial direct API request failed DNS resolution in the restricted preparation environment. The optional `PW_PROXY_SERVER` setting allowed the real Playwright API test to use the environment's network proxy; that test then passed. Leave this option empty on a normal direct network.

Both full Chromium and its headless-shell downloads returned invalid/truncated archives, so no claim is made that the browser test or trace-viewing exercise passed here. The UI selector pattern follows the handbook's Toolshop examples; verify the current DOM and run the test locally before marking Day 1 complete.

Expected local checks:

```bash
python -m playwright install chromium
python -m pytest tests/api -v
python -m pytest tests/ui -v --headed
python -m pytest tests/ui --tracing on -v
```

No assertions were weakened to turn the infrastructure failures into passing tests. Later layers and CI are learning tasks, not completed implementation.
