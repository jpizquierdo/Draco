# Running Draco as a systemd Service

Copy the unit file and enable the service:

```shell
cp draco.service ~/.config/systemd/user/draco.service
systemctl --user enable draco.service
systemctl --user start draco.service
```

Check status with:

```shell
systemctl --user status draco.service
journalctl --user -u draco.service -f
```
