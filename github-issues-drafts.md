# GitHub Issue Drafts for OpenClaw

## Issue 1: Configurable Permissions-Policy header

**Repo:** https://github.com/openclaw/openclaw/issues/new
**Title:** `Feature: Configurable Permissions-Policy header for Control UI (microphone/camera access)`

The Control UI serves a hardcoded `Permissions-Policy: camera=(), microphone=(), geolocation=()` header, which denies microphone access at the HTTP level. This prevents the webchat voice input feature from working, regardless of browser permission settings.

Users accessing the Control UI through a reverse proxy or external domain (e.g., Cloudflare → Fly Machine) see "Microphone access denied" even when the browser is explicitly set to Allow. There is no config option to override this — `gateway.http.securityHeaders` currently only exposes `strictTransportSecurity`.

**Proposed fix:** Add a `permissionsPolicy` field to `gateway.http.securityHeaders`:

```json
{
  "gateway": {
    "http": {
      "securityHeaders": {
        "permissionsPolicy": "microphone=(self), camera=(self)"
      }
    }
  }
}
```

This would allow any deployment (especially behind reverse proxies where header overrides aren't possible) to enable mic/camera access in the Control UI.

---

## Issue 2: Control UI webchat file attachments silently fail

**Repo:** https://github.com/openclaw/openclaw/issues/new
**Title:** `Bug: Control UI webchat file attachments show thumbnail but never deliver to agent`

The Control UI webchat provides a paperclip attachment button and shows a thumbnail preview after selecting a file/image, giving the user confidence the attachment was sent. However, the attachment never arrives in the agent session — it silently fails with no error message.

Both drag-and-drop and the file picker exhibit the same behavior: thumbnail appears on the client side, but no attachment reaches the agent.

**Expected:** File/image attachments sent via the Control UI webchat should be delivered to the agent session. If an upload fails, the user should see an error message.
