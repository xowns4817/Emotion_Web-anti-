from dotenv import load_dotenv
import os

load_dotenv()

# LLM (Google Gemini)
LLM_API_KEY = os.getenv("GOOGLE_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.0-flash")

# Spring Boot Callback
SPRING_BOOT_URL = os.getenv("SPRING_BOOT_URL", "http://localhost:8080")

# MCP Server
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:3001")

# FastAPI
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
