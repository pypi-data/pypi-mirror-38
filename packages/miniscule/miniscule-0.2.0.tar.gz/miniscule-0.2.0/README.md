# yaml-conf

Miniscule library for flexible YAML configuration files, inspired by
[Aero](https://github.com/juxt/aero).

## Example

Loading this configuration with `config.load` expands the `!or` and `!env` tags
in the expected way.

```yaml
server:
  host: !or [!env HOST, localhost]
  port: !or [!env PORT, 8000]
debug: !env DEBUG
database:
  name: my_database
  user: my_user
  password: !env DB_PASSWORD
```
