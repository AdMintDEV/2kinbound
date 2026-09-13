(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  root.TUBECHECK_PACK = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  function paymentUrlOf(cfg) {
    return String((cfg && cfg.paymentUrl) || "").trim();
  }

  function queryGet(params, key) {
    if (!params) return "";
    if (typeof params.get === "function") return String(params.get(key) || "");
    return String(params[key] || "");
  }

  /**
   * Paid exclusive files may be shown only when this returns true.
   * Static Pages cannot verify payment. Empty paymentUrl is not unlock.
   * A published query-string token is not a paywall.
   */
  function isPackUnlocked(cfg, params) {
    if (!paymentUrlOf(cfg)) return false;
    void params;
    void (cfg && cfg.unlockToken);
    return false;
  }

  function packPageState(cfg, params) {
    if (isPackUnlocked(cfg, params)) return "unlocked";
    if (!paymentUrlOf(cfg)) return "unconfigured";
    if (queryGet(params, "paid") === "1") return "thanks";
    return "checkout";
  }

  function renderPackPage(doc, cfg, params) {
    const gate = doc.getElementById("gate");
    const detail = doc.getElementById("pack-detail");
    const cta = doc.getElementById("pack-cta");
    if (!gate || !detail || !cta) return packPageState(cfg, params);

    const state = packPageState(cfg, params);
    cta.replaceChildren();

    if (state === "unconfigured") {
      gate.textContent = "Checkout is not connected. The Team Pack is not a free download on this site.";
      detail.textContent = "The owner must attach the catalog to a Payhip product or a Stripe Payment Link. This page never hosts paid files.";
    } else if (state === "thanks") {
      gate.textContent = "Thanks for buying the 4130 Team Pack.";
      detail.textContent = "Your files come from the checkout provider (Payhip library, receipt email, or Stripe file attachment). This page does not host the catalog.";
    } else if (state === "checkout") {
      gate.textContent = "The $9 Team Pack is sold at checkout. This page does not include the catalog.";
      detail.textContent = "After payment, the merchant delivers the file. There is no download on GitHub Pages.";
      const link = doc.createElement("a");
      link.className = "primary";
      link.href = paymentUrlOf(cfg);
      link.textContent = "Pay $" + ((cfg && cfg.priceUsd) || 9) + " — checkout delivers the file";
      link.style.display = "inline-block";
      link.style.textDecoration = "none";
      link.style.padding = "10px 14px";
      cta.appendChild(link);
    } else {
      gate.textContent = "The Team Pack is not available as a download on this site.";
      detail.textContent = "Paid files are delivered by the merchant, not GitHub Pages.";
    }
    return state;
  }

  return { isPackUnlocked, packPageState, renderPackPage };
});
