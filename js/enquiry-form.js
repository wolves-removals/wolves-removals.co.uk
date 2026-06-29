/* Enquiry form handler — progressive enhancement for the .enquiry-form on
 * /get-a-quote/ and /contact-us/ (and any page that embeds one).
 *
 * Intercepts the submit, POSTs the fields as JSON to the form's action
 * (/api/contact), and shows an inline status message — so the visitor stays on
 * the page. With JS disabled the form still does a normal POST to /api/contact,
 * which the Cloudflare Pages Function also accepts.
 */
(function () {
  "use strict";
  var forms = document.querySelectorAll("form.enquiry-form");
  if (!forms.length) return;

  Array.prototype.forEach.call(forms, function (form) {
    // A status line lives just after the submit button (created once).
    var msg = form.querySelector(".enquiry-msg");
    if (!msg) {
      msg = document.createElement("p");
      msg.className = "enquiry-msg";
      msg.setAttribute("aria-live", "polite");
      msg.style.cssText = "margin:0.85rem 0 0;font-size:0.9rem;font-weight:600;text-align:center;";
      var btn = form.querySelector('button[type="submit"]');
      if (btn && btn.parentNode) btn.parentNode.appendChild(msg);
      else form.appendChild(msg);
    }

    function setMsg(text, ok) {
      msg.textContent = text;
      msg.style.color = ok === true ? "#047857" : ok === false ? "#b91c1c" : "#697783";
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.company && form.company.value) return;            // honeypot — silently ignore bots
      if (!form.checkValidity()) { form.reportValidity(); return; }

      var fd = new FormData(form);
      var payload = {};
      fd.forEach(function (value, key) {
        if (key === "company") return;                           // never send the honeypot
        if (key === "enquiry") { (payload.enquiry = payload.enquiry || []).push(value); }
        else payload[key] = value;
      });

      var btn = form.querySelector('button[type="submit"]');
      if (btn) btn.disabled = true;
      setMsg("Sending your enquiry…", null);

      fetch(form.getAttribute("action") || "/api/contact", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(function (r) {
          return r.json().then(function (d) { return { ok: r.ok, d: d }; })
            .catch(function () { return { ok: r.ok, d: {} }; });
        })
        .then(function (res) {
          if (res.ok && res.d && res.d.ok) {
            form.reset();
            setMsg("Thank you! Your enquiry is on its way — we’ll be in touch shortly. A confirmation is on its way to your inbox too.", true);
          } else {
            setMsg((res.d && res.d.error) || "Sorry, we couldn’t send your enquiry just now — please call us instead.", false);
            if (btn) btn.disabled = false;
          }
        })
        .catch(function () {
          setMsg("Sorry, we couldn’t send your enquiry just now — please call us instead.", false);
          if (btn) btn.disabled = false;
        });
    });
  });
})();
