/* Cloudflare Pages Function — POST /api/boxshop
 *
 * Receives a box-shop order (JSON) from /box-shop/, then emails BOTH the Wolves
 * Removals team and the customer (a confirmation copy) via Resend.
 *
 * Required Pages environment variables (Settings -> Environment variables):
 *   RESEND_API_KEY   - a Resend API key (https://resend.com)
 *   BOXSHOP_FROM     - verified sender, e.g. "Wolves Removals Box Shop <boxshop@wolves-removals.co.uk>"
 *   BOXSHOP_TO       - where orders go, e.g. "info@wolves-removals.co.uk"
 *
 * The sending domain must be verified in Resend. Until the vars are set the form
 * shows a friendly "please call us" message — the page never breaks.
 */

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

function money(n) { return "£" + (Number(n) || 0).toFixed(2); }

function validEmail(e) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(e || "")); }

async function sendEmail(env, to, subject, html, replyTo) {
  var body = { from: env.BOXSHOP_FROM, to: [to], subject: subject, html: html };
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

  // Parse the order (accept JSON or form-encoded).
  var order;
  try {
    var ct = context.request.headers.get("content-type") || "";
    if (ct.indexOf("application/json") > -1) {
      order = await context.request.json();
    } else {
      var fd = await context.request.formData();
      order = Object.fromEntries(fd.entries());
      if (typeof order.items === "string") { try { order.items = JSON.parse(order.items); } catch (e) { order.items = []; } }
    }
  } catch (e) { return json({ ok: false, error: "We couldn't read your order — please try again." }, 400); }

  var items = Array.isArray(order && order.items) ? order.items : [];
  if (!items.length) return json({ ok: false, error: "Please select at least one item." }, 400);
  if (!order.name) return json({ ok: false, error: "Please add your name." }, 400);
  if (!validEmail(order.email)) return json({ ok: false, error: "Please add a valid email address." }, 400);

  if (!env.RESEND_API_KEY || !env.BOXSHOP_FROM || !env.BOXSHOP_TO) {
    return json({ ok: false, error: "Online ordering isn't switched on yet — please call us to place your order and we'll sort it right away." }, 503);
  }

  // Build the order table (recompute the total server-side; never trust the client).
  var rows = "", total = 0;
  for (var i = 0; i < items.length; i++) {
    var it = items[i];
    var qty = Math.max(0, parseInt(it.qty, 10) || 0);
    var price = Number(it.price) || 0;
    if (qty <= 0) continue;
    var line = qty * price;
    total += line;
    rows += '<tr><td style="padding:6px 10px;border-bottom:1px solid #eee">' + esc(qty) + " &times; " + esc(it.name) +
      '</td><td style="padding:6px 10px;border-bottom:1px solid #eee;text-align:right;white-space:nowrap">' + money(line) + "</td></tr>";
  }
  if (!rows) return json({ ok: false, error: "Please select at least one item." }, 400);

  var customer =
    "<p><strong>Name:</strong> " + esc(order.name) + "<br>" +
    "<strong>Email:</strong> " + esc(order.email) + "<br>" +
    "<strong>Phone:</strong> " + esc(order.phone || "—") + "<br>" +
    "<strong>Preference:</strong> " + esc(order.fulfilment || "—") +
    (order.address ? "<br><strong>Address:</strong> " + esc(order.address) : "") +
    (order.notes ? "<br><strong>Notes:</strong> " + esc(order.notes) : "") + "</p>";

  var table =
    '<table style="border-collapse:collapse;width:100%;max-width:480px;font-family:Arial,sans-serif;font-size:15px">' +
    rows +
    '<tr><td style="padding:8px 10px;font-weight:bold">Estimated total</td>' +
    '<td style="padding:8px 10px;text-align:right;font-weight:bold">' + money(total) + "</td></tr></table>";

  var teamHtml =
    '<div style="font-family:Arial,sans-serif;color:#262626">' +
    "<h2>New Box Shop order</h2>" + customer +
    "<h3>Items</h3>" + table +
    '<p style="color:#777;font-size:13px">Sent from the wolves-removals.co.uk box shop. Total is an estimate; confirm stock, payment and delivery with the customer.</p></div>';

  var customerHtml =
    '<div style="font-family:Arial,sans-serif;color:#262626">' +
    "<h2>Thanks for your order, " + esc(order.name) + "!</h2>" +
    "<p>We&rsquo;ve received your packing-materials order and will be in touch shortly to confirm availability, payment and " +
    esc((order.fulfilment || "collection or delivery")).toLowerCase() + ".</p>" +
    "<h3>Your order</h3>" + table +
    "<p>If anything&rsquo;s not right, just reply to this email or call us on " +
    '<a href="tel:01903893731">01903 893731</a>.</p>' +
    "<p>Many thanks,<br>The Wolves Removals team</p></div>";

  var sentTeam = await sendEmail(env, env.BOXSHOP_TO, "New Box Shop order — " + esc(order.name), teamHtml, order.email);
  if (!sentTeam) return json({ ok: false, error: "Sorry, we couldn't send your order just now — please call us." }, 502);

  // Customer confirmation is best-effort — don't fail the order if it bounces.
  try { await sendEmail(env, order.email, "Your Wolves Removals box shop order", customerHtml); } catch (e) {}

  return json({ ok: true });
}
