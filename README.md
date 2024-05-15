# Installing the package `helpScannerS`

1. create virtual environment inside sh-bbyy-pheno
`python3 -m venv .venv`

2. activate the virtual environment
`source .venv/bin/activate`

3. install dependencies (package versions used as of working on this project)
`pip3 install -r requirements.txt`

4. enter helpScannerS
`cd helpScannerS`

5. make sure you have the latest version of pip installed (otherwise some commands
might not work)
`python3 -m pip install --upgrade pip`

6. upgrade build to latest version
`pip3 install --upgrade build`

7. run build (must be done inside the directory helpScannerS)
`python3 -m build`

8. install helpScannerS as an editable package (must be done inside the directory
helpScannerS)
`pip3 install --editable .`
