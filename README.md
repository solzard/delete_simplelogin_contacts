# Delete a SimpleLogin user's all contacts.
## Usage
1. `echo "SIMPLELOGIN_API_KEY = YOUR_API_KEY" > .env`
2. `poetry run python delete_simplelogin_contacts.py`

## Disclaimer
This scripts works as of Apr 8, 2022; however, its implementation thoroughly relies on SimpleLogin's API design. Please double check [the official document](https://github.com/simple-login/app/blob/master/docs/api.md) before your use 😀

