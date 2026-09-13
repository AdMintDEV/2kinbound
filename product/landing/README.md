# Inbound Score landing (AC#1)

Static public page. No Stripe. No answer-engine API calls.

## Run

```bash
python product/landing/serve.py
```

- Home: http://127.0.0.1:8765/
- Free audit stub: http://127.0.0.1:8765/audit

`--port` / `--host` override the bind address.

Open `index.html` as a file only if you do not need `/audit` and `/styles.css` paths; the server is the supported way to run it.
