# Facebook social feed — setup

The home-page **"Follow Us on Facebook"** carousel auto-updates from your Facebook
Page via a Cloudflare Pages Function at `/api/social`. Until it's configured it
shows the built-in fallback posts, so the site is never broken.

Files involved:
- `functions/api/social.js` — calls the Graph API, returns the latest posts as JSON (edge-cached 15 min).
- `js/social-feed.js` — front-end fetches `/api/social`, falls back to the embedded posts on any error.
- `tools/render_home.py` → `SOCIAL_POSTS` — the fallback posts shown before live data loads.

## What you need to provide (one-time)

Two Cloudflare environment variables: **`FB_PAGE_ID`** and **`FB_PAGE_TOKEN`**.

### 1. Get the Page ID
Facebook Page → **About** → scroll to **Page transparency / Page ID**, or use
[findmyfbid.com]. It's a long number.

### 2. Create a Facebook App + long-lived Page token
1. Go to **developers.facebook.com** → **My Apps → Create App** → type **Business**.
2. Open **Tools → Graph API Explorer**.
3. Select your app, click **Generate Access Token**, and grant these permissions:
   `pages_show_list`, `pages_read_engagement`, `pages_read_user_content`.
4. This gives a **short-lived user token**. Exchange it for a **long-lived** one:
   `GET /oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_TOKEN`
5. With the long-lived **user** token, call `GET /me/accounts` — copy the
   `access_token` for your Page. **Page tokens derived from a long-lived user
   token do not expire**, which is what we want.
6. Verify in **Tools → Access Token Debugger** that the Page token shows
   "Expires: Never".

> Note: a Facebook App in "Development" mode can read its own Pages fine. You only
> need App Review if you later expand scope. Keep the App Secret private.

### 3. Add the variables to Cloudflare Pages
Cloudflare dashboard → **Pages → (this project) → Settings → Environment variables**:
- `FB_PAGE_ID` = your numeric page id
- `FB_PAGE_TOKEN` = the long-lived Page token (add to **Production** and **Preview**; mark as **Encrypted/secret**)

Then **Redeploy**.

## Verify
Visit `https://wolves-removals.co.uk/api/social` — you should see JSON with a
`posts` array and `"configured": true`. The home-page carousel will then show your
real, latest Facebook posts (refreshing at the edge every 15 minutes).

If `posts` is empty or `configured:false`, the page keeps the fallback posts and
no error is shown to visitors — re-check the token/permissions.

## Notes
- Post images come straight from Facebook's CDN (allowed by the site CSP `img-src https:`).
- New posts appear automatically within ~15 minutes (the edge cache window).
- To change the fallback posts, edit `SOCIAL_POSTS` in `tools/render_home.py`.
