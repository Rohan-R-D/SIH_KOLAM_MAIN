# Docker Troubleshooting Guide for Python Web Apps

## Top 8 Common Issues and Fixes

1. **Missing Dependencies**
   - Issue: Package not found errors during container startup
   - Fix: `RUN pip install --no-cache-dir -r requirements.txt && pip install <missing_package>`

2. **File Path and CWD Issues**
   - Issue: Files not found or incorrect working directory
   - Fix: `WORKDIR /app` and ensure all file references use relative paths from this directory

3. **Port Mismatches**
   - Issue: App running but not accessible from host
   - Fix: `EXPOSE 5000` and ensure app binds to `0.0.0.0` not `127.0.0.1` with `app.run(host='0.0.0.0')`

4. **Permission Issues**
   - Issue: Permission denied when writing to files/directories
   - Fix: `RUN chown -R nonroot:nonroot /app && chmod -R 755 /app`

5. **Environment Variables**
   - Issue: Missing configuration or secrets
   - Fix: `ENV FLASK_ENV=production` or use `docker run -e FLASK_ENV=production` for runtime variables

6. **Large Image Size**
   - Issue: Slow builds and deployments
   - Fix: `FROM python:3.11-slim` and add `--no-cache-dir` to pip install commands

7. **Dev Server vs Production Server**
   - Issue: Using Flask's development server in production
   - Fix: `CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]` instead of `python app.py`

8. **Missing .dockerignore**
   - Issue: Unnecessary files bloating the image
   - Fix: Create `.dockerignore` with entries for `__pycache__/`, `*.pyc`, `venv/`, `.git/`, etc.

## 3-Step Sanity Checklist

1. **Verify Container Starts Successfully**
   ```bash
   docker run -d --name test-container -p 5000:5000 your-image-name && docker logs test-container
   ```
   ✓ Check for successful startup messages and no errors

2. **Confirm Application Accessibility**
   ```bash
   curl http://localhost:5000/ || wget -qO- http://localhost:5000/
   ```
   ✓ Verify you receive the expected HTML/JSON response

3. **Validate Core Functionality**
   ```bash
   docker exec -it test-container /bin/sh -c "ls -la /app && pip list && env | grep FLASK"
   ```
   ✓ Confirm files exist, dependencies are installed, and environment variables are set

## Quick Recovery Commands

```bash
# Clean up test container
docker stop test-container && docker rm test-container

# Rebuild image with no cache
docker build --no-cache -t your-image-name .

# Run with interactive shell for debugging
docker run -it --rm your-image-name /bin/sh
```