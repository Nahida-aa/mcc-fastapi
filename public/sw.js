if(!self.define){let e,s={};const n=(n,t)=>(n=new URL(n+".js",t).href,s[n]||new Promise((s=>{if("document"in self){const e=document.createElement("script");e.src=n,e.onload=s,document.head.appendChild(e)}else e=n,importScripts(n),s()})).then((()=>{let e=s[n];if(!e)throw new Error(`Module ${n} didn’t register its module`);return e})));self.define=(t,a)=>{const i=e||("document"in self?document.currentScript.src:"")||location.href;if(s[i])return;let c={};const l=e=>n(e,i),r={module:{uri:i},exports:c,require:l};s[i]=Promise.all(t.map((e=>r[e]||l(e)))).then((e=>(a(...e),c)))}}define(["./workbox-e9849328"],(function(e){"use strict";importScripts(),self.skipWaiting(),e.clientsClaim(),e.precacheAndRoute([{url:"/_next/app-build-manifest.json",revision:"679dc7220714e67b764feb529996592e"},{url:"/_next/static/Z_LCblIF6FTkDOb-7lFwL/_buildManifest.js",revision:"96e58a13991e9cd988ab557b612cbf9d"},{url:"/_next/static/Z_LCblIF6FTkDOb-7lFwL/_ssgManifest.js",revision:"b6652df95db52feb4daf4eca35380933"},{url:"/_next/static/chunks/314-bc94a5e38fe76cae.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/376-3c5083598304069f.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/378-447a1a3684994517.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/429-20a15787e9aafbba.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/485-033c6eee4b92343e.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/750-fe222478be4519a0.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/905-fd9fc79289329fde.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/94-e0358477ec7c9568.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/941-efa7fc43e2d7f79c.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/%5Bname%5D/page-b894e60f36bd1345.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/(auth)/login/page-cf5f10d6cc0a6fe3.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/(auth)/sign-in/page-bb15770d06df0620.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/(main)/layout-8b2b74dbb90daffd.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/(main)/page-3c2fdf23c5bf5b20.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/_not-found/page-adb3fb4cf4412409.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/layout-dc550d0a1a9c95a9.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/register/page-3ce3aec9f3d33b11.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/settings/idcard/page-12854f4dfa7b6d29.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/settings/layout-0bb1bd10cbce5061.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/settings/page-3619413109cacb0e.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/settings/platform/page-4a284c127e2e08d4.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/app/test/page-47c73ce8299fc672.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/e4f73795-9d4abef19c4b0256.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/framework-6e06c675866dc992.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/main-23c71c3c53944f97.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/main-app-2701b0aa08048e57.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/pages/_app-a5985df79dbcabd6.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/pages/_error-84f9a10ef397fea5.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/chunks/polyfills-42372ed130431b0a.js",revision:"846118c33b2c0e922d7b3a7676f81f6f"},{url:"/_next/static/chunks/webpack-c62ffb01b0a32269.js",revision:"Z_LCblIF6FTkDOb-7lFwL"},{url:"/_next/static/css/cad3cebd098146e7.css",revision:"cad3cebd098146e7"}],{ignoreURLParametersMatching:[]}),e.cleanupOutdatedCaches(),e.registerRoute("/",new e.NetworkFirst({cacheName:"start-url",plugins:[{cacheWillUpdate:async({request:e,response:s,event:n,state:t})=>s&&"opaqueredirect"===s.type?new Response(s.body,{status:200,statusText:"OK",headers:s.headers}):s}]}),"GET"),e.registerRoute(/^https:\/\/fonts\.(?:gstatic)\.com\/.*/i,new e.CacheFirst({cacheName:"google-fonts-webfonts",plugins:[new e.ExpirationPlugin({maxEntries:4,maxAgeSeconds:31536e3})]}),"GET"),e.registerRoute(/^https:\/\/fonts\.(?:googleapis)\.com\/.*/i,new e.StaleWhileRevalidate({cacheName:"google-fonts-stylesheets",plugins:[new e.ExpirationPlugin({maxEntries:4,maxAgeSeconds:604800})]}),"GET"),e.registerRoute(/\.(?:eot|otf|ttc|ttf|woff|woff2|font.css)$/i,new e.StaleWhileRevalidate({cacheName:"static-font-assets",plugins:[new e.ExpirationPlugin({maxEntries:4,maxAgeSeconds:604800})]}),"GET"),e.registerRoute(/\.(?:jpg|jpeg|gif|png|svg|ico|webp)$/i,new e.StaleWhileRevalidate({cacheName:"static-image-assets",plugins:[new e.ExpirationPlugin({maxEntries:64,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\/_next\/image\?url=.+$/i,new e.StaleWhileRevalidate({cacheName:"next-image",plugins:[new e.ExpirationPlugin({maxEntries:64,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:mp3|wav|ogg)$/i,new e.CacheFirst({cacheName:"static-audio-assets",plugins:[new e.RangeRequestsPlugin,new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:mp4)$/i,new e.CacheFirst({cacheName:"static-video-assets",plugins:[new e.RangeRequestsPlugin,new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:js)$/i,new e.StaleWhileRevalidate({cacheName:"static-js-assets",plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:css|less)$/i,new e.StaleWhileRevalidate({cacheName:"static-style-assets",plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\/_next\/data\/.+\/.+\.json$/i,new e.StaleWhileRevalidate({cacheName:"next-data",plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:json|xml|csv)$/i,new e.NetworkFirst({cacheName:"static-data-assets",plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute((({url:e})=>{if(!(self.origin===e.origin))return!1;const s=e.pathname;return!s.startsWith("/api/auth/")&&!!s.startsWith("/api/")}),new e.NetworkFirst({cacheName:"apis",networkTimeoutSeconds:10,plugins:[new e.ExpirationPlugin({maxEntries:16,maxAgeSeconds:86400})]}),"GET"),e.registerRoute((({url:e})=>{if(!(self.origin===e.origin))return!1;return!e.pathname.startsWith("/api/")}),new e.NetworkFirst({cacheName:"others",networkTimeoutSeconds:10,plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute((({url:e})=>!(self.origin===e.origin)),new e.NetworkFirst({cacheName:"cross-origin",networkTimeoutSeconds:10,plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:3600})]}),"GET")}));
