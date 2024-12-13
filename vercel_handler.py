from proxy import app  # Import your FastAPI app from proxy.py
from vercel_asgi import VercelASGI

handler = VercelASGI(app)
