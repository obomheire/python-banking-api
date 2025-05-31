from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.app.api.routes.auth.deps import CurrentUser
from backend.app.api.services.profile import get_all_user_profiles
from backend.app.core.db import get_session
from backend.app.core.logging import get_logger
from backend.app.user_profile.schema import (
    PaginatedProfileResponseSchema,
    ProfileResponseSchema,
)

logger = get_logger()

router = APIRouter(prefix="/profile")


@router.get(
    "/all",
    response_model=PaginatedProfileResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def list_user_profiles(
    current_user: CurrentUser,
    session: AsyncSession = Depends(get_session),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1),
) -> PaginatedProfileResponseSchema:
    try:
        users, total_count = await get_all_user_profiles(
            session=session, current_user=current_user, skip=skip, limit=limit
        )

        profile_responses = [
            ProfileResponseSchema(
                username=user.username or "",
                first_name=user.first_name or "",
                middle_name=user.middle_name or "",
                last_name=user.last_name or "",
                email=user.email or "",
                id_no=str(user.id_no) if user.id_no else "",
                role=user.role,
                profile=user.profile,
            )
            for user in users
        ]

        return PaginatedProfileResponseSchema(
            profiles=profile_responses, total=total_count, skip=skip, limit=limit
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logger.error(f"Error fetching all user profiles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Failed to fetch user profiles",
                "action": "Please try again later",
            },
        )
