/* Service worker kalkulatora Carthago.
   Wersję stempluje build.py — każda kompilacja tworzy nową pamięć podręczną. */

const VERSION = "2026-08-24-2259";
const CACHE = "carthago-" + VERSION;

const PRECACHE = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  "./icon-maskable-512.png",
  "./apple-touch-icon.png"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE)
      .then(function (cache) { return cache.addAll(PRECACHE); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (names) {
        return Promise.all(names
          .filter(function (name) { return name !== CACHE; })
          .map(function (name) { return caches.delete(name); }));
      })
      .then(function () { return self.clients.claim(); })
  );
});

// Odpowiedzi logowania Cloudflare Access nie mogą trafić do pamięci podręcznej,
// bo zastąpiłyby kalkulator ekranem logowania.
function cacheable(response) {
  return response && response.ok && !response.redirected && response.type === "basic";
}

self.addEventListener("fetch", function (event) {
  const request = event.request;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  const sameOrigin = url.origin === self.location.origin;

  // Strona: najpierw sieć (świeża wersja po wdrożeniu), offline z pamięci.
  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then(function (response) {
          if (cacheable(response)) {
            const copy = response.clone();
            caches.open(CACHE).then(function (cache) { cache.put("./index.html", copy); });
          }
          return response;
        })
        .catch(function () {
          return caches.match("./index.html").then(function (cached) {
            return cached || Response.error();
          });
        })
    );
    return;
  }

  // Pliki własne i fonty: najpierw pamięć, w tle uzupełniana z sieci.
  event.respondWith(
    caches.match(request).then(function (cached) {
      const fromNetwork = fetch(request)
        .then(function (response) {
          const storable = sameOrigin ? cacheable(response) : (response && response.status === 200);
          if (storable) {
            const copy = response.clone();
            caches.open(CACHE).then(function (cache) { cache.put(request, copy); });
          }
          return response;
        })
        .catch(function () { return cached || Response.error(); });

      return cached || fromNetwork;
    })
  );
});
