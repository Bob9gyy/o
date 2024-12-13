# Web Proxy with Password Protection

This project implements a web proxy with password protection using FastAPI, designed for deployment on Vercel.

## Features
- **Password Protection**: Clients must provide a valid password in the `Authorization` header.
- **Web Proxy**: Users can browse a target website via the proxy by specifying the URL in a query parameter.
- **Deployable on Vercel**: Works seamlessly with Vercel's serverless infrastructure.

## Setup

### Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
