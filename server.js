const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = 3000;

// Store URLs in memory
const urlStore = {};

// Generate a random 6-character short code
function generateCode() {
  return Math.random().toString(36).substring(2, 8);
}

const server = http.createServer((req, res) => {
  const url = req.url;
  const method = req.method;

  // ── Serve index.html ──────────────────────────────────────────
  if (url === "/" && method === "GET") {
    const filePath = path.join(__dirname, "index.html");
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(500);
        res.end("Error loading page");
        return;
      }
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end(data);
    });
    return;
  }

  // ── POST /shorten ─────────────────────────────────────────────
  if (url === "/shorten" && method === "POST") {
    let body = "";
    req.on("data", (chunk) => (body += chunk));
    req.on("end", () => {
      try {
        const { longUrl, alias } = JSON.parse(body);

        if (!longUrl) {
          res.writeHead(400, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ error: "Please enter a URL" }));
          return;
        }

        // Validate URL
        try { new URL(longUrl); } catch {
          res.writeHead(400, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ error: "Invalid URL. Include http:// or https://" }));
          return;
        }

        const code = alias && alias.trim() ? alias.trim() : generateCode();

        if (urlStore[code]) {
          res.writeHead(409, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ error: "That alias is already taken" }));
          return;
        }

        urlStore[code] = { longUrl, code, clicks: 0 };

        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({
          shortUrl: `http://localhost:${PORT}/${code}`,
          code,
          longUrl
        }));
      } catch {
        res.writeHead(400, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "Bad request" }));
      }
    });
    return;
  }

  // ── GET /urls (list all) ──────────────────────────────────────
  if (url === "/urls" && method === "GET") {
    const list = Object.values(urlStore).reverse();
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(list));
    return;
  }

  // ── Redirect short URLs ───────────────────────────────────────
  const code = url.slice(1); // remove leading /
  if (urlStore[code]) {
    urlStore[code].clicks++;
    res.writeHead(302, { Location: urlStore[code].longUrl });
    res.end();
    return;
  }

  // ── 404 ───────────────────────────────────────────────────────
  res.writeHead(404, { "Content-Type": "text/html" });
  res.end(`<h2>404 - Short link not found</h2><a href="/">Go back</a>`);
});

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
