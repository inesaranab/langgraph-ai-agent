/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Remove output: 'export' for Vercel deployment (we want SSR capabilities)
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'http://localhost:8000',
    NEXT_PUBLIC_RAILWAY_URL: 'https://langgraph-ai-agent-production-7799.up.railway.app',
  },
}

module.exports = nextConfig