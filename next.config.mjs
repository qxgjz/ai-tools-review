/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: 'export',
  images: { unoptimized: true },
  trailingSlash: true,
  staticPageGenerationTimeout: 300,
};

export default nextConfig;
