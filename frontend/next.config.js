/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: 'standalone', // Required for Railway deployment
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'http://localhost:8000',
    NEXT_PUBLIC_RAILWAY_URL: process.env.NEXT_PUBLIC_RAILWAY_URL || 'https://langgraph-ai-agent-production-561e.up.railway.app',
  },
}

module.exports = nextConfig