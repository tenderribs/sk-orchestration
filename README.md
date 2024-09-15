# Stadtklima Ingest Service

Notice: ATM corporate proxies are completely bypassed out of convenience.

## Installation [Dev]

### VSCode Devcontainer

> Prerequisite: Docker installed and ready to go.

1. Clone the repo and open in vscode
2. Copy and rename the `.env.example` to `.env` and set secret tokens / API keys / passwords
3. Click the light blue button on the bottom left, "reopen folder in container"

### Manual Installation

1. Clone the repo and open in vscode
2. Manually install and configure PostgreSQL and Python to your liking.
3. Copy and rename the `.env.example` to `.env` and set secret tokens / API keys / passwords
4. Install python libraries using

    ```sh
    pip install -r requirements.txt
    ```