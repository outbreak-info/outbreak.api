//WORKBOX

importScripts('https://storage.googleapis.com/workbox-cdn/releases/3.0.0/workbox-sw.js');

  workbox.precaching.precacheAndRoute([
    {
      "url": "/static/css/app.css",
      "revision": "fd2e1d3c4c8d43da10afe67a7d69fbd1"
    },
    {
      "url": "/",
      "revision": "39b8fb34f8be7ecf969530f1b9e69ba1"
    },
    {
      "url": "/static/js/contribute.js",
      "revision": "03bde26b6af07cd6bb0378ec0a50e410"
    },
    {
      "url": "/static/js/renderjson.js",
      "revision": "03bde26b6af07cd6bb0378ec0a50e410"
    },
    {
      "url": "/denovodb",
      "revision": "03bde26b6af07cd6bb0378ec0a50e410"
    },
    {
      "url": "/static/js/worker.js",
      "revision": "03bde26b6af07cd6bb0378ec0a50e410"
    },
    {
      "url": "https://pending.biothings.io/",
      "revision": "03bde26b6af07cd6bb0378ec0a50e410"
    },
    {
      "url": "https://pending.biothings.io/denovodb/metadata",
      "revision": "03bde26b6af07cd6bb0378ec0a50e410"
    },
    {
      "url": "https://pending.biothings.io/fire/metadata",
      "revision": "03bde26b6af07cd6bb0378ec0a50e410"
    },
    {
      "url": "https://pending.biothings.io/ccle/metadata",
      "revision": "03bde26b6af07cd6bb0378ec0a50e410"
    },
    {
      "url": "https://pending.biothings.io/biomuta/metadata",
      "revision": "03bde26b6af07cd6bb0378ec0a50e410"
    },
    {
      "url": "https://pending.biothings.io/kaviar/metadata",
      "revision": "03bde26b6af07cd6bb0378ec0a50e410"
    }
  ]);

  workbox.routing.registerRoute(
    new RegExp('https://pending.biothings.io/denobodb/metadata'),
    workbox.strategies.cacheFirst()
  );

  workbox.routing.registerRoute(
    new RegExp('https://pending.biothings.io/biomuta/metadata'),
    workbox.strategies.cacheFirst()
  );

  workbox.routing.registerRoute(
    new RegExp('https://pending.biothings.io/fire/metadata'),
    workbox.strategies.cacheFirst()
  );

  workbox.routing.registerRoute(
    new RegExp('https://pending.biothings.io/kaviar/metadata'),
    workbox.strategies.cacheFirst()
  );

  workbox.routing.registerRoute(
    new RegExp('https://pending.biothings.io/'),
    workbox.strategies.cacheFirst()
  );

  workbox.routing.registerRoute(
    new RegExp('https://pending.biothings.io/ccle/metadata'),
    workbox.strategies.cacheFirst()
  );

  workbox.routing.registerRoute(
    new RegExp('/'),
    new workbox.strategies.CacheFirst()
  );

  workbox.routing.registerRoute(
    new RegExp('/denobodb'),
    new workbox.strategies.CacheFirst()
  );

  workbox.routing.registerRoute(
    new RegExp('/static/js/contribute.js'),
    new workbox.strategies.CacheFirst()
  );

  workbox.routing.registerRoute(
    new RegExp('/static/js/renderjson.js'),
    new workbox.strategies.CacheFirst()
  );
