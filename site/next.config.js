/** @type {import('next').NextConfig} */

const nextConfig = {
  output: 'export',
  distDir: '../public',
  env: {
    name: 'Steemers Kasm Registry',
    description: 'Eigen Kasm Workspaces registry van Steemers ICT: LinuxServer.io-apps (o.a. Ferdium) voor Kasm 1.19.',
    icon: 'https://steemersict.github.io/kasm-registry/1.1/steemers.svg',
    listUrl: 'https://steemersict.github.io/kasm-registry/',
    contactUrl: 'https://github.com/steemersict/kasm-registry/issues',
  },
  reactStrictMode: true,
  basePath: '/kasm-registry/1.0',
  trailingSlash: true,
  images: {
    unoptimized: true,
  }
}

module.exports = nextConfig
