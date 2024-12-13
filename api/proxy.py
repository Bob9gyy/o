from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
import httpx
import os
from bs4 import BeautifulSoup

app = FastAPI()

# Password stored in environment variable
PASSWORD = os.getenv("PROXY_PASSWORD", "defaultpassword")

@app.middleware("http")
async def password_protect(request: Request, call_next):
    """
    Middleware to enforce password protection.
    The client must provide the correct password in the Authorization header.
    """
    auth = request.headers.get("Authorization")
    if not auth or auth != f"Bearer {PASSWORD}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await call_next(request)

@app.get("/", response_class=HTMLResponse)
async def web_proxy(url: str = Query(None, description="The URL to proxy")):
    """
    A simple web proxy endpoint. Users provide a target URL as a query parameter.
    """
    if not url:
        return HTMLResponse(content="""
        <html>
            <head><title>Web Proxy</title></head>
            <body>
                <h1>Enter the URL you want to browse:</h1>
                <form method="get">
                    <input type="text" name="url" placeholder="https://example.com" required />
                    <button type="submit">Go</button>
                </form>
            </body>
        </html>
        """, status_code=200)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={"User-Agent": "WebProxy/1.0"})
        response.raise_for_status()

        # Parse and rewrite HTML
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all(["a", "link", "script", "img"]):
            attr = "href" if tag.name in ["a", "link"] else "src"
            if tag.get(attr):
                tag[attr] = f"/?url={tag[attr]}"  # Rewrite URLs to pass through the proxy

        return HTMLResponse(content=str(soup), status_code=200)

    except Exception as e:
        return HTMLResponse(content=f"<h1>Error</h1><p>{str(e)}</p>", status_code=500)

