## [Test(s)](./tests/verification_test.py):
* **Virtual Environment:**
  1. [Create Virtual Environment](./docs/ENV.md)
  2. Activate Virtual Environment
  ```bash
  cd <CATs parent directory>/cats-research
  source ./venv/bin/activate
  # (venv) $
  ```
* **Session 1**
  ```bash
  # (venv) $
  PYTHONPATH=./ python cats/node.py
  ```
* **Session 2**
  ```bash
  # (venv) $
  pytest -s tests/verification_test.py
  ```