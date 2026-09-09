# Run the controller

If all previous steps have been followed the controller should now be fully
functional. To run it, ensure that the Python virtual environment has been
sourced, then:

```bash
source ~/.venv/bin/activate
cd <src>/pt/controller_3/src
python -m plant_controller run
```

The controller now monitors and waters the connected plant, and the web
interface is accessible on port 8099 of the Raspberry Pi.

If connected to the Raspberry Pi over LAN, this interface can be found by
typing `<CONTROLLER_IP>:8099` in a browser from another computer on the same
LAN, where `<CONTROLLER_IP>` is the IP of the Raspberry Pi.

If running the Raspberry Pi with a desktop environment and a connected screen
and keyboard, the web interface is available from within the Raspberry Pi by
typing `localhost:8099` in the Raspberry Pi's browser.

---

[**Next steps**](./qs_next_steps.md)