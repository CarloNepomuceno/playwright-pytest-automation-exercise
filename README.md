# Automation Exercise test framework

![Smoke tests](https://github.com/CarloNepomuceno/playwright-pytest-automation-exercise/actions/workflows/tests.yml/badge.svg)

I built this to practice what I learned in a Playwright + Python course, but on a
different site than the one used in the lessons. It tests
https://automationexercise.com, a practice online store, through both the
browser and the API.

Stack: Python, Playwright, pytest, pytest-bdd.

## What's in it

- API tests for login verification and the products list
- UI tests for registration, product search, cart, and checkout/payment
- One hybrid test: the API creates a user, the browser logs in and buys a product,
  then the API deletes the user afterwards
- Two network tests: one blocks images while shopping, the other makes the
  add-to-cart request fail and checks the cart stays empty
- One BDD scenario for the purchase flow

15 tests in total.

## How it's set up

Each page of the site has its own class in `pageObjects/`. The methods return the
next page, so a test reads like the user's steps (login, then products, then cart, and so on).

Every test that needs a logged-in user gets a fresh one from a `newUser` fixture.
It creates the account through the API before the test and deletes it afterwards,
even if the test failed. Because tests never share an account, they can run in
parallel.

The API helper in `utils/apiBase.py` retries when the site returns an error page
instead of JSON, which happens when it's busy.

The browser fixture in `conftest.py` blocks ad requests, since the ads on this site
sometimes cover buttons and break clicks. There's also a `--browser_name` option
(chrome or firefox) and a `--run_headless` flag.

## Folder layout

```
Features/         purchase.feature
data/             user_profiles.json (fake test user data only)
pageObjects/      login, home, products, cart, checkout, payment, signup
utils/            apiBase.py
conftest.py       fixtures and options
pytest.ini        markers
test_*.py         the tests
```

## Running it

I used Python 3.14 on Windows.

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

Smoke tests only (4 tests, about 15 seconds):

```
pytest -m smoke --run_headless
```

Everything, in parallel, with an HTML report (about a minute):

```
pytest -n 2 --reruns 1 --run_headless --html=report.html --self-contained-html
```

Other browser:

```
pytest --browser_name firefox --run_headless
```

Markers you can use with `-m`: smoke, ui, api, hybrid, network, bdd.

## Things to know

The site is a shared public one and gets slow sometimes, so a test now and then
fails once and passes on the retry. That's why I run with `--reruns 1`.

The tests that use pytest-playwright's built-in `page` fixture run headless by
default. The ones using my own `browserInstance` fixture open a visible browser
unless you pass `--run_headless`.
