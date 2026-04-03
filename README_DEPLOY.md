Deployment guide

Build Docker image (core only):

```bash
# Build without AI extras (faster, smaller image)
docker build -t rwanda-exports:latest .

# Build with AI extras (heavy; may require additional system libs)
docker build --build-arg INSTALL_AI=1 -t rwanda-exports:ai .
```

Run container:

```bash
docker run -p 8501:8501 rwanda-exports:latest
```

Deploy to Heroku (container):

- Use a Heroku container-based deployment or adapt `Procfile` for buildpacks.
- Make sure large model/AI deps are installed only if necessary.

Notes and tips:
- The `ai_chat` assistants are optional. If AI extras are not installed, the app will show helpful errors instead of failing on import.
- Some packages (Prophet, XGBoost, torch/faiss) may require build tools or platform-specific wheels; prefer installing on Linux images (Docker) or using pinned whls.
- For Windows deployment/testing, use a matching Python version and install Visual C++ Build Tools to compile native extensions.
