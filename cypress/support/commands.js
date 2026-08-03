/**
 * Commandes partagées des tests E2E TeamFit.
 *
 * Sélecteurs alignés sur les data-testid réellement présents dans les templates
 * Django (voir templates/accounts/login.html, apps/positions/forms.py,
 * templates/positions/*.html, templates/partials/_navbar_menu.html).
 */

Cypress.Commands.add("loginAsTestAccount", () => {
  const email = Cypress.env("TEAMFIT_TEST_EMAIL");
  const password = Cypress.env("TEAMFIT_TEST_PASSWORD");

  if (!email || !password) {
    throw new Error(
      "TEAMFIT_TEST_EMAIL / TEAMFIT_TEST_PASSWORD manquants — vérifier .env à la racine du projet."
    );
  }

  cy.visit("/login/");
  cy.get('[data-testid="login-email"]').type(email);
  cy.get('[data-testid="login-password"]').type(password, { log: false });
  cy.get('[data-testid="login-submit"]').click();
  cy.get('[data-testid="dashboard-page"]').should("be.visible");
  cy.url().should("include", "/dashboard/");
});

/**
 * Positionne un slider <input type="range"> (piloté par Alpine x-model, qui
 * n'écoute que l'événement "input") sur une valeur donnée. cy.type() ne
 * fonctionne pas sur un range — on passe par .invoke('val', ...).
 */
Cypress.Commands.add("setSlider", (testid, value) => {
  cy.get(`[data-testid="${testid}"]`)
    .invoke("val", value)
    .trigger("input")
    .trigger("change");
});

/**
 * cy.screenshot() conditionnel : cy.screenshot() redimensionne brièvement la
 * page pour cadrer la capture, ce qui produit un flash visible (zoom avant/
 * arrière) dans la vidéo. Quand on veut juste une vidéo propre (pas besoin des
 * images pour la doc), on désactive les captures via --env takeScreenshots=false.
 * Par défaut (rien de précisé), les captures restent actives.
 *
 * Les captures sont rangées dans un sous-dossier par langue (fr/, en/, ...)
 * selon --env lang=xx (défaut : fr), pour permettre de générer le guide PDF
 * dans plusieurs langues à partir du même spec — voir switchLanguage ci-dessous.
 */
Cypress.Commands.add("maybeScreenshot", (name) => {
  if (Cypress.env("takeScreenshots") === false) return;
  const lang = Cypress.env("lang") || "fr";
  cy.screenshot(`${lang}/${name}`);
});

/**
 * Bascule la langue de l'interface via le vrai sélecteur du menu (comme le
 * ferait un utilisateur) plutôt qu'en manipulant un cookie directement — le
 * <select> soumet le formulaire vers la vue Django set_language, qui pose un
 * cookie persistant pour la session. Toutes les pages suivantes s'affichent
 * ensuite dans la langue choisie, même sans préfixe /en/ dans l'URL.
 */
Cypress.Commands.add("switchLanguage", (lang) => {
  cy.get('[data-testid="language-select-desktop"]').select(lang);
  cy.wait(500);
});
