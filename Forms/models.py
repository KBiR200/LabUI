from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from main.models import Machine, Laberatory

# Create your models here.
class MachineRecordParameter(models.Model):
    """

    Example `parameters` value:
        {
            "oil_pressure_bar": int,
            "oil_temp_c": str,
            "leak_check": bool
        }
    """

    machine      = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="machine",
    )


    # flexible container for all key-value pairs
    parameters   = models.JSONField(default=dict, blank=True)


    def __str__(self):
        return f"{self.machine} @ {self.captured_at:%Y-%m-%d %H:%M}"

    # ────────────────────────────────────────────────────────────────
    # Convenience helpers
    # ────────────────────────────────────────────────────────────────
    def get_param(self, key, default=None):
        """Helper to fetch a parameter safely."""
        return self.parameters.get(key, default)

    def set_param(self, key, value):
        """Update one parameter in memory (call save() afterwards)."""
        self.parameters[key] = value


class LaberatoryFormsParameter(models.Model):
    Lab      = models.ForeignKey(
        Laberatory,
        on_delete=models.CASCADE,
        related_name="machine",
    )


    # flexible container for all key-value pairs
    parameters   = models.JSONField(default=dict, blank=True)


    def __str__(self):
        return f"{self.machine} @ {self.captured_at:%Y-%m-%d %H:%M}"

    # ────────────────────────────────────────────────────────────────
    # Convenience helpers
    # ────────────────────────────────────────────────────────────────
    def get_param(self, key, default=None):
        """Helper to fetch a parameter safely."""
        return self.parameters.get(key, default)

    def set_param(self, key, value):
        """Update one parameter in memory (call save() afterwards)."""
        self.parameters[key] = value