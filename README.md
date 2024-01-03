# FUXLOGSOCKS Client

### Requirement
- GUI(Terminal form) for Edit/Save Proxy Server information
- Support USERNAME/PASSWORD authentication with FUXLOGSOCKS Proxy Server
- Support register USERNAME/PASSWORD to FUXLOGSOCKS Proxy Server


### GUI Review

```
Welcome to FUXLOGSOCKS client
    1. Current configuration
    2. Register USERNAME/PASSWORD authentication
    0. Exit
```
`Current configuration` is saved in file `proxy.config`. If none, show error.

`Change configuration` will rewrite proxy information in file `proxy.config`

For user input display
```
[USER] > _
```

Current configuration display
```
Current configuration (enter 0 to back)
    Host: None
    Port: None
    Username: None
    Password: None
```

Change configuration need to verify all field which user typed in.
```
Register USERNAME/PASSWORD authentication information
Username (At least 8 characters): (USER WILL TYPE INPUT HERE)
Password (At least 8 characters): (USER WILL TYPE INPUT HERE)
```
