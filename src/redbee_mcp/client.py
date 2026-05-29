"""
HTTP client for Red Bee Media OTT Platform Exposure API.
Documentation: https://exposure.api.redbee.live/docs
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

import httpx

from .models import AuthenticationResponse, RedBeeConfig

logger = logging.getLogger(__name__)


class RedBeeAPIError(Exception):
    """Raised when the Red Bee API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class RedBeeClient:
    """Async HTTP client for Red Bee Media APIs with connection pooling."""

    def __init__(self, config: RedBeeConfig):
        self.config = config
        self.session_token: Optional[str] = config.session_token
        self.device_id: Optional[str] = config.device_id
        self.username: Optional[str] = config.username
        self.account_id: Optional[str] = None
        self._http: Optional[httpx.AsyncClient] = None
        self._base_headers = {
            "User-Agent": "RedbeePlayer/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        timeout = httpx.Timeout(float(config.timeout), connect=10.0)
        self._client_kwargs = {
            "timeout": timeout,
            "follow_redirects": True,
            "verify": True,
        }

    async def __aenter__(self) -> "RedBeeClient":
        self._http = httpx.AsyncClient(**self._client_kwargs)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def close(self) -> None:
        if self._http is not None:
            await self._http.aclose()
            self._http = None

    def _ensure_client(self) -> httpx.AsyncClient:
        if self._http is None:
            self._http = httpx.AsyncClient(**self._client_kwargs)
        return self._http

    def _build_url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        base = self.config.exposure_base_url.rstrip("/")
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{base}{path}"

    def _auth_headers(self, include_auth: bool) -> Dict[str, str]:
        headers = dict(self._base_headers)
        if include_auth and self.session_token:
            headers["Authorization"] = f"Bearer {self.session_token}"
        return headers

    async def _make_request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        include_auth: bool = True,
        use_auth: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Execute an HTTP request against the Exposure API."""
        if use_auth is not None:
            include_auth = use_auth

        body = data if data is not None else json_data
        url = self._build_url(path)
        headers = self._auth_headers(include_auth)
        client = self._ensure_client()
        method_upper = method.upper()

        try:
            if method_upper == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method_upper == "POST":
                response = await client.post(url, headers=headers, params=params, json=body)
            elif method_upper == "PUT":
                response = await client.put(url, headers=headers, params=params, json=body)
            elif method_upper == "DELETE":
                response = await client.delete(url, headers=headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            logger.info("REQUEST %s %s -> %s", method_upper, path, response.status_code)

            if response.status_code >= 400:
                detail = response.text[:500] if response.text else response.reason_phrase
                raise RedBeeAPIError(
                    f"API error: {detail}",
                    status_code=response.status_code,
                )

            if response.status_code == 204:
                return {"success": True, "message": "No content"}

            content_type = response.headers.get("content-type", "")
            if content_type.startswith("application/json"):
                result = response.json()
                if isinstance(result, dict):
                    return result
                return {"data": result}

            return {"text": response.text, "status_code": response.status_code}

        except httpx.RequestError as exc:
            logger.error("Request error for %s %s: %s", method_upper, path, exc)
            raise RedBeeAPIError(f"HTTP request failed: {exc}") from exc

    def _parse_expires_at(self, value: Any) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return None
        return None

    async def authenticate(self, username: str, password: str) -> AuthenticationResponse:
        """Authenticate with username and password (v2 API)."""
        result = await self._make_request(
            "POST",
            f"/v2/customer/{self.config.customer}/businessunit/{self.config.business_unit}/auth/login",
            data={
                "username": username,
                "password": password,
                "device": {
                    "deviceId": self.device_id,
                    "type": "WEB",
                },
            },
            include_auth=False,
        )

        self.session_token = result.get("sessionToken")
        self.device_id = result.get("deviceId") or self.device_id
        self.account_id = result.get("accountId")

        if not self.session_token:
            raise RedBeeAPIError("Authentication succeeded but no session token was returned")

        return AuthenticationResponse(
            session_token=self.session_token,
            device_id=self.device_id or "",
            expires_at=self._parse_expires_at(result.get("expiresAt")),
        )

    async def authenticate_anonymous(self) -> Dict[str, Any]:
        """Create an anonymous session (v2 API)."""
        result = await self._make_request(
            "POST",
            f"/v2/customer/{self.config.customer}/businessunit/{self.config.business_unit}/auth/anonymous",
            data={
                "device": {
                    "deviceId": self.device_id,
                    "type": "WEB",
                },
            },
            include_auth=False,
        )
        if result.get("sessionToken"):
            self.session_token = result["sessionToken"]
        if result.get("deviceId"):
            self.device_id = result["deviceId"]
        return result

    async def login(self, username: str, password: str) -> Dict[str, Any]:
        """Legacy login helper returning raw API payload."""
        auth = await self.authenticate(username, password)
        return {
            "sessionToken": auth.session_token,
            "deviceId": auth.device_id,
            "accountId": self.account_id,
            "expiresAt": auth.expires_at.isoformat() if auth.expires_at else None,
        }

    async def create_anonymous_session(self) -> Dict[str, Any]:
        """Legacy alias for anonymous session creation."""
        return await self.authenticate_anonymous()
