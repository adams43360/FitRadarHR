/**
 * Parcours : création d'un poste sur TeamFit (epic E2 — gestion des postes).
 *
 * Reproduit les 6 étapes du parcours manuel de référence transmis par Damien :
 * connexion → "+ Nouveau poste" → formulaire poste → profil Big Five cible →
 * retrouver le poste via le menu "Recrutement / Postes" → détail depuis "Voir".
 *
 * Prérequis :
 * - .env rempli (TEAMFIT_BASE_URL, TEAMFIT_TEST_EMAIL, TEAMFIT_TEST_PASSWORD)
 * - `make dev` lancé en local (http://localhost:8000)
 *
 * Les noms de cy.maybeScreenshot() sont destinés à être consommés plus tard par une
 * génération de doc utilisateur à partir des captures — ne pas les renommer sans
 * mettre à jour ce process en aval.
 *
 * ⚠️ Pas de nettoyage automatique pour l'instant : le compte de test utilisé est
 * le compte réel de Damien (choix assumé temporairement), donc les postes créés
 * par ce test s'accumulent dans les données réelles. Le titre inclut un timestamp
 * pour rester identifiable et pour que le test reste rejouable sans collision.
 */

function testPositionData() {
  const stamp = Date.now();
  return {
    titleFr: `[E2E] Chargé·e de recrutement ${stamp}`,
    titleEn: `[E2E] Recruitment Officer ${stamp}`,
    descriptionFr: "Poste créé automatiquement par le test E2E Cypress — à ignorer.",
  };
}

describe("Création d'un poste", () => {
  it("permet de créer un poste, définir son profil Big Five cible, et le retrouver dans la liste", () => {
    const data = testPositionData();

    // Étape 1 — connexion, arrivée sur le dashboard
    cy.loginAsTestAccount();
    cy.wait(800);
    cy.maybeScreenshot("01-etape1-connexion-dashboard");
    cy.wait(500);

    // Étape 2 — "+ Nouveau poste"
    cy.get('[data-testid="new-position-button"]').click();
    cy.url().should("include", "/positions/new/");
    cy.wait(500);
    cy.maybeScreenshot("02-etape2-formulaire-nouveau-poste");
    cy.wait(500);

    // Étape 3 — remplir le formulaire, créer le poste
    cy.get('[data-testid="position-title-fr"]').type(data.titleFr, { delay: 40 });
    cy.wait(300);
    cy.get('[data-testid="position-title-en"]').type(data.titleEn, { delay: 40 });
    cy.wait(300);
    cy.get('[data-testid="position-description-fr"]').type(data.descriptionFr, { delay: 20 });
    cy.wait(500);
    cy.maybeScreenshot("03-etape3a-formulaire-poste-rempli");
    cy.wait(500);
    cy.get('[data-testid="create-position-submit"]').click();
    cy.url().should("match", /\/positions\/[0-9a-f-]{36}\/profile\/$/);
    cy.wait(500);
    cy.maybeScreenshot("04-etape3b-poste-cree-arrivee-profil-big-five");
    cy.wait(500);

    // Étape 4 — définir le profil Big Five cible, enregistrer
    cy.setSlider("profile-openness-min", 40);
    cy.setSlider("profile-openness-max", 80);
    cy.wait(200);
    cy.setSlider("profile-conscientiousness-min", 60);
    cy.setSlider("profile-conscientiousness-max", 100);
    cy.wait(200);
    cy.setSlider("profile-extraversion-min", 30);
    cy.setSlider("profile-extraversion-max", 70);
    cy.wait(200);
    cy.setSlider("profile-agreeableness-min", 50);
    cy.setSlider("profile-agreeableness-max", 90);
    cy.wait(200);
    cy.setSlider("profile-neuroticism-min", 0);
    cy.setSlider("profile-neuroticism-max", 40);
    cy.wait(500);
    cy.maybeScreenshot("05-etape4a-profil-big-five-rempli");
    cy.wait(500);
    cy.get('[data-testid="save-profile-submit"]').click();
    cy.url().should("match", /\/positions\/[0-9a-f-]{36}\/$/);
    cy.get('[data-testid="position-title"]').should("contain.text", data.titleFr);
    cy.wait(500);
    cy.maybeScreenshot("06-etape4b-profil-enregistre-detail-poste");
    cy.wait(500);

    // Étape 5 — menu "Recrutement" > "Postes", confirmer que le poste y est
    cy.get('[data-testid="navbar-category-recrutement"]').click();
    cy.wait(400);
    cy.get('[data-testid="navbar-link-postes"]').click();
    cy.url().should("include", "/positions/");
    cy.get(`[data-testid="position-row"][data-position-title="${data.titleFr}"]`).should(
      "be.visible"
    );
    cy.wait(500);
    cy.maybeScreenshot("07-etape5-poste-present-dans-la-liste");
    cy.wait(500);

    // Étape 6 — "Voir" sur la ligne du poste, vérifier le détail
    cy.get(`[data-testid="position-row"][data-position-title="${data.titleFr}"]`)
      .find('[data-testid="position-view-link"]')
      .click();
    cy.get('[data-testid="position-title"]').should("contain.text", data.titleFr);
    cy.contains(data.titleEn).should("be.visible");
    cy.wait(800);
    cy.maybeScreenshot("08-etape6-detail-poste-verification-finale");
    cy.wait(500);
  });
});
