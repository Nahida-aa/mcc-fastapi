// import type { NextConfig } from 'next'; // next15
import nextPWA from "next-pwa";
import { fileURLToPath } from 'url';

const isDev = process.env.NODE_ENV === "development";

const withPWA = nextPWA({
  dest: "public",
  register: true,
  skipWaiting: true,
  // disable: isDev,
});

/** @type {import('next').NextConfig} */
// const nextConfig: NextConfig = { // next15
const nextConfig = {
  webpack: (config, { isServer }) => {
    if (!isServer) {
      const __filename = fileURLToPath(import.meta.url);
      config.cache = {
        type: 'filesystem',
        buildDependencies: {
          config: [__filename],
        },
      };
    }
    return config;
  },
  images: {
    remotePatterns: [
      {
        hostname: 'avatar.vercel.sh',
      },
      {
        hostname: 'avatars.githubusercontent.com',
      }
    ],
  },
  rewrites: async () => {
    return [
      {
        source: "/api/py/:path*",
        destination:
          isDev
            ? "http://127.0.0.1:8000/api/py/:path*"
            : "/api/",
      },
      {
        source: "/docs",
        destination:
          isDev
            ? "http://127.0.0.1:8000/api/py/docs"
            : "/api/py/docs",
      },
      {
        source: "/openapi.json",
        destination:
          isDev
            ? "http://127.0.0.1:8000/api/py/openapi.json"
            : "/api/py/openapi.json",
      },
    ];
  },
};

export default withPWA(nextConfig); // mjs, esmodule

// module.exports = nextConfig; // js, commonjs
