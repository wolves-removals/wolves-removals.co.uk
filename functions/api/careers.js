/* Cloudflare Pages Function — POST /api/careers
 *
 * Receives a job application from /job-vacancies/ and emails BOTH the Wolves Removals
 * team and the applicant (a confirmation copy) via Resend.
 *
 * Required Pages environment variables:
 *   RESEND_API_KEY   - a Resend API key (https://resend.com)
 *   CAREERS_FROM     - verified sender, e.g. "Wolves Removals Careers <careers@wolves-removals.co.uk>"
 *   CAREERS_TO       - where applications go, e.g. "info@wolves-removals.co.uk"
 *
 * Until the vars are set the form shows a friendly "email your CV" message — never breaks.
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
function validEmail(e) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(e || "")); }

async function sendEmail(env, to, subject, html, replyTo) {
  var body = { from: env.CAREERS_FROM, to: [to], subject: subject, html: html };
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

  if (!a.firstName) return json({ ok: false, error: "Please add your name." }, 400);
  if (!validEmail(a.email)) return json({ ok: false, error: "Please add a valid email address." }, 400);

  if (!env.RESEND_API_KEY || !env.CAREERS_FROM || !env.CAREERS_TO) {
    return json({ ok: false, error: "Applications aren't switched on online yet — please email your CV to us and we'll be in touch." }, 503);
  }

  var name = (esc(a.firstName) + " " + esc(a.lastName || "")).trim();
  var cats = Array.isArray(a.licenceCats) ? a.licenceCats.join(", ") : (a.licenceCats || "");
  function row(k, v) {
    return v ? '<tr><td style="padding:5px 10px;font-weight:bold;vertical-align:top;border-bottom:1px solid #eee">' + esc(k) +
      '</td><td style="padding:5px 10px;border-bottom:1px solid #eee">' + esc(v).replace(/\n/g, "<br>") + "</td></tr>" : "";
  }
  var table = '<table style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:14px;max-width:560px">' +
    row("Name", name) + row("Email", a.email) + row("Phone", a.phone) + row("Town / city", a.town) + row("Postcode", a.postcode) +
    row("Right to work", a.rightToWork) + row("Position", a.position) + row("Availability", a.availability) + row("Earliest start", a.startDate) +
    row("Driving licence", a.licence) + row("Years driving", a.yearsDriving) + row("Licence categories", cats) +
    row("Years in removals", a.yearsRemovals) + row("Previous experience", a.experience) + row("Why this role", a.whyRole) +
    "</table>";

  var teamHtml = '<div style="font-family:Arial,sans-serif;color:#262626"><h2>New job application</h2>' + table +
    '<p style="color:#777;font-size:12px">Sent from the wolves-removals.co.uk careers page.</p></div>';
  var applicantHtml = '<div style="font-family:Arial,sans-serif;color:#262626"><h2>Thanks for your application, ' + esc(a.firstName) + "!</h2>" +
    "<p>We&rsquo;ve received your application to join Wolves Removals and will review it within five working days. " +
    "If your experience is a fit, we&rsquo;ll be in touch to arrange a chat.</p><h3>Your application</h3>" + table +
    "<p>Many thanks,<br>The Wolves Removals team</p></div>";

  var sentTeam = await sendEmail(env, env.CAREERS_TO, "New job application — " + name, teamHtml, a.email);
  if (!sentTeam) return json({ ok: false, error: "Sorry, we couldn't send your application just now — please email us your CV." }, 502);

  try { await sendEmail(env, a.email, "Your Wolves Removals job application", applicantHtml); } catch (e) {}

  return json({ ok: true });
}
