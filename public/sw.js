if(!self.define){let e,s={};const a=(a,t)=>(a=new URL(a+".js",t).href,s[a]||new Promise((s=>{if("document"in self){const e=document.createElement("script");e.src=a,e.onload=s,document.head.appendChild(e)}else e=a,importScripts(a),s()})).then((()=>{let e=s[a];if(!e)throw new Error(`Module ${a} didn’t register its module`);return e})));self.define=(t,n)=>{const i=e||("document"in self?document.currentScript.src:"")||location.href;if(s[i])return;let c={};const r=e=>a(e,i),o={module:{uri:i},exports:c,require:r};s[i]=Promise.all(t.map((e=>o[e]||r(e)))).then((e=>(n(...e),c)))}}define(["./workbox-e9849328"],(function(e){"use strict";importScripts(),self.skipWaiting(),e.clientsClaim(),e.precacheAndRoute([{url:"/_next/app-build-manifest.json",revision:"0be776a1fa84b8fa74bd700c7e7b59bc"},{url:"/_next/static/chunks/314-bc94a5e38fe76cae.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/352-47d5e5d0a6ea0d06.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/376-3c5083598304069f.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/378-447a1a3684994517.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/429-20a15787e9aafbba.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/485-033c6eee4b92343e.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/750-fe222478be4519a0.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/905-7b835766c8a4bef7.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/94-e0358477ec7c9568.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/941-efa7fc43e2d7f79c.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/%5Bname%5D/page-b894e60f36bd1345.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/(auth)/login/page-cf5f10d6cc0a6fe3.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/(auth)/sign-in/page-bb15770d06df0620.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/(main)/layout-7fa8723005481d48.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/(main)/page-3de3c3c2d7f8c158.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/_not-found/page-adb3fb4cf4412409.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/layout-4e99edbb3f0a942e.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/nx/page-654ce3019747ca7e.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/register/page-3ce3aec9f3d33b11.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/settings/idcard/page-12854f4dfa7b6d29.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/settings/layout-0bb1bd10cbce5061.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/settings/page-3619413109cacb0e.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/settings/platform/page-4a284c127e2e08d4.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/app/test/page-47c73ce8299fc672.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/e4f73795-9d4abef19c4b0256.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/framework-6e06c675866dc992.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/main-ab71bbe48826412f.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/main-app-2701b0aa08048e57.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/pages/_app-a5985df79dbcabd6.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/pages/_error-84f9a10ef397fea5.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/chunks/polyfills-42372ed130431b0a.js",revision:"846118c33b2c0e922d7b3a7676f81f6f"},{url:"/_next/static/chunks/webpack-be31256aee916f67.js",revision:"wHaWytNF4fB33zs5UqarW"},{url:"/_next/static/css/d5e4f86dabba7df8.css",revision:"d5e4f86dabba7df8"},{url:"/_next/static/wHaWytNF4fB33zs5UqarW/_buildManifest.js",revision:"96e58a13991e9cd988ab557b612cbf9d"},{url:"/_next/static/wHaWytNF4fB33zs5UqarW/_ssgManifest.js",revision:"b6652df95db52feb4daf4eca35380933"},{url:"/fonts/XiaolaiMonoSC-Regular.ttf",revision:"cf08ec3f9087ac63381bd606ac7ba38c"},{url:"/next.svg",revision:"8e061864f388b47f33a1c3780831193e"},{url:"/vercel.svg",revision:"61c6b19abff40ea7acd577be818f3976"}],{ignoreURLParametersMatching:[]}),e.cleanupOutdatedCaches(),e.registerRoute("/",new e.NetworkFirst({cacheName:"start-url",plugins:[{cacheWillUpdate:async({request:e,response:s,event:a,state:t})=>s&&"opaqueredirect"===s.type?new Response(s.body,{status:200,statusText:"OK",headers:s.headers}):s}]}),"GET"),e.registerRoute(/^https:\/\/fonts\.(?:gstatic)\.com\/.*/i,new e.CacheFirst({cacheName:"google-fonts-webfonts",plugins:[new e.ExpirationPlugin({maxEntries:4,maxAgeSeconds:31536e3})]}),"GET"),e.registerRoute(/^https:\/\/fonts\.(?:googleapis)\.com\/.*/i,new e.StaleWhileRevalidate({cacheName:"google-fonts-stylesheets",plugins:[new e.ExpirationPlugin({maxEntries:4,maxAgeSeconds:604800})]}),"GET"),e.registerRoute(/\.(?:eot|otf|ttc|ttf|woff|woff2|font.css)$/i,new e.StaleWhileRevalidate({cacheName:"static-font-assets",plugins:[new e.ExpirationPlugin({maxEntries:4,maxAgeSeconds:604800})]}),"GET"),e.registerRoute(/\.(?:jpg|jpeg|gif|png|svg|ico|webp)$/i,new e.StaleWhileRevalidate({cacheName:"static-image-assets",plugins:[new e.ExpirationPlugin({maxEntries:64,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\/_next\/image\?url=.+$/i,new e.StaleWhileRevalidate({cacheName:"next-image",plugins:[new e.ExpirationPlugin({maxEntries:64,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:mp3|wav|ogg)$/i,new e.CacheFirst({cacheName:"static-audio-assets",plugins:[new e.RangeRequestsPlugin,new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:mp4)$/i,new e.CacheFirst({cacheName:"static-video-assets",plugins:[new e.RangeRequestsPlugin,new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:js)$/i,new e.StaleWhileRevalidate({cacheName:"static-js-assets",plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:css|less)$/i,new e.StaleWhileRevalidate({cacheName:"static-style-assets",plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\/_next\/data\/.+\/.+\.json$/i,new e.StaleWhileRevalidate({cacheName:"next-data",plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:json|xml|csv)$/i,new e.NetworkFirst({cacheName:"static-data-assets",plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute((({url:e})=>{if(!(self.origin===e.origin))return!1;const s=e.pathname;return!s.startsWith("/api/auth/")&&!!s.startsWith("/api/")}),new e.NetworkFirst({cacheName:"apis",networkTimeoutSeconds:10,plugins:[new e.ExpirationPlugin({maxEntries:16,maxAgeSeconds:86400})]}),"GET"),e.registerRoute((({url:e})=>{if(!(self.origin===e.origin))return!1;return!e.pathname.startsWith("/api/")}),new e.NetworkFirst({cacheName:"others",networkTimeoutSeconds:10,plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute((({url:e})=>!(self.origin===e.origin)),new e.NetworkFirst({cacheName:"cross-origin",networkTimeoutSeconds:10,plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:3600})]}),"GET")}));
