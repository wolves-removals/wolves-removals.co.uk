/* Cloudflare Pages Function — POST /api/careers
 *
 * Receives a job application from /job-vacancies/ and emails BOTH the Wolves Removals
 * team and the applicant a branded confirmation copy via Resend.
 *
 * Env vars (Settings -> Variables and secrets):
 *   RESEND_API_KEY   - a Resend API key (https://resend.com)
 *   CAREERS_FROM     - verified sender, e.g. "Wolves Removals Careers <careers@wolves-removals.co.uk>"
 *   CAREERS_TO       - where applications go, e.g. "contact@wolves-removals.co.uk"
 *
 * Falls back to CONTACT_FROM/CONTACT_TO (then QUOTE_FROM/QUOTE_TO) if the CAREERS_*
 * vars aren't set, so it works with the same config as the contact form. The sending
 * domain must be verified in Resend. Until something is set the form shows a friendly
 * "email your CV" message — it never breaks.
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
function fromAddr(env) { return clean(env.CAREERS_FROM) || clean(env.CONTACT_FROM) || clean(env.QUOTE_FROM); }
function toAddr(env) { return clean(env.CAREERS_TO) || clean(env.CONTACT_TO) || clean(env.QUOTE_TO); }

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
  try {
    var ct = context.request.headers.get("content-type") || "";
    if (ct.indexOf("application/json") > -1) {
      a = await context.request.json();
    } else {
      var fd = await context.request.formData();
      a = {};
      for (var pair of fd.entries()) {
        if (pair[0] === "licenceCats") { (a.licenceCats = a.licenceCats || []).push(pair[1]); }
        else a[pair[0]] = pair[1];
      }
    }
  } catch (e) { return json({ ok: false, error: "We couldn't read your application — please try again." }, 400); }

  if (a && a.company) return json({ ok: true });   // honeypot
  if (!a.firstName) return json({ ok: false, error: "Please add your name." }, 400);
  if (!validEmail(a.email)) return json({ ok: false, error: "Please add a valid email address." }, 400);

  if (!apiKey(env) || !fromAddr(env) || !toAddr(env)) {
    return json({ ok: false, error: "Applications aren't switched on online yet — please email your CV to " + BRAND.email + " and we'll be in touch." }, 503);
  }

  var name = (esc(a.firstName) + " " + esc(a.lastName || "")).trim();
  var cats = Array.isArray(a.licenceCats) ? a.licenceCats.join(", ") : (a.licenceCats || "");

  var details = kvTable([
    ["Name", name],
    ["Email", a.email],
    ["Phone", a.phone],
    ["Town / city", a.town],
    ["Postcode", a.postcode],
    ["Right to work", a.rightToWork],
    ["Position", a.position],
    ["Availability", a.availability],
    ["Earliest start", a.startDate],
    ["Driving licence", a.licence],
    ["Years driving", a.yearsDriving],
    ["Licence categories", cats],
    ["Years in removals", a.yearsRemovals],
    ["Previous experience", a.experience],
    ["Why this role", a.whyRole]
  ]);

  // ---- Team email ----
  var teamInner =
    p('<strong style="color:' + BRAND.ink + ';">New job application</strong>', false) +
    p('A new application was submitted via the careers page. Reply directly to this email to reach the applicant.', true) +
    sectionH("Applicant") + details +
    p('<span style="font-size:12px;color:' + BRAND.inkSoft + ';">Sent from the wolves-removals.co.uk careers page.</span>', true);
  var teamHtml = wrap("New job application: " + name, teamInner);

  var sentTeam = await sendEmail(env, toAddr(env), "New job application — " + name + (a.position ? (" (" + a.position + ")") : ""), teamHtml, a.email);
  if (!sentTeam.ok) {
    try { console.error("careers: Resend send failed", sentTeam.status, sentTeam.detail); } catch (er) {}
    return json({ ok: false, error: "Sorry, we couldn't send your application just now — please email your CV to " + BRAND.email + "." }, 502);
  }

  // ---- Applicant confirmation (best-effort) ----
  var custInner =
    p('Hi ' + esc(a.firstName) + ',', false) +
    p('Thanks for your application to join <strong>Wolves Removals</strong>. We&rsquo;ve received it and will review it within five working days. If your experience is a fit, we&rsquo;ll be in touch to arrange a chat.', false) +
    sectionH("Your application") + details +
    p('Many thanks,<br>The Wolves Removals team', false);
  var custHtml = wrap("Thanks " + a.firstName + " — we've received your application.", custInner);

  try { await sendEmail(env, a.email, "Your Wolves Removals job application", custHtml); } catch (e) {}

  return json({ ok: true });

  } catch (err) {
    return json({ ok: false, error: "Sorry, we couldn't send your application just now — please email your CV to " + BRAND.email + ".", crash: String((err && err.message) || err) }, 500);
  }
}
