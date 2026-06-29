/* Cloudflare Pages Function — POST /api/calculator
 *
 * Receives a Removals & Storage Calculator estimate from /removals-calculator/ and emails
 * BOTH the Wolves Removals team and the customer a branded copy via Resend. Separate from
 * the /api/contact enquiry form.
 *
 * Env vars (Settings -> Variables and secrets):
 *   RESEND_API_KEY   - a Resend API key (https://resend.com)
 *   QUOTE_FROM       - verified sender, e.g. "Wolves Removals <quotes@wolves-removals.co.uk>"
 *   QUOTE_TO         - where estimates go, e.g. "contact@wolves-removals.co.uk"
 *
 * Falls back to CONTACT_FROM/CONTACT_TO if the QUOTE_* vars aren't set, so it works with
 * the same config as the contact form. The sending domain must be verified in Resend.
 */

var BRAND = {
  name: "Wolves Removals",
  tagline: "Professional Home &amp; Office Removals in Sussex",
  url: "https://wolves-removals.co.uk",
  logo: "https://wolves-removals.co.uk/wolves-removals-logo.png",
  phone: "01903 893731",
  phoneHref: "tel:+441903893731",
  email: "contact@wolves-removals.co.uk",
  address: "Doryln House, London Road, Ashington, Pulborough, West Sussex, RH20 3JT",
  hours: "Mon–Fri 08:00–18:00 · Sat 09:00–13:00",
  legal: "Wolves Removals Limited",
  founded: "2016",
  ink: "#262626", inkSoft: "#697783", orange: "#FC9700", green: "#02be7c",
  surface: "#F9F8F6", border: "#E7E7E7", page: "#E8E6DA"
};

function json(obj, status) {
  return new Response(JSON.stringify(obj), { status: status || 200, headers: { "content-type": "application/json; charset=utf-8" } });
}
function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
}
function validEmail(e) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(e || "")); }

function clean(v) { return (v == null ? "" : String(v)).trim(); }
function apiKey(env) { return clean(env.RESEND_API_KEY); }
function fromAddr(env) { return clean(env.QUOTE_FROM) || clean(env.CONTACT_FROM); }
function toAddr(env) { return clean(env.QUOTE_TO) || clean(env.CONTACT_TO); }

async function sendEmail(env, to, subject, html, replyTo) {
  var body = { from: fromAddr(env), to: [to], subject: subject, html: html };
  if (replyTo) body.reply_to = replyTo;
  try {
    var res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { "authorization": "Bearer " + apiKey(env), "content-type": "application/json" },
      body: JSON.stringify(body)
    });
    if (res.ok) return { ok: true };
    var detail = "";
    try { detail = await res.text(); } catch (e) {}
    return { ok: false, status: res.status, detail: detail.slice(0, 300) };
  } catch (e) {
    return { ok: false, status: 0, detail: "fetch threw: " + (e && e.message ? e.message : String(e)) };
  }
}

// Branded HTML shell — white card, logo header, orange divider, contact footer.
function wrap(preheader, inner) {
  return '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width,initial-scale=1"><title>' + BRAND.name + '</title></head>' +
    '<body style="margin:0;padding:0;background:' + BRAND.page + ';font-family:Arial,Helvetica,sans-serif;">' +
    '<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;visibility:hidden;opacity:0;color:transparent;height:0;width:0;font-size:1px;line-height:1px;">' + esc(preheader) + '</div>' +
    '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:' + BRAND.page + ';"><tr><td align="center" style="padding:24px 12px;">' +
    '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="width:100%;max-width:600px;background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 6px 24px rgba(38,38,38,0.08);">' +
    '<tr><td style="background:#ffffff;padding:22px 28px 18px;border-bottom:1px solid ' + BRAND.border + ';">' +
    '<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>' +
    '<td style="vertical-align:middle;padding-right:14px;"><img src="' + BRAND.logo + '" width="48" height="48" alt="Wolves Removals" style="display:block;border:0;width:48px;height:48px;"></td>' +
    '<td style="vertical-align:middle;"><div style="font-size:21px;font-weight:bold;color:' + BRAND.ink + ';line-height:1.1;">Wolves <span style="color:' + BRAND.orange + ';">Removals</span></div>' +
    '<div style="margin-top:4px;font-size:11px;color:' + BRAND.inkSoft + ';letter-spacing:0.4px;text-transform:uppercase;">' + BRAND.tagline + '</div></td>' +
    '</tr></table></td></tr>' +
    '<tr><td style="height:4px;background:' + BRAND.orange + ';line-height:4px;font-size:0;">&nbsp;</td></tr>' +
    '<tr><td style="padding:24px 28px 8px;">' + inner + '</td></tr>' +
    '<tr><td style="padding:20px 28px 24px;background:' + BRAND.surface + ';border-top:1px solid ' + BRAND.border + ';">' +
    '<div style="font-size:12px;color:' + BRAND.inkSoft + ';line-height:1.55;">' +
    '<strong style="color:' + BRAND.ink + ';font-size:13px;">' + BRAND.name + '</strong><br>' + BRAND.address + '<br>' +
    '<a href="' + BRAND.phoneHref + '" style="color:' + BRAND.orange + ';text-decoration:none;">' + BRAND.phone + '</a> · ' +
    '<a href="mailto:' + BRAND.email + '" style="color:' + BRAND.orange + ';text-decoration:none;">' + BRAND.email + '</a> · ' +
    '<a href="' + BRAND.url + '" style="color:' + BRAND.orange + ';text-decoration:none;">wolves-removals.co.uk</a><br>' + BRAND.hours +
    '<div style="margin-top:10px;font-size:11px;color:#9aa3ab;">' + BRAND.legal + ' · Keeping promises since ' + BRAND.founded + '.</div>' +
    '</div></td></tr>' +
    '</table></td></tr></table></body></html>';
}

