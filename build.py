#!/usr/bin/env python3
"""Buduje wersję PWA (index.html) ze źródła kalkulatora.

kalkulator.html jest źródłem publikowanym jako Artifact — celowo bez znaczników
<!doctype>, <html>, <head> i <body>. Ten skrypt opakowuje go w pełną stronę:
dokłada nagłówek dokumentu, manifest, ikony i rejestrację service workera,
a przy okazji stempluje wersję w sw.js, żeby przeglądarki pobrały świeże pliki.

Użycie:  python3 build.py
"""

import datetime
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SOURCE = ROOT / "kalkulator.html"
TARGET = ROOT / "index.html"
WORKER = ROOT / "sw.js"

HEAD = """<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Kalkulator ceny kampera Carthago: rabaty, koszty fabryczne, skonto, akcyza i transport.">
<meta name="theme-color" content="#14496b" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0e151b" media="(prefers-color-scheme: dark)">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Kalkulator">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png" sizes="192x192">
<link rel="icon" href="icon-512.png" sizes="512x512">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
__HEAD_EXTRA__
<style>
  /* pasek kwoty ponad obszarem gestów na telefonie */
  .mobile-bar { padding-bottom: calc(10px + env(safe-area-inset-bottom)) !important; }
  #updateBar {
    position: fixed;
    left: 50%;
    transform: translateX(-50%);
    bottom: calc(96px + env(safe-area-inset-bottom));
    z-index: 40;
    display: none;
    gap: 10px;
    align-items: center;
    padding: 10px 14px;
    border-radius: 10px;
    background: #14496b;
    color: #fff;
    font-family: "Barlow", system-ui, sans-serif;
    font-size: 14px;
    box-shadow: 0 10px 30px -12px rgba(0, 0, 0, .6);
  }
  #updateBar button {
    font: inherit;
    font-weight: 600;
    color: #14496b;
    background: #fff;
    border: none;
    border-radius: 7px;
    padding: 6px 12px;
    cursor: pointer;
  }
  @media (min-width: 900px) { #updateBar { bottom: 24px; } }
</style>
</head>
<body>
"""

FOOT = """
<div id="updateBar" role="status">
  <span>Jest nowsza wersja kalkulatora</span>
  <button type="button" onclick="location.reload()">Odśwież</button>
</div>
<script>
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("sw.js").then(function (reg) {
        reg.addEventListener("updatefound", function () {
          var fresh = reg.installing;
          if (!fresh) return;
          fresh.addEventListener("statechange", function () {
            // nowa wersja gotowa, a stara nadal obsługuje stronę
            if (fresh.state === "installed" && navigator.serviceWorker.controller) {
              document.getElementById("updateBar").style.display = "flex";
            }
          });
        });
      }).catch(function () { /* offline albo brak uprawnień — kalkulator działa dalej */ });
    });
  }
</script>
</body>
</html>
"""


def main():
    source = SOURCE.read_text(encoding="utf-8")

    # <title> i <link> do fontów należą do <head>, reszta zostaje treścią strony
    head_extra = []
    for pattern in (r"<title>.*?</title>", r'<link rel="(?:preconnect|stylesheet)"[^>]*>'):
        for match in re.findall(pattern, source, flags=re.S):
            head_extra.append(match)
            source = source.replace(match, "", 1)

    TARGET.write_text(
        HEAD.replace("__HEAD_EXTRA__", "\n".join(head_extra)) + source.strip() + FOOT,
        encoding="utf-8",
    )

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d-%H%M")
    worker = WORKER.read_text(encoding="utf-8")
    worker = re.sub(r'const VERSION = "[^"]*";', 'const VERSION = "%s";' % stamp, worker, count=1)
    WORKER.write_text(worker, encoding="utf-8")

    print("index.html zbudowany, sw.js ostemplowany wersją " + stamp)


if __name__ == "__main__":
    main()
