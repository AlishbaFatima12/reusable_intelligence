/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Ignore TypeScript errors during build for deployment
  typescript: {
    ignoreBuildErrors: true,
  },

  // Ignore ESLint errors during build
  eslint: {
    ignoreDuringBuilds: true,
  },

  // Environment variables exposed to the browser
  env: {
    PROGRESS_TRACKER_URL: process.env.PROGRESS_TRACKER_URL || 'http://localhost:8006',
    TRIAGE_AGENT_URL: process.env.TRIAGE_AGENT_URL || 'http://localhost:8001',
    WEBSOCKET_URL: process.env.WEBSOCKET_URL || 'http://localhost:4001',
  },

  // Silence multiple lockfiles warning
  outputFileTracingRoot: require('path').join(__dirname, '..'),

  // Webpack config for Three.js
  webpack: (config) => {
    config.externals = [...(config.externals || []), { canvas: 'canvas' }];
    return config;
  },
};

module.exports = nextConfig;
