## [Test(s)](./tests/verification_test.py):
* **[Install CATs](https://github.com/BlockScience/cats/tree/cats2?tab=readme-ov-file#installation)**
* **[Create Virtual Environment](./docs/ENV.md)**
* **Activate Virtual Environment**
  ```bash
  cd cats
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