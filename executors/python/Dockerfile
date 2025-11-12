# 1. Base Image
FROM python:3.11-slim

# 2. Set Working Directory: /app inside the container
WORKDIR /app

# 3. Copy Executor Script: (Updated path)
# Copies from the build context (Desktop/CPTJudge) into the container's /app
COPY CptJudge/executors/python/python_executor.py /app/python_executor.py

# 4. Define Entrypoint
ENTRYPOINT ["python", "python_executor.py"] 

# # 5. Default Command
# CMD ["Usage: Pass test_number as argument."]