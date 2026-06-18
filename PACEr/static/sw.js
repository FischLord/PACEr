const CACHE_NAME = 'pacer-offline-v2';
const APP_SHELL = [
    '/rechner',
    '/static/js/pace-core.js',
    '/static/js/calculator.js',
    '/static/js/layout.js',
    '/static/img/pacerLogoSmall.png',
    '/static/img/pacerLogo.png',
    '/static/img/pacer-icon-128.png',
    '/static/img/pacer-icon-192.png'
];

function isAdminOrPrivatePath(pathname) {
    return pathname.startsWith('/admin') ||
        pathname === '/adminLogin' ||
        pathname === '/adminTools' ||
        pathname === '/changePassword' ||
        pathname === '/viewReports';
}

function cacheStaticResponse(request) {
    return fetch(request)
        .then(function(response) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then(function(cache) { cache.put(request, copy); });
            return response;
        })
        .catch(function() { return caches.match(request); });
}

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) { return cache.addAll(APP_SHELL); })
            .then(function() { return self.skipWaiting(); })
    );
});

self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(cacheNames.map(function(cacheName) {
                if (cacheName !== CACHE_NAME) {
                    return caches.delete(cacheName);
                }
            }));
        }).then(function() { return self.clients.claim(); })
    );
});

self.addEventListener('fetch', function(event) {
    const request = event.request;
    if (request.method !== 'GET') return;

    const url = new URL(request.url);
    if (url.origin !== self.location.origin) return;
    if (isAdminOrPrivatePath(url.pathname)) return;

    if (request.mode === 'navigate') {
        event.respondWith(
            fetch(request)
                .then(function(response) {
                    const copy = response.clone();
                    if (url.pathname === '/rechner') {
                        caches.open(CACHE_NAME).then(function(cache) { cache.put('/rechner', copy); });
                    }
                    return response;
                })
                .catch(function() { return caches.match('/rechner'); })
        );
        return;
    }

    if (url.pathname.startsWith('/static/')) {
        event.respondWith(cacheStaticResponse(request));
    }
});
