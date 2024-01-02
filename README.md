# HUSTSOCKS Client

### Requirement
- GUI(Terminal form) for Edit/Save Proxy Server information
- Support USERNAME/PASSWORD authentication with HUSTSOCKS Proxy Server
- Support register USERNAME/PASSWORD to HUSTSOCKS Proxy Server


### GUI Review

```
Welcome to HUSTSOCKS client
    1. Current configuration
    2. Register USERNAME/PASSWORD authentication
    0. Exit
```
`Current configuration` is saved in file `hustsocks.conf`. If none, show error.

`Change configuration` will rewrite proxy information in file `hustsocks.conf`

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