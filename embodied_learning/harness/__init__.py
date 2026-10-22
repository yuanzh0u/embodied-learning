"""AI-model invocation harness.

Anything that needs model capability goes through this package's interface —
the rest of the codebase stays mechanical and deterministic (pybind-style:
the binding layer owns the foreign runtime, callers never touch it directly).
Currently one binding: :mod:`embodied_learning.harness.claude` (the ``claude``
CLI). Adding another backend means adding a sibling module here, not touching
callers.
"""
