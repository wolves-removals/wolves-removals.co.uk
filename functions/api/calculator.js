/* Cloudflare Pages Function — POST /api/calculator
 *
 * Receives a Removals & Storage Calculator estimate from /removals-calculator/ and emails
 * BOTH the Wolves Removals team and the customer (a copy) via Resend. This is entirely
 * separate from the /get-a-quote/ contact form.
 *
 * Required Pages environment variables:
 *   RESEND_API_KEY   - a Resend API key (https://resend.com)
 *   QUOTE_FROM       - verified sender, e.g. "Wolves Removals <quotes@wolves-removals.co.uk>"
 *   QUOTE_TO         - where estimates go, e.g. "info@wolves-removals.co.uk"
 */

function json(obj, status) {
  return new Response(JSON.stringify(obj), { status: status || 200, headers: { "content-type": "application/json; charset=utf-8" } });
}
function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
}
function validEmail(e) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(e || "")); }

async function sendEmail(env, to, subject, html, replyTo) {
  var body = { from: env.QUOTE_FROM, to: [to], subject: subject, html: html };
  if (replyTo) body.reply_to = replyTo;
  var res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { "authorization": "Bearer " + env.RESEND_API_KEY, "content-type": "application/json" },
    body: JSON.stringify(body)
  });
  return res.ok;
}

export async function onRequestPost(context) {
  var env = context.env || {};

  var a;
  try { a = await context.request.json(); }
  catch (e) { return json({ ok: false, error: "We couldn't read your details — please try again." }, 400); }

  if (!a.name) return json({ ok: false, error: "Please add your name." }, 400);
  if (!validEmail(a.email)) return json({ ok: false, error: "Please add a valid email address." }, 400);

  if (!env.RESEND_API_KEY || !env.QUOTE_FROM || !env.QUOTE_TO) {
    return json({ ok: false, error: "Online quotes aren't switched on yet — please call us and we'll sort your estimate." }, 503);
  }

  var e = a.estimate || {};
  function row(k, v) {
    return (v || v === 0) ? '<tr><td style="padding:5px 10px;font-weight:bold;vertical-align:top;border-bottom:1px solid #eee">' + esc(k) +
      '</td><td style="padding:5px 10px;border-bottom:1px solid #eee">' + esc(v) + "</td></tr>" : "";
  }
  var removals = e.mode !== "storage", storage = e.mode !== "removals";
  var table = '<table style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:14px;max-width:560px">' +
    row("Estimate type", e.service) +
    row("Total volume", (e.cuft || 0) + " cu ft / " + (e.cum || 0) + " cu m" + (e.items ? " (" + e.items + " items)" : "")) +
    (removals ? (
      row("Recommended vehicle", e.vehicle ? (e.vehicle + (e.crew ? " · " + e.crew : "")) : "") +
      row("Round-trip distance", e.miles ? (e.miles + " miles") : "") +
      row("Route", e.route) +
      row("Volume cost", e.volumeCost) + row("Mileage", e.mileage) +
      row("Removals nett", e.removalsNett) + row("VAT (20%)", e.removalsVat)
    ) : "") +
    (storage ? (
      row("Storage pods", e.pods) + row("Days of storage", e.days) +
      row("Daily rate", e.dailyRate) + row("Storage subtotal (nett)", e.storageTotal)
    ) : "") +
    row("Grand estimate (+ VAT at booking)", e.grand) +
    row("Inventory", e.inventory) +
    row("Preferred date", a.date) +
    "</table>";

  var contact = '<table style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:14px;max-width:560px">' +
    row("Name", a.name) + row("Email", a.email) + row("Phone", a.phone) + "</table>";

  var teamHtml = '<div style="font-family:Arial,sans-serif;color:#262626"><h2>New calculator estimate &mdash; ' + esc(e.service || "") + "</h2>" +
    "<h3>Customer</h3>" + contact + "<h3>Their estimate</h3>" + table +
    '<p style="color:#777;font-size:12px">Sent from the Removals &amp; Storage Calculator on wolves-removals.co.uk. Estimate only &mdash; confirm with a survey.</p></div>';
  var custHtml = '<div style="font-family:Arial,sans-serif;color:#262626"><h2>Your moving estimate, ' + esc(a.name) + "</h2>" +
    "<p>Thanks for using our calculator. Here&rsquo;s the estimate you generated &mdash; it&rsquo;s a guide only " +
    "(+ VAT at booking), and we&rsquo;ll confirm an exact, fixed price with a free, no-obligation survey.</p>" + table +
    "<p>We&rsquo;ll be in touch shortly. Many thanks,<br>The Wolves Removals team</p></div>";

  var sentTeam = await sendEmail(env, env.QUOTE_TO, "Calculator estimate — " + a.name + " (" + (e.grand || "") + ")", teamHtml, a.email);
  if (!sentTeam) return json({ ok: false, error: "Sorry, we couldn't send your estimate just now — please call us." }, 502);

  try { await sendEmail(env, a.email, "Your Wolves Removals estimate", custHtml); } catch (e2) {}

  return json({ ok: true });
}
