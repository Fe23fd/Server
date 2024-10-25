version: "3.8"

services:
  minecraft:
    image: itzg/minecraft-server
    tty: true
    stdin_open: true
    ports:
      - "25565:25565"
    environment:
      TYPE: "AUTO_CURSEFORGE"
      CF_API_KEY: "$$2a$$10$$akGZEcR7WCaJYJdHtr9hv.pUxBP3CaQp.9gFV2ikFHlOC.f./h8Wa"
      CF_PAGE_URL: "https://legacy.curseforge.com/minecraft/modpacks/modsaq"
      # The project ID of mods to exclude.
      CF_EXCLUDE_MODS: "1127952"
      MEMORY: "4G"
      MAX_MEMORY: "8G"
      VERSION: "1.16.5"
      EULA: "TRUE"
    volumes:
      # attach the relative directory 'data' to the container's /data path
      - F:\mcdata:/data
    restart: on-failure:3
