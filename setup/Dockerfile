# Base layer for Setup Utility
ARG DISTRO=node:22-alpine
FROM $DISTRO AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
ENV TZ=Etc/UTC LANG=C.UTF-8

RUN set -euxo pipefail \
  ; corepack enable \
  ; apk add --no-cache curl tzdata

WORKDIR /app

# Production dependencies layer
FROM base AS prod-deps

COPY package.json .
COPY pnpm-lock.yaml .

RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --prod --frozen-lockfile

# Build layer
FROM base AS build

COPY package.json .
COPY pnpm-lock.yaml .

RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --frozen-lockfile

COPY . .

RUN pnpm run build && pnpm prune --prod

# Runtime layer
FROM base AS runtime

ARG VERSION=local
LABEL version=$VERSION
LABEL org.opencontainers.image.url="https://github.com/heviat/Mailu-OIDC/tree/oidc-setup/setup#readme"
LABEL org.opencontainers.image.version=$VERSION
LABEL org.opencontainers.image.vendors="Heviat"
LABEL org.opencontainers.image.title="Mailu Setup Utility"
LABEL org.opencontainers.image.description="Set up a Mailu instance according to your needs. This tool generates configuration files for Mailu without you having to refer to the documentation all the time."

COPY --from=prod-deps /app/node_modules ./node_modules
COPY --from=build /app/build ./build

RUN echo "$VERSION" >> /version

EXPOSE 80/tcp
HEALTHCHECK --start-period=350s CMD ["curl", "-m3", "-skfLo", "/dev/null", "http://localhost/"]

ENV NODE_ENV=production
ENV PORT=80
CMD ["node","build/index.js"]
