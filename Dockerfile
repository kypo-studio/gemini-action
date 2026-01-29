# ================================================================
# STAGE 1: Dependencies
# ================================================================
FROM node:18-alpine AS dependencies

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm ci --only=production

# ================================================================
# STAGE 2: Build
# ================================================================
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including dev)
RUN npm ci

# Copy source code
COPY . .

# Run linting and tests (optional, can be removed if already done in CI)
# RUN npm run lint
# RUN npm test

# ================================================================
# STAGE 3: Production
# ================================================================
FROM node:18-alpine

# Set NODE_ENV
ENV NODE_ENV=production

# Create app user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy dependencies from dependencies stage
COPY --from=dependencies --chown=nodejs:nodejs /app/node_modules ./node_modules

# Copy application code from build stage
COPY --from=build --chown=nodejs:nodejs /app/src ./src
COPY --from=build --chown=nodejs:nodejs /app/package*.json ./

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start the application
CMD ["node", "src/app.js"]
