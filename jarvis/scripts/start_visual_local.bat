@echo off
cd /d C:\jarvis
call .venv\Scripts\activate
python -m jarvis.main --mode local --visual
