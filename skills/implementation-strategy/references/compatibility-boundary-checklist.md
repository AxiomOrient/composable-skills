# Compatibility boundary checklist

Treat these as compatibility-sensitive when they were released or explicitly promised stable:
- public APIs and documented behavior
- CLI flags and configuration keys
- environment variables and config file schema
- serialized or persisted state
- wire protocols and integration payloads
- migrations, rollback paths, and durable external data

Treat these as directly rewritable by default:
- branch-local interfaces
- internal helpers
- same-branch tests and fixtures
- private examples that are not a released contract
