from typing import Any, List
from sqlalchemy.types import TypeDecorator, String
from sqlalchemy.dialects import postgresql
import json
import logging

logger = logging.getLogger(__name__)


class ListStringType(TypeDecorator):
    """
    Custom SQLAlchemy Type for storing lists as PostgreSQL arrays.
    Now supports newline-separated strings from TextAreaField.
    """

    impl = postgresql.ARRAY(String)

    def process_bind_param(self, value: Any, dialect: Any) -> List[str] | None:
        """
        Convert input to list for storage.
        Supports: list, JSON string, comma-separated string, newline-separated.
        """
        logger.debug(
            f"ListStringType.process_bind_param: {value!r}, type: {type(value)}"
        )

        if value is None:
            return None

        # Already a list
        if isinstance(value, list):
            result = [str(item).strip() for item in value if item]
            logger.debug(f"Processing as list: {result}")
            return result or None

        # String input
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return None

            logger.debug(f"Processing string: {value!r}")

            # 1. Try JSON first (from API)
            try:
                data = json.loads(value)
                if isinstance(data, list):
                    result = [str(item).strip() for item in data if item]
                    logger.debug(f"Parsed as JSON: {result}")
                    return result or None
            except json.JSONDecodeError:
                pass

            # 2. Check for newline-separated (from Admin TextAreaField)
            if "\n" in value:
                items = [line.strip() for line in value.split("\n") if line.strip()]
                result = [item for item in items if item]
                logger.debug(f"Parsed as newline-separated: {result}")
                return result or None

            # 3. Try comma-separated
            if "," in value:
                items = [item.strip() for item in value.split(",")]
                result = [item for item in items if item]
                logger.debug(f"Parsed as comma-separated: {result}")
                return result or None

            # 4. Single item
            item = value.strip()
            if item:
                logger.debug(f"Single item: {[item]}")
                return [item]

        logger.warning(f"Unhandled type: {type(value)}, value: {value!r}")
        return None

    def process_result_value(self, value: Any, dialect: Any) -> List[str]:
        """Return list from database."""
        if value is None:
            return []
        # PostgreSQL returns a list-like object
        return list(value) if value else []

    def copy(self, **kw: Any) -> "ListStringType":
        return ListStringType(**kw)
