# Varla-Backup Service


## config.yaml

```yaml
backups:
    - PREFIX: <BackupName>
      destination_dir: <DestinationDir>
      zip_compression: <bool>
      keep_window: <int>

      source_directories:
          - <SourceDir>
          - <SourceDir>
            ...

      database_names:
          - <DatabaseName>
          - <DatabaseName>
            ...

      remote_backups:
          - host: <RemoteHost>
            path: <RemotePath>
          - host: <RemoteHost>
            path: <RemotePath>
            ...
```

## Zip Compression
Zip requires `zip` package to be installed at the server.
```
apt install zip
```

## Database Backups
Database servers require Varla to run as root, so `mysql` do not ask for password.

## Remote Backups
RemoteHosts need to have key access configured already with no password.