function sectionH(label) {
  return '<h3 style="margin:22px 0 8px;font-size:15px;color:' + BRAND.ink + ';font-weight:bold;border-bottom:2px solid ' + BRAND.orange + ';padding-bottom:6px;">' + esc(label) + '</h3>';
}
function p(html, soft) {
  return '<p style="margin:0 0 12px;font-size:14px;color:' + (soft ? BRAND.inkSoft : BRAND.ink) + ';line-height:1.55;">' + html + '</p>';
}
function kvTable(rows) {
  var body = rows.map(function (r) {
    if (!r[1] && r[1] !== 0) return "";
    return '<tr><td style="padding:7px 12px;font-weight:bold;vertical-align:top;border-bottom:1px solid ' + BRAND.border + ';font-size:13px;color:' + BRAND.inkSoft + ';white-space:nowrap;">' + esc(r[0]) +
      '</td><td style="padding:7px 12px;border-bottom:1px solid ' + BRAND.border + ';font-size:14px;color:' + BRAND.ink + ';line-height:1.5;">' + esc(r[1]).replace(/\n/g, "<br>") + "</td></tr>";
  }).join("");
  return '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:collapse;width:100%;">' + body + "</table>";
}

export async function onRequestPost(context) {
  var env = context.env || {};
  try {

  var a;
  try { a = await context.request.json(); }
  catch (e) { return json({ ok: false, error: "We couldn't read your details — please try again." }, 400); }

  if (a && a.company) return json({ ok: true });   // honeypot
  if (!a.name) return json({ ok: false, error: "Please add your name." }, 400);
  if (!validEmail(a.email)) return json({ ok: false, error: "Please add a valid email address." }, 400);

  if (!apiKey(env) || !fromAddr(env) || !toAddr(env)) {
    return json({ ok: false, error: "Online quotes aren't switched on yet — please call us on " + BRAND.phone + " and we'll sort your estimate." }, 503);
  }

  var e = a.estimate || {};
  var removals = e.mode !== "storage", storage = e.mode !== "removals";

  var estRows = [
    ["Estimate type", e.service],
    ["Total volume", (e.cuft || e.cum) ? ((e.cuft || 0) + " cu ft / " + (e.cum || 0) + " cu m" + (e.items ? " (" + e.items + " items)" : "")) : ""]
  ];
  if (removals) estRows = estRows.concat([
    ["Recommended vehicle", e.vehicle ? (e.vehicle + (e.crew ? " · " + e.crew : "")) : ""],
    ["Round-trip distance", e.miles ? (e.miles + " miles") : ""],
    ["Route", e.route],
    ["Volume cost", e.volumeCost],
    ["Mileage", e.mileage],
    ["Removals nett", e.removalsNett],
    ["VAT (20%)", e.removalsVat]
  ]);
  if (storage) estRows = estRows.concat([
    ["Storage pods", e.pods],
    ["Days of storage", e.days],
    ["Daily rate", e.dailyRate],
    ["Storage subtotal (nett)", e.storageTotal]
  ]);
  estRows = estRows.concat([
    ["Grand estimate (+ VAT at booking)", e.grand],
    ["Inventory", e.inventory],
    ["Preferred date", a.date]
  ]);
  var estTable = kvTable(estRows);
  var contact = kvTable([["Name", a.name], ["Email", a.email], ["Phone", a.phone]]);

  // ---- Team email ----
  var teamInner =
    p('<strong style="color:' + BRAND.ink + ';">New calculator estimate</strong>' + (e.service ? (" &mdash; " + esc(e.service)) : ""), false) +
    p('Generated via the Removals &amp; Storage Calculator. Reply directly to this email to reach the customer.', true) +
    sectionH("Customer") + contact +
    sectionH("Their estimate") + estTable +
    p('<span style="font-size:12px;color:' + BRAND.inkSoft + ';">Estimate only &mdash; confirm with a survey.</span>', true);
  var teamHtml = wrap("New calculator estimate: " + a.name, teamInner);

  var sentTeam = await sendEmail(env, toAddr(env), "Calculator estimate — " + a.name + (e.grand ? (" (" + e.grand + ")") : ""), teamHtml, a.email);
  if (!sentTeam.ok) {
    try { console.error("calculator: Resend send failed", sentTeam.status, sentTeam.detail); } catch (er) {}
    return json({ ok: false, error: "Sorry, we couldn't send your estimate just now — please call us on " + BRAND.phone + "." }, 502);
  }

  // ---- Customer confirmation (best-effort) ----
  var custInner =
    p('Hi ' + esc(a.name) + ',', false) +
    p('Thanks for using our calculator. Here&rsquo;s the estimate you generated &mdash; it&rsquo;s a guide only (+ VAT at booking), and we&rsquo;ll confirm an exact, fixed price with a free, no-obligation survey.', false) +
    sectionH("Your estimate") + estTable +
    p('We&rsquo;ll be in touch shortly. If your move is time-sensitive, call us on <a href="' + BRAND.phoneHref + '" style="color:' + BRAND.orange + ';text-decoration:none;">' + BRAND.phone + '</a>.', false) +
    p('Many thanks,<br>The Wolves Removals team', false);
  var custHtml = wrap("Your moving estimate from Wolves Removals", custInner);

  try { await sendEmail(env, a.email, "Your Wolves Removals estimate", custHtml); } catch (e2) {}

  return json({ ok: true });

  } catch (err) {
    return json({ ok: false, error: "Sorry, we couldn't send your estimate just now — please call us on " + BRAND.phone + ".", crash: String((err && err.message) || err) }, 500);
  }
}
