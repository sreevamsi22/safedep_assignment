# SafeDep Assignment

## Overview
This project is designed to synchronize shell command history across multiple systems. It enables seamless access to your frequently used shell commands, making switching between systems or working on temporary cloud VMs effortless.

## Features
- **Command History Synchronization**: Automatically syncs shell history (PowerShell, CMD) across systems.
- **API Integration**: Uses an existing API to store and retrieve commands.
- **Automation**: Supports periodic synchronization through an executable script.

## Problem Statement
Shells like PowerShell and CMD store command history locally, which becomes a problem when switching systems. This project solves that by:
- Fetching command history from local files.
- Uploading it to a central API for storage.
- Synchronizing the history across multiple systems.

## Folder Structure
- `api_db.py`: Handles the database logic and API interactions.
- `sync_script.py`: Automates synchronization tasks between systems.
- `safedep_assignment.py`: Orchestrates the entire workflow.

## How to Use
### Prerequisites
- Python 3.8 or above installed.
- Required Python libraries: 
  pip install flask
  pip install requests    
