if(!self.define){let e,s={};const i=(i,n)=>(i=new URL(i+".js",n).href,s[i]||new Promise((s=>{if("document"in self){const e=document.createElement("script");e.src=i,e.onload=s,document.head.appendChild(e)}else e=i,importScripts(i),s()})).then((()=>{let e=s[i];if(!e)throw new Error(`Module ${i} didn’t register its module`);return e})));self.define=(n,t)=>{const a=e||("document"in self?document.currentScript.src:"")||location.href;if(s[a])return;let c={};const o=e=>i(e,a),r={module:{uri:a},exports:c,require:o};s[a]=Promise.all(n.map((e=>r[e]||o(e)))).then((e=>(t(...e),c)))}}define(["./workbox-e9849328"],(function(e){"use strict";importScripts(),self.skipWaiting(),e.clientsClaim(),e.precacheAndRoute([{url:"/_next/app-build-manifest.json",revision:"552a637db4a785a3760b472b269b2e3f"},{url:"/_next/static/chunks/314-bc94a5e38fe76cae.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/376-77a10d5f6e338b7b.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/378-447a1a3684994517.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/429-fb9a80a90233642c.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/485-033c6eee4b92343e.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/750-fe222478be4519a0.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/905-fd9fc79289329fde.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/94-e0358477ec7c9568.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/app/%5Bname%5D/page-f7294c94b722b72f.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/app/(auth)/sign-in/page-b24ba3567dc18075.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/app/(main)/layout-1d733d9bfcbab129.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/app/(main)/page-6619e45c37cf3164.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/app/_not-found/page-adb3fb4cf4412409.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/app/layout-dc550d0a1a9c95a9.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/app/register/page-8cff0cd15acaa8b3.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/app/settings/idcard/page-f4e8138dd09fe66a.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/app/settings/layout-0bb1bd10cbce5061.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/app/settings/page-78bc940beac7ae64.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/app/settings/platform/page-21f66cdb4762300d.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/app/test/page-47c73ce8299fc672.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/e4f73795-9d4abef19c4b0256.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/framework-6e06c675866dc992.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/main-448a9be231ad412b.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/main-app-2701b0aa08048e57.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/pages/_app-a5985df79dbcabd6.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/pages/_error-84f9a10ef397fea5.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/chunks/polyfills-42372ed130431b0a.js",revision:"846118c33b2c0e922d7b3a7676f81f6f"},{url:"/_next/static/chunks/webpack-8be8ef9dc5bccb87.js",revision:"zwxS3yiEiolVMAPwJPJ_C"},{url:"/_next/static/css/f8f086d033a671ea.css",revision:"f8f086d033a671ea"},{url:"/_next/static/zwxS3yiEiolVMAPwJPJ_C/_buildManifest.js",revision:"96e58a13991e9cd988ab557b612cbf9d"},{url:"/_next/static/zwxS3yiEiolVMAPwJPJ_C/_ssgManifest.js",revision:"b6652df95db52feb4daf4eca35380933"}],{ignoreURLParametersMatching:[]}),e.cleanupOutdatedCaches(),e.registerRoute("/",new e.NetworkFirst({cacheName:"start-url",plugins:[{cacheWillUpdate:async({request:e,response:s,event:i,state:n})=>s&&"opaqueredirect"===s.type?new Response(s.body,{status:200,statusText:"OK",headers:s.headers}):s}]}),"GET"),e.registerRoute(/^https:\/\/fonts\.(?:gstatic)\.com\/.*/i,new e.CacheFirst({cacheName:"google-fonts-webfonts",plugins:[new e.ExpirationPlugin({maxEntries:4,maxAgeSeconds:31536e3})]}),"GET"),e.registerRoute(/^https:\/\/fonts\.(?:googleapis)\.com\/.*/i,new e.StaleWhileRevalidate({cacheName:"google-fonts-stylesheets",plugins:[new e.ExpirationPlugin({maxEntries:4,maxAgeSeconds:604800})]}),"GET"),e.registerRoute(/\.(?:eot|otf|ttc|ttf|woff|woff2|font.css)$/i,new e.StaleWhileRevalidate({cacheName:"static-font-assets",plugins:[new e.ExpirationPlugin({maxEntries:4,maxAgeSeconds:604800})]}),"GET"),e.registerRoute(/\.(?:jpg|jpeg|gif|png|svg|ico|webp)$/i,new e.StaleWhileRevalidate({cacheName:"static-image-assets",plugins:[new e.ExpirationPlugin({maxEntries:64,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\/_next\/image\?url=.+$/i,new e.StaleWhileRevalidate({cacheName:"next-image",plugins:[new e.ExpirationPlugin({maxEntries:64,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:mp3|wav|ogg)$/i,new e.CacheFirst({cacheName:"static-audio-assets",plugins:[new e.RangeRequestsPlugin,new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:mp4)$/i,new e.CacheFirst({cacheName:"static-video-assets",plugins:[new e.RangeRequestsPlugin,new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:js)$/i,new e.StaleWhileRevalidate({cacheName:"static-js-assets",plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:css|less)$/i,new e.StaleWhileRevalidate({cacheName:"static-style-assets",plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\/_next\/data\/.+\/.+\.json$/i,new e.StaleWhileRevalidate({cacheName:"next-data",plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute(/\.(?:json|xml|csv)$/i,new e.NetworkFirst({cacheName:"static-data-assets",plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute((({url:e})=>{if(!(self.origin===e.origin))return!1;const s=e.pathname;return!s.startsWith("/api/auth/")&&!!s.startsWith("/api/")}),new e.NetworkFirst({cacheName:"apis",networkTimeoutSeconds:10,plugins:[new e.ExpirationPlugin({maxEntries:16,maxAgeSeconds:86400})]}),"GET"),e.registerRoute((({url:e})=>{if(!(self.origin===e.origin))return!1;return!e.pathname.startsWith("/api/")}),new e.NetworkFirst({cacheName:"others",networkTimeoutSeconds:10,plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:86400})]}),"GET"),e.registerRoute((({url:e})=>!(self.origin===e.origin)),new e.NetworkFirst({cacheName:"cross-origin",networkTimeoutSeconds:10,plugins:[new e.ExpirationPlugin({maxEntries:32,maxAgeSeconds:3600})]}),"GET")}));
