from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI
from app.models.admin_model import Base
from app.config.database import engine

# routers
from app.routes.admin_routes import router as admin_router
from app.routes.staff_routes import router as staff_routes

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


# setup seeds
from app.seeds.seed_admin import user_seed_data
# user_seed_data()

# setup migrations

# Mount the directory containing the YAML file as a static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["Base"])
async def hello_world():
    """
    Base endpoint returning a Hello World message.
    This function responds to the root URL and is typically used to verify
    that the service is operational.
    
    Returns:
        dict: A message saying "We're live"
    """
    return {"message": "We're live 🎉 🚀 😍"}

@app.get("/docs/", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/static/swagger.yaml",  # Path to your YAML file
        title="Custom Swagger UI",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.52.5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.52.5/swagger-ui.css",
    )


# Initialize the FastAPI app.
# This object creates an ASGI application that can receive requests and
# send responses.
app = FastAPI()

# Create database tables.
# It connects to the database using the engine from the database configuration and ensures all tables are created before the application starts.
# It's crucial for initial setup and ensuring the database schema is ready.
Base.metadata.create_all(bind=engine)

# Include routers.
# Routers in FastAPI are used to manage different endpoints. In this case, the user routes are included.
# This modular approach allows for easy maintenance and scaling of the
# application as routes are logically separated.
app.include_router(admin_router)

# Main entry point of the application when run as a standalone script.
# The condition `if __name__ == "__main__"` makes sure the server is only run when this script is executed directly,
# and not when it's imported as a module.
# Uvicorn is an ASGI server that runs the FastAPI application. It's configured to listen to all available IP addresses
# (host "0.0.0.0") and on port 8000, which are common default settings for web applications.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)