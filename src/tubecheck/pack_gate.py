"""Fail-closed Team Pack access for static GitHub Pages.

Pages cannot verify Stripe or Payhip payment. Paid exclusive files must
not live in the publish root, and this gate must never treat an empty
paymentUrl or a published query-string token as unlock.
"""

from __future__ import annotations

from typing import Any, Mapping


def is_pack_unlocked(
    cfg: Mapping[str, Any] | None = None,
    params: Mapping[str, Any] | None = None,
) -> bool:
    """Return True only if paid exclusive files may be shown or linked.

    Always False here: empty paymentUrl is not unlock, and ``?k=`` / ``?paid=1``
    are not a paywall. Delivery is the merchant file attachment, not this site.
    """
    cfg = cfg or {}
    payment_url = str(cfg.get("paymentUrl") or "").strip()
    if not payment_url:
        return False
    # Query tokens and success flags are client-visible; they do not prove payment.
    _ = params
    _ = cfg.get("unlockToken")
    return False


def pack_page_state(
    cfg: Mapping[str, Any] | None = None,
    params: Mapping[str, Any] | None = None,
) -> str:
    """Landing-page state. Never implies the catalog is on this site.

    ``unconfigured`` — no merchant URL.
    ``checkout`` — send the visitor to the merchant.
    ``thanks`` — post-pay thank-you only (still no files).
    ``unlocked`` — reserved; this implementation never returns it.
    """
    if is_pack_unlocked(cfg, params):
        return "unlocked"
    cfg = cfg or {}
    params = params or {}
    payment_url = str(cfg.get("paymentUrl") or "").strip()
    if not payment_url:
        return "unconfigured"
    if str(params.get("paid") or "") == "1":
        return "thanks"
    return "checkout"
