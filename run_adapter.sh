#!/bin/bash
# run_adapter.sh
export PYTHONPATH=src
exec uvicorn ai_models.cultural_adapter.api:app --reload
