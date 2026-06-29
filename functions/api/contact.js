/* Cloudflare Pages Function — POST /api/contact
 *
 * Receives an enquiry from the /get-a-quote/ and /contact-us/ forms (the .enquiry-form)
 * and emails BOTH the Wolves Removals team AND the customer a branded confirmation copy
 * via Resend. Separate from /api/calculator (estimate) and /api/careers (jobs).
 *
 * Accepts either a JSON body (the enquiry-form.js fetch) or a classic form POST
 * (application/x-www-form-urlencoded / multipart) so it works even without JavaScript.
 *
 * Required Pages environment variables:
 *   RESEND_API_KEY   - a Resend API key (https://resend.com)
 *   CONTACT_FROM     - verified sender, e.g. "Wolves Removals <enquiries@wolves-removals.co.uk>"
 *   CONTACT_TO       - where enquiries go, e.g. "contact@wolves-removals.co.uk"
 *
 * If CONTACT_FROM / CONTACT_TO aren't set, it falls back to the calculator's
 * QUOTE_FROM / QUOTE_TO — so if the estimate form already works, this one does too
 * with no extra config. Until something is set the form shows a friendly "call us"
 * message — it never breaks.
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
  return new Response(JSON.stringify(obj), {
    status: status || 200,
    headers: { "content-type": "application/json; charset=utf-8" }
  });
}
function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
  });
}
function validEmail(e) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(e || "")); }

// Trim env values — pasted secrets often pick up a trailing newline/space, which
// makes the Authorization header invalid and causes fetch() to throw a raw 502.
function clean(v) { return (v == null ? "" : String(v)).trim(); }
function apiKey(env) { return clean(env.RESEND_API_KEY); }
function fromAddr(env) { return clean(env.CONTACT_FROM) || clean(env.QUOTE_FROM); }
function toAddr(env) { return clean(env.CONTACT_TO) || clean(env.QUOTE_TO); }

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
    // header
    '<tr><td style="background:#ffffff;padding:22px 28px 18px;border-bottom:1px solid ' + BRAND.border + ';">' +
    '<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>' +
    '<td style="vertical-align:middle;padding-right:14px;"><img src="' + BRAND.logo + '" width="48" height="48" alt="Wolves Removals" style="display:block;border:0;width:48px;height:48px;"></td>' +
    '<td style="vertical-align:middle;"><div style="font-size:21px;font-weight:bold;color:' + BRAND.ink + ';line-height:1.1;">Wolves <span style="color:' + BRAND.orange + ';">Removals</span></div>' +
    '<div style="margin-top:4px;font-size:11px;color:' + BRAND.inkSoft + ';letter-spacing:0.4px;text-transform:uppercase;">' + BRAND.tagline + '</div></td>' +
    '</tr></table></td></tr>' +
    // orange divider
    '<tr><td style="height:4px;background:' + BRAND.orange + ';line-height:4px;font-size:0;">&nbsp;</td></tr>' +
    // body
    '<tr><td style="padding:24px 28px 8px;">' + inner + '</td></tr>' +
    // footer
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
function table(rows) {
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

  // Read JSON or classic form encoding.
  var a;
  try {
    var ct = (context.request.headers.get("content-type") || "");
    if (ct.indexOf("application/json") > -1) {
      a = await context.request.json();
    } else {
      var fd = await context.request.formData();
      a = {};
      for (var pair of fd.entries()) {
        if (pair[0] === "enquiry") { (a.enquiry = a.enquiry || []).push(pair[1]); }
        else a[pair[0]] = pair[1];
      }
    }
  } catch (e) { return json({ ok: false, error: "We couldn't read your enquiry — please try again." }, 400); }

  // Honeypot — a filled "company" field is a bot. Pretend success so it moves on.
  if (a.company) return json({ ok: true });

  var first = (a.first_name || a.name || "").toString().trim();
  if (!first) return json({ ok: false, error: "Please add your name." }, 400);
  if (!validEmail(a.email)) return json({ ok: false, error: "Please add a valid email address." }, 400);

  if (!apiKey(env) || !fromAddr(env) || !toAddr(env)) {
    return json({ ok: false, error: "Online enquiries aren't switched on yet — please call us on " + BRAND.phone + " and we'll be glad to help." }, 503);
  }
  var debug = false;
  try { debug = new URL(context.request.url).searchParams.get("debug") === "1"; } catch (e) {}

  var name = (esc(first) + " " + esc(a.last_name || "")).trim();
  var enquiry = Array.isArray(a.enquiry) ? a.enquiry.join(", ") : (a.enquiry || "");

  var details = table([
    ["Name", name],
    ["Email", a.email],
    ["Phone", a.phone],
    ["Moving from", a.from],
    ["Moving to", a.to],
    ["Preferred date", a.date],
    ["Property size", a.size],
    ["Help needed", enquiry],
    ["Message", a.message]
  ]);

  // ---- Team email ----
  var teamInner =
    p('<strong style="color:' + BRAND.ink + ';">New website enquiry</strong>', false) +
    p('A new enquiry was submitted via the website. Reply directly to this email to reach the customer.', true) +
    sectionH("Enquiry details") + details +
    p('<span style="font-size:12px;color:' + BRAND.inkSoft + ';">Sent from the enquiry form on wolves-removals.co.uk.</span>', true);
  var teamHtml = wrap("New enquiry: " + name, teamInner);

  var subjectBits = enquiry ? (" — " + enquiry) : "";
  var sentTeam = await sendEmail(env, toAddr(env), "New enquiry — " + name + subjectBits, teamHtml, a.email);
  if (!sentTeam.ok) {
    var err = { ok: false, error: "Sorry, we couldn't send your enquiry just now — please call us on " + BRAND.phone + "." };
    if (debug) { err.resendStatus = sentTeam.status; err.resendDetail = sentTeam.detail; err.from = fromAddr(env); err.to = toAddr(env); }
    return json(err, 502);
  }

  // ---- Customer confirmation ----
  var custInner =
    p('Hi ' + esc(first) + ',', false) +
    p('Thanks for getting in touch with <strong>Wolves Removals</strong>. We&rsquo;ve received your enquiry and a member of our friendly, family-run team will get back to you shortly &mdash; usually within a few hours during office hours.', false) +
    p('If your move is time-sensitive, feel free to call us on <a href="' + BRAND.phoneHref + '" style="color:' + BRAND.orange + ';text-decoration:none;">' + BRAND.phone + '</a> and we&rsquo;ll be glad to help straight away.', false) +
    sectionH("What you sent us") + details +
    p('Many thanks,<br>The Wolves Removals team', false);
  var custHtml = wrap("Thanks " + first + " — we've received your enquiry and will reply shortly.", custInner);

  try { await sendEmail(env, a.email, "We've received your enquiry — Wolves Removals", custHtml); } catch (e2) {}

  return json({ ok: true });

  } catch (err) {
    return json({ ok: false, error: "Sorry, we couldn't send your enquiry just now — please call us on " + BRAND.phone + ".", crash: String((err && err.message) || err) }, 500);
  }
}
