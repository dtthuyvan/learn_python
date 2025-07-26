Install requirement package if needed
cd to host_agent folder and run: py agent.py
This appeal is ok: Uvicorn running on http://127.0.0.1:10000 (Press CTRL+C to quit)

From UI, call api with prompt to get result:
curl sample: 
curl --location 'http://127.0.0.1:10000/prompt' \
--header 'Content-Type: application/json' \
--data '{
    
    "prompt": "Find employees with full attendance on 2025-07-26"
}'