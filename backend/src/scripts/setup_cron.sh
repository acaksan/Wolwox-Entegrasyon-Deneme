#!/bin/bash
(crontab -l 2>/dev/null; echo "0 0 * * * cd /path/to/backend/src && python scripts/log_management.py") | crontab - 