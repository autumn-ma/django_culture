from typing import Any, Optional

import hashlib
import random

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone

from core.models import (
    FeatureFlag,
    FeatureFlagAuditLog,
    FeatureFlagUserOverride,
)

User = get_user_model()


class FeatureFlagService:
    """Service class for feature flag operations"""

    def __init__(self):
        self.cache_timeout = 300  # 5 minutes

    def is_enabled(
        self,
        flag_name: str,
        user: User | None = None,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """Check if a feature flag is enabled for a user"""

        # Check cache first
        cache_key = (
            f"feature_flag:{flag_name}:{user.id if user else 'anonymous'}"
        )
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        try:
            flag = FeatureFlag.objects.get(name=flag_name)
        except FeatureFlag.DoesNotExist:
            return False

        if not flag.is_active:
            cache.set(cache_key, False, self.cache_timeout)
            return False

        # Check user override first
        if user:
            override = FeatureFlagUserOverride.objects.filter(
                feature_flag=flag, user=user
            ).first()
            if override:
                result = override.is_enabled
                cache.set(cache_key, result, self.cache_timeout)
                self._log_flag_check(flag, user, result, "override")
                return result

        # Apply rollout strategy
        result = self._apply_rollout_strategy(flag, user, context)
        cache.set(cache_key, result, self.cache_timeout)
        self._log_flag_check(flag, user, result, "rollout")
        return result

    def _apply_rollout_strategy(
        self,
        flag: FeatureFlag,
        user: User | None,
        context: dict[str, Any] | None,
    ) -> bool:
        """Apply the rollout strategy for the flag"""

        if flag.rollout_strategy == "all":
            return True

        elif flag.rollout_strategy == "percentage":
            if not user:
                return False
            # Use consistent hashing for stable rollout
            user_hash = int(
                hashlib.md5(f"{flag.name}:{user.id}".encode()).hexdigest(), 16
            )
            return (user_hash % 100) < flag.rollout_percentage

        elif flag.rollout_strategy == "user_list":
            if not user:
                return False
            allowed_users = flag.rollout_config.get("user_ids", [])
            return user.id in allowed_users

        elif flag.rollout_strategy == "user_attributes":
            if not user:
                return False
            return self._check_user_attributes(flag, user)

        elif flag.rollout_strategy == "gradual":
            return self._apply_gradual_rollout(flag, user)

        return False

    def _check_user_attributes(self, flag: FeatureFlag, user: User) -> bool:
        """Check if user matches attribute conditions"""
        conditions = flag.rollout_config.get("conditions", [])

        for condition in conditions:
            attr_name = condition.get("attribute")
            operator = condition.get("operator")
            value = condition.get("value")

            if not all([attr_name, operator, value]):
                continue

            user_value = getattr(user, attr_name, None)

            if (
                operator == "eq"
                and user_value == value
                or operator == "in"
                and user_value in value
                or (
                    operator == "contains"
                    and isinstance(user_value, str)
                    and value in user_value
                )
            ):
                return True

        return False

    def _apply_gradual_rollout(
        self, flag: FeatureFlag, user: User | None
    ) -> bool:
        """Apply gradual rollout based on time and configuration"""
        config = flag.rollout_config
        start_time = config.get("start_time")
        end_time = config.get("end_time")
        start_percentage = config.get("start_percentage", 0)
        end_percentage = config.get("end_percentage", 100)

        if not start_time or not end_time:
            return False

        now = timezone.now()
        start_dt = timezone.datetime.fromisoformat(start_time)
        end_dt = timezone.datetime.fromisoformat(end_time)

        if now < start_dt:
            return False
        elif now > end_dt:
            current_percentage = end_percentage
        else:
            # Calculate current percentage based on time progression
            total_duration = (end_dt - start_dt).total_seconds()
            elapsed_duration = (now - start_dt).total_seconds()
            progress = elapsed_duration / total_duration

            current_percentage = start_percentage + (
                (end_percentage - start_percentage) * progress
            )

        # Apply percentage rollout
        if not user:
            return False

        user_hash = int(
            hashlib.md5(f"{flag.name}:{user.id}".encode()).hexdigest(), 16
        )
        return (user_hash % 100) < current_percentage

    def _log_flag_check(
        self,
        flag: FeatureFlag,
        user: User | None,
        result: bool,
        strategy: str,
    ):
        """Log flag check for audit purposes"""
        action_mapping = {
            "override": "checked_override",
            "rollout": "checked_rollout",
            "default": "checked_default",
        }

        FeatureFlagAuditLog.objects.create(
            feature_flag=flag,
            user=user,
            action=action_mapping.get(strategy, "checked_default"),
            new_value={"result": result, "strategy": strategy},
        )

    def invalidate_cache(self, flag_name: str, user_id: int | None = None):
        """Invalidate cache for a specific flag"""
        if user_id:
            cache_key = f"feature_flag:{flag_name}:{user_id}"
            cache.delete(cache_key)
        else:
            # Clear all cache entries for this flag
            cache.delete_many([f"feature_flag:{flag_name}:*"])
