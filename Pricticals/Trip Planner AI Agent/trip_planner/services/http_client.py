from __future__ import annotations

import time
from typing import Any

import requests

from trip_planner.config import Settings


class HttpError(RuntimeError):
    pass


class ResilientHttpClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "TripPlannerAIAgent/1.0 (learning-project)",
                "Accept": "application/json",
            }
        )

    def request(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        data: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any] | list[Any] | str:
        retries = max(1, self.settings.http_retries)
        backoff = max(0.1, self.settings.http_backoff_seconds)
        last_error: Exception | None = None

        for attempt in range(1, retries + 1):
            try:
                response = self.session.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    data=data,
                    headers=headers,
                    timeout=self.settings.http_timeout_seconds,
                )

                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else backoff * attempt
                    time.sleep(delay)
                    continue

                if response.status_code >= 400:
                    raise HttpError(
                        f"HTTP {response.status_code} from {url}: {response.text[:300]}"
                    )

                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return response.json()
                return response.text
            except (requests.RequestException, HttpError) as exc:
                last_error = exc
                if attempt < retries:
                    time.sleep(backoff * attempt)
                    continue
                break

        raise HttpError(f"Request failed for {url}: {last_error}")
