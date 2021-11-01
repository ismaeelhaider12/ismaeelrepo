name: pylint

on:
  push:
    branches:
      - master
      - develop
      - release/*
      - feature/*
      - hotfix/*
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
      with:
        fetch-depth: 100

    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pylint pytest pytest-cov selenium playwright
    - name: Running pytest
      run: |
        pytest -v  --cov --cov-report=xml --cov-report=html
    - name: Analysing the code with pylint
      continue-on-error: true
      run: |
        pylint src/git_graph_automation
    - name: SonarCloud Scan
      uses: SonarSource/sonarcloud-github-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Needed to get PR information, if any
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
