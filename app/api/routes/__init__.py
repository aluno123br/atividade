from app.api.routes.health import router as health_router
from app.api.routes.profiles import router as profiles_router
from app.api.routes.projects import router as projects_router
from app.api.routes.technologies import router as technologies_router

__all__ = ["health_router", "profiles_router", "projects_router", "technologies_router"]
