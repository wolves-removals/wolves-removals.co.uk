/* Cloudflare Pages Function — GET /api/social
 *
 * Returns the latest Wolves Removals Facebook posts as JSON in the shape the
 * home-page carousel expects. The site front-end fetches this and falls back to
 * the embedded posts if it errors, so the page never breaks.
 *
 * Required Pages environment variables (Settings -> Environment variables):
 *   FB_PAGE_ID     - the numeric Facebook Page ID
 *   FB_PAGE_TOKEN  - a long-lived Page access token (see SOCIAL-FEED-SETUP.md)
 *
 * Edge-cached for 15 minutes so we never hammer the Graph API.
 */

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function fmtDate(iso) {
  const d = new Date(iso);
  if (isNaN(d)) return "";
  return d.getUTCDate() + " " + MONTHS[d.getUTCMonth()] + " " + d.getUTCFullYear();
}

function firstLine(msg) {
  const line = (msg || "").split("\n")[0].trim();
  return line.length > 64 ? line.slice(0, 61).trim() + "…" : line;
}

function hashtags(msg) {
  const m = (msg || "").match(/#[A-Za-z0-9_]+/g);
  return m ? m.join(" ") : "";
}

function captionBody(msg) {
  // Strip the trailing hashtag block so the caption text reads cleanly.
  return (msg || "").replace(/(\s*#[A-Za-z0-9_]+)+\s*$/, "").trim();
}

function json(obj, maxAge) {
  return new Response(JSON.stringify(obj), {
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "public, max-age=" + maxAge + ", s-maxage=" + maxAge
    }
  });
}

export async function onRequestGet(context) {
  const env = context.env || {};
  if (!env.FB_PAGE_ID || !env.FB_PAGE_TOKEN) {
    // Not configured yet — front-end keeps its fallback posts.
    return json({ posts: [], configured: false }, 60);
  }

  const fields = [
    "id", "message", "created_time", "permalink_url", "full_picture",
    "attachments{media_type}", "likes.summary(true)", "comments.summary(true)"
  ].join(",");

  const url = "https://graph.facebook.com/v19.0/" + encodeURIComponent(env.FB_PAGE_ID) +
    "/posts?limit=12&fields=" + encodeURIComponent(fields) +
    "&access_token=" + encodeURIComponent(env.FB_PAGE_TOKEN);

  try {
    const res = await fetch(url, { cf: { cacheTtl: 900, cacheEverything: true } });
    if (!res.ok) return json({ posts: [], error: "graph " + res.status }, 60);
    const data = await res.json();
    const rows = Array.isArray(data.data) ? data.data : [];

    const posts = rows
      .filter(function (p) { return p.full_picture; })
      .map(function (p) {
        const att = p.attachments && p.attachments.data && p.attachments.data[0];
        const isVideo = !!(att && att.media_type && att.media_type.toLowerCase() === "video");
        return {
          date: fmtDate(p.created_time),
          img: p.full_picture,
          alt: "Wolves Removals Facebook post — " + (firstLine(p.message) || "update"),
          likes: (p.likes && p.likes.summary && p.likes.summary.total_count) || 0,
          comments: (p.comments && p.comments.summary && p.comments.summary.total_count) || 0,
          video: isVideo,
          title: firstLine(p.message) || "Wolves Removals",
          caption: captionBody(p.message) || "",
          tags: hashtags(p.message),
          permalink: p.permalink_url || ("https://www.facebook.com/" + env.FB_PAGE_ID)
        };
      })
      .slice(0, 9);

    return json({ posts: posts, configured: true }, 900);
  } catch (e) {
    return json({ posts: [], error: String(e) }, 60);
  }
}
