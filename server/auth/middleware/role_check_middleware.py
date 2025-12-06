from fastapi import HTTPException
from server.user.enum.user_role_enum import UserRole
class RoleChecker:
    def require_admin(self, user):
        if user.get("role") != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Admin access required")
