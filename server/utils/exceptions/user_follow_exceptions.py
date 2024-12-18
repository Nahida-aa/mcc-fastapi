from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class SelfFollowedException(HTTPException):
    def __init__(
        self,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Following/Unfollowing self not allowed!",
            headers=headers,
        )