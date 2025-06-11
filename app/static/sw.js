const CACHE_NAME = 'task-manager-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/icons/icon.svg',
    '/static/manifest.json',
    '/auth/login',
    '/auth/register',
    '/tasks',
    '/tasks/create',
    '/profile'
];

// Cache strategies
const CACHE_FIRST = 'cache-first';
const NETWORK_FIRST = 'network-first';

// Routes that should use network-first strategy
const NETWORK_FIRST_ROUTES = [
    '/tasks',
    '/tasks/create',
    '/profile'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);
    const path = url.pathname;

    // Use network-first strategy for dynamic routes
    if (NETWORK_FIRST_ROUTES.some(route => path.startsWith(route))) {
        event.respondWith(networkFirstStrategy(event.request));
    } else {
        // Use cache-first strategy for static assets
        event.respondWith(cacheFirstStrategy(event.request));
    }
});

async function networkFirstStrategy(request) {
    try {
        const networkResponse = await fetch(request);
        const cache = await caches.open(CACHE_NAME);
        cache.put(request, networkResponse.clone());
        return networkResponse;
    } catch (error) {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        // Return offline page for HTML requests
        if (request.headers.get('accept').includes('text/html')) {
            return caches.match('/offline.html');
        }
        throw error;
    }
}

async function cacheFirstStrategy(request) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
        return cachedResponse;
    }
    try {
        const networkResponse = await fetch(request);
        const cache = await caches.open(CACHE_NAME);
        cache.put(request, networkResponse.clone());
        return networkResponse;
    } catch (error) {
        throw error;
    }
}

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
}); 