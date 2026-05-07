from fastapi import APIRouter

from app.api.routes import (
    pharmacy,
    update_profile,
    request,
    response,
    get_request,
    get_response,
    order,
    refresh_token,
    send_otp,
    verify_otp,
    verify_pharmacy,
    get_order,
    order_status,
    get_pharmacy_request,
)

api_router = APIRouter()


# =========================
# Authentication Routes
# =========================
api_router.include_router(
    send_otp.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    verify_otp.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    refresh_token.router,
    prefix="/auth",
    tags=["Authentication"]
)


# =========================
# User Routes
# =========================
api_router.include_router(
    update_profile.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    request.router,
    prefix="/users/requests",
    tags=["Requests"]
)

api_router.include_router(
    get_response.router,
    prefix="/users/responses",
    tags=["Responses"]
)

api_router.include_router(
    get_order.router,
    prefix="/users/orders",
    tags=["Orders"]
)


# =========================
# Pharmacy Routes
# =========================
api_router.include_router(
    pharmacy.router,
    prefix="/pharmacies",
    tags=["Pharmacies"]
)

api_router.include_router(
    verify_pharmacy.router,
    prefix="/pharmacies",
    tags=["Pharmacies"]
)

api_router.include_router(
    response.router,
    prefix="/pharmacies/responses",
    tags=["Responses"]
)

api_router.include_router(
    get_pharmacy_request.router,
    prefix="/pharmacies/requests",
    tags=["Pharmacies"]
)


# =========================
# Common Request Routes
# =========================
api_router.include_router(
    get_request.router,
    prefix="/requests",
    tags=["Requests"]
)


# =========================
# Order Routes
# =========================
api_router.include_router(
    order.router,
    prefix="/orders",
    tags=["Orders"]
)

api_router.include_router(
    order_status.router,
    prefix="/orders",
    tags=["Orders"]
)