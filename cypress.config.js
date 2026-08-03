const { defineConfig } = require("cypress");
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");

// Largeur (en px) du panneau "Command Log" que Cypress incruste à gauche de la
// vidéo enregistrée en mode `cypress run` (contrairement à cy.screenshot(), qui
// ne capture que l'app). Pas d'option native pour l'exclure — on recadre la
// vidéo après coup avec ffmpeg. 320px est une première estimation : si le
// recadrage n'est pas exactement sur le bord de l'app, ajuster cette valeur.
const VIDEO_CROP_LEFT_PX = 320;

module.exports = defineConfig({
  screenshotsFolder: "cypress/screenshots",
  // false : les captures sont rangées par langue (fr/, en/) dans le même
  // dossier de spec (voir cy.maybeScreenshot()). Avec `true`, chaque nouveau
  // `cypress run` de ce spec videait tout cypress/screenshots/creation-poste.cy.js/
  // — donc le run EN supprimait les captures FR juste produites avant de
  // générer les siennes. Makefile fait le nettoyage explicite à la place.
  trashAssetsBeforeRuns: false,
  video: true,
  // > 1024px (breakpoint Tailwind `lg`) pour que le menu desktop (navbar.html)
  // soit affiché plutôt que le menu mobile — les tests ciblent le menu desktop.
  viewportWidth: 1920,
  viewportHeight: 1080,
  e2e: {
    baseUrl: process.env.TEAMFIT_BASE_URL,
    env: {
      TEAMFIT_TEST_EMAIL: process.env.TEAMFIT_TEST_EMAIL,
      TEAMFIT_TEST_PASSWORD: process.env.TEAMFIT_TEST_PASSWORD,
    },
    setupNodeEvents(on, config) {
      // Bug connu Cypress sur Mac Retina : en headless, le navigateur Electron
      // par défaut est plafonné par la résolution physique de l'écran et ignore
      // viewportWidth au-delà — les captures étaient tronquées à droite quelle
      // que soit la valeur configurée (cf. cypress-io/cypress#2313, #6485).
      // Chrome headless respecte --window-size si on désactive le scaling Retina.
      on("before:browser:launch", (browser, launchOptions) => {
        if (browser.family === "chromium" && browser.name !== "electron") {
          launchOptions.args.push(
            `--window-size=${config.viewportWidth},${config.viewportHeight}`
          );
          launchOptions.args.push("--force-device-scale-factor=1");
          launchOptions.args.push("--high-dpi-support=1");
        }
        return launchOptions;
      });

      // Recadre la vidéo après chaque spec pour retirer le panneau Command Log
      // (ffmpeg requis : `brew install ffmpeg`). Si ffmpeg est absent ou échoue,
      // on garde la vidéo brute plutôt que de faire échouer le run.
      on("after:spec", (spec, results) => {
        const videoPath = results && results.video;
        if (!videoPath || !fs.existsSync(videoPath)) return;

        const croppedPath = videoPath.replace(/\.mp4$/, ".cropped.mp4");
        try {
          execFileSync(
            "ffmpeg",
            [
              "-y",
              "-i",
              videoPath,
              "-filter:v",
              `crop=iw-${VIDEO_CROP_LEFT_PX}:ih:${VIDEO_CROP_LEFT_PX}:0`,
              "-c:a",
              "copy",
              croppedPath,
            ],
            { stdio: "ignore" }
          );
          fs.rmSync(videoPath);
          fs.renameSync(croppedPath, videoPath);
          console.log(`[cypress] Vidéo recadrée (-${VIDEO_CROP_LEFT_PX}px à gauche) : ${videoPath}`);
        } catch (err) {
          console.warn(
            "[cypress] Recadrage ffmpeg impossible (ffmpeg installé ? `brew install ffmpeg`) — vidéo brute conservée :",
            err.message
          );
        }
      });

      // Nettoie les postes [E2E] créés pendant le run, une fois tous les specs
      // terminés (succès ou échec) — évite d'accumuler des lignes de test dans
      // les données réelles. Nécessite `make dev` lancé (docker compose).
      on("after:run", () => {
        try {
          execFileSync(
            "docker",
            [
              "compose",
              "-f",
              "docker-compose.dev.yml",
              "exec",
              "-T",
              "app",
              "python",
              "manage.py",
              "cleanup_e2e_data",
            ],
            { stdio: "inherit" }
          );
        } catch (err) {
          console.warn(
            "[cypress] Nettoyage des données E2E impossible (docker compose lancé ? `make dev`) :",
            err.message
          );
        }
      });

      return config;
    },
  },
});
