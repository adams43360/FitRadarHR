# User Stories — FitRadarHR

> Document vivant. Les user stories sont ajoutées au fil de l'eau, rattachées aux epics définis dans `00-cadrage.md`.
> Format : *En tant que [rôle], je veux [besoin], afin de [valeur]*
> Critères d'acceptation explicites pour chaque story.

---

## Rôles de référence

| Code | Rôle |
|---|---|
| `RH` | Responsable RH / Talent Acquisition (contexte B2B) |
| `MGR` | Manager (contexte B2B ou B2C) |
| `SOLO` | Utilisateur individuel B2C (consultant, manager indépendant, petit collectif) |
| `CAND` | Candidat ou collaborateur en mobilité (passation questionnaire) |
| `ADMIN` | Administrateur de l'organisation (peut être le RH en V1) |

> **Modèle économique** : FitRadarHR est gratuit et libre de droits. L'inscription est en self-service, sans abonnement ni paiement.

---

## E1 — Authentification & organisations

### US-E1-00 — Choix du parcours à l'inscription
**En tant que** visiteur, **je veux** choisir entre un compte "Pour mon entreprise" (B2B) et un compte "Usage personnel" (B2C) dès la page d'inscription, **afin d'** accéder au parcours adapté à ma situation.

**Critères d'acceptation :**
- [ ] La page d'accueil/inscription présente deux parcours distincts, avec une courte description de chacun
- [ ] Le choix oriente vers des formulaires et des espaces de travail différents
- [ ] Aucun choix n'est verrouillé derrière un paiement — les deux sont gratuits
- [ ] La langue (FR/EN) est sélectionnable avant même ce choix

---

### US-E1-01 — Création d'un compte organisation (B2B)
**En tant que** RH, **je veux** créer un espace organisation (nom, email, mot de passe), **afin de** démarrer l'utilisation de FitRadarHR pour ma structure.

**Critères d'acceptation :**
- [ ] Le formulaire demande : nom de l'organisation, prénom/nom du RH, email professionnel, mot de passe (confirmation)
- [ ] Un email de vérification est envoyé avant activation du compte
- [ ] Un tenant isolé est créé pour cette organisation (aucune donnée partagée avec d'autres orgs)
- [ ] L'interface est disponible en FR et EN dès l'inscription (choix de langue sur la page)
- [ ] Pas de moyen de paiement demandé — l'activation est immédiate après vérification email

---

### US-E1-01B — Création d'un compte individuel (B2C)
**En tant que** utilisateur solo (consultant, manager indépendant, responsable de petite équipe), **je veux** créer un compte personnel sans avoir à déclarer d'organisation formelle, **afin de** pouvoir utiliser FitRadarHR pour moi-même ou ma petite équipe.

**Critères d'acceptation :**
- [ ] Le formulaire demande uniquement : prénom/nom, email, mot de passe (confirmation) — pas de nom d'entreprise obligatoire
- [ ] Un espace de travail personnel est créé automatiquement (nom par défaut : "Espace de [prénom]", modifiable)
- [ ] L'utilisateur B2C dispose des mêmes fonctionnalités que le B2B en V1 (postes, équipes, questionnaires, rapports)
- [ ] Un email de vérification est envoyé avant activation
- [ ] Pas de moyen de paiement demandé

---

### US-E1-02 — Connexion utilisateur
**En tant que** tout utilisateur inscrit (B2B ou B2C), **je veux** me connecter avec mon email et mon mot de passe, **afin d'** accéder à mon espace sécurisé.

**Critères d'acceptation :**
- [ ] La page de connexion est accessible sans compte et affiche le choix de langue
- [ ] En cas d'erreur de mot de passe, un message générique est affiché (pas d'information sur l'existence du compte)
- [ ] Une option "mot de passe oublié" permet une réinitialisation par email
- [ ] Après connexion, l'utilisateur est redirigé vers son tableau de bord

---

### US-E1-03 — Invitation d'un Manager
**En tant que** RH, **je veux** inviter un Manager par email à rejoindre mon espace organisation, **afin qu'**il puisse accéder aux fonctionnalités liées à ses équipes.

**Critères d'acceptation :**
- [ ] Le RH saisit l'email du Manager et lui attribue le rôle "Manager"
- [ ] Le Manager reçoit un email d'invitation avec un lien sécurisé (expirant sous 72h)
- [ ] Le Manager crée son mot de passe via ce lien et accède directement à l'espace
- [ ] Le RH peut voir la liste des membres de l'organisation et leur statut (invité / actif)

---

### US-E1-05 — Connexion SSO via l'IdP OIDC de l'organisation
**En tant que** RH (ADMIN), **je veux** configurer le fournisseur d'identité (Keycloak ou tout IdP compatible OIDC) de mon organisation, **afin que** mes utilisateurs puissent se connecter avec leurs identifiants d'entreprise plutôt qu'un mot de passe FitRadarHR dédié.

**Critères d'acceptation :**
- [ ] Un RH accède à un écran de configuration SSO depuis les paramètres de son organisation
- [ ] Le formulaire demande : nom d'affichage (ex. "Acme Corp SSO"), identifiant de connexion (`login_slug`, unique, utilisé dans l'URL de connexion), URL d'émetteur OIDC (`issuer_url`), `client_id`, `client_secret`
- [ ] Le `client_secret` n'est jamais ré-affiché après saisie (write-only) — seule sa présence est confirmée à l'écran
- [ ] Un bascule "Activé / Désactivé" permet de couper le SSO sans perdre la configuration
- [ ] Chaque organisation configure **son propre** IdP — aucune configuration n'est partagée entre organisations (isolation multi-tenant stricte)
- [ ] Le SSO **s'ajoute** à la connexion par email/mot de passe existante — il ne la remplace jamais automatiquement, pour éviter un verrouillage en cas de panne de l'IdP
- [ ] La page de connexion propose un lien "Se connecter via votre organisation" qui demande le `login_slug` puis redirige vers l'IdP correspondant
- [ ] À la première connexion réussie via SSO, un compte `User` est automatiquement créé (provisioning JIT) et rattaché à l'organisation propriétaire de la configuration SSO utilisée, avec le rôle par défaut Manager (modifiable ensuite par un RH)
- [ ] Si un compte avec le même email existe déjà dans l'organisation, la connexion SSO se rattache à ce compte plutôt que d'en créer un doublon
- [ ] Toute erreur de configuration (IdP injoignable, identifiants invalides) affiche un message clair, sans exposer de détail technique sensible
- [ ] L'écran de configuration est disponible en FR et EN

---

### US-E1-07 — Plan gratuit et abonnement
**En tant que** RH (ADMIN), **je veux** utiliser FitRadarHR gratuitement sans limite de durée tant que mon organisation reste petite, puis souscrire un abonnement simple, **afin de** continuer sans limite au-delà du seuil du plan gratuit.

> Révision 2026-07-06 : le modèle initial (essai gratuit de 14 jours puis quotas)
> est remplacé par un plan gratuit permanent — plus simple à comprendre, sans
> pression artificielle à la conversion.

**Critères d'acceptation :**
- [ ] Toute organisation (B2B et B2C) démarre sur le plan gratuit, sans limite de durée ni compte à rebours
- [ ] Un seuil unique et cumulé s'applique au plan gratuit : 25 personnes au total dans l'organisation. La création de postes et l'envoi de questionnaires restent libres (le nombre de personnes capture implicitement le volume de questionnaires) — jamais un blocage total, seul l'ajout de nouvelles personnes est limité, les données existantes restent consultables
- [ ] Un seul plan payant, sans palier — 39 €/mois — un abonnement actif lève la limite
- [ ] Un écran `/settings/billing/` (RH only) affiche le statut (plan gratuit avec compteur de personnes sur le seuil, ou abonnement actif avec date de renouvellement), avec un bouton "S'abonner" (redirection Stripe Checkout) et "Gérer mon abonnement" (Stripe Customer Portal) une fois client Stripe créé
- [ ] Le prix facturé est configuré côté Stripe (`STRIPE_PRICE_ID`) — le prix affiché sur l'écran abonnement doit rester cohérent avec lui ; si Stripe n'est pas configuré, l'écran affiche "configuration requise" au lieu de planter
- [ ] Le statut d'abonnement est synchronisé via un webhook Stripe (paiement réussi, renouvellement, échec de paiement, résiliation), jamais interrogé en direct à chaque page vue
- [ ] L'organisation de démonstration publique n'est jamais soumise aux quotas
- [ ] Le contenu est disponible en FR/EN/ES/DE

---

### US-E1-06 — API publique en lecture seule (clé API par organisation)
**En tant que** RH (ADMIN), **je veux** générer une clé API pour mon organisation, **afin de** connecter un outil tiers (ATS, SIRH) à FitRadarHR en lecture seule, sans intervention manuelle.

**Critères d'acceptation :**
- [ ] Un RH accède à un écran `/settings/api/` listant les clés API de son organisation (nom, préfixe, date de création, dernière utilisation, statut actif/révoquée)
- [ ] La génération d'une clé affiche sa valeur en clair **une seule fois** ; elle n'est plus jamais ré-affichable ensuite (seul le préfixe non secret reste visible dans la liste)
- [ ] La révocation d'une clé est immédiate et définitive (pas de suppression physique de l'enregistrement, pour garder une trace d'audit) ; une clé révoquée est immédiatement rejetée par l'API
- [ ] Chaque clé est scopée à **une seule organisation** — isolation multi-tenant stricte, aucune fuite cross-tenant possible via l'API
- [ ] L'authentification se fait via l'en-tête `Authorization: Api-Key <clé>` ; toute requête sans en-tête valide reçoit une erreur 401 explicite
- [ ] L'API est strictement **en lecture seule** (GET uniquement) — aucun endpoint ne permet de créer, modifier ou supprimer une donnée
- [ ] Le périmètre exposé couvre : postes et équipes (métadonnées), personnes et statut de leur questionnaire, résultats de fit (poste et équipe)
- [ ] **Les scores Big Five bruts (O/C/E/A/N d'un `BigFiveProfile`) ne sont jamais exposés par l'API**, sous quelque forme que ce soit — seul un indicateur booléen "profil renseigné" et les résultats de fit dérivés sont disponibles, par choix produit RGPD (minimisation des données transmises à des tiers)
- [ ] Les listes sont paginées (page/page_size), avec une taille de page maximale pour éviter les exports de masse non maîtrisés
- [ ] L'écran de gestion des clés est réservé aux RH (403 pour un Manager, redirection login pour un anonyme)

---

### US-E1-08 — Refonte du menu de navigation principal (catégories + sous-menus déroulants)
**En tant que** utilisateur connecté (RH, Manager, Admin), **je veux** un menu principal organisé en catégories avec des sous-menus déroulants, **afin de** naviguer sans que les liens ne chevauchent le logo à mesure que de nouvelles fonctionnalités s'ajoutent.

**Contexte :** le menu s'est allongé au fil des livraisons (Départements, Postes, Équipes, Questionnaires, Rapports, Analytics, Audit, Membres, SSO, API, Abonnement…) au point de chevaucher le logo sur écran standard. Regrouper les entrées par catégorie avec un menu déroulant limite la casse à chaque nouvel ajout.

**Critères d'acceptation :**
- [x] Les liens du menu sont regroupés en catégories principales cohérentes (Organisation → Départements/Équipes/Membres ; Recrutement → Postes/Questionnaires/Rapports ; Pilotage → Analytics/Audit ; Paramètres → SSO/API/Abonnement), plutôt qu'une liste plate
- [x] Chaque catégorie principale ouvre un sous-menu déroulant au clic, sans rechargement de page
- [x] Aucun chevauchement avec le logo sur les largeurs d'écran usuelles (desktop et tablette) ; comportement mobile prévu (bouton burger + panneau empilé sous le seuil `lg`)
- [x] La visibilité des entrées reste conditionnée aux mêmes règles de permission qu'aujourd'hui (ex. Abonnement/SSO/API réservés RH) — une catégorie sans item visible est masquée entièrement (cas Manager : Pilotage/Paramètres disparaissent)
- [x] Tous les libellés passent par le système i18n existant (FR/EN/ES/DE), aucun texte en dur
- [x] Le menu déroulant est utilisable au clavier (Échap pour fermer, clic extérieur, boutons nativement focusables/activables)
- [x] Aucune régression sur les liens existants (mêmes URLs, mêmes noms de routes) — source unique des liens via le template tag `navbar_categories`, partagée desktop/mobile

**Livré (2026-07-04)** : template tag `apps/accounts/templatetags/navbar_tags.py::navbar_categories`,
partiel `templates/partials/_navbar_menu.html` (rendu desktop dropdown / mobile empilé),
`templates/partials/navbar.html` réécrit. 261 tests toujours au vert.

---

### US-E1-04 — Gestion des rôles
**En tant que** RH (ADMIN), **je veux** modifier le rôle d'un utilisateur ou le désactiver, **afin de** maintenir un contrôle sur les accès.

**Critères d'acceptation :**
- [ ] Le RH peut changer le rôle d'un utilisateur (RH ↔ Manager)
- [ ] Le RH peut désactiver un compte (l'utilisateur ne peut plus se connecter, ses données sont conservées)
- [ ] Un utilisateur désactivé ne peut pas se reconnecter
- [ ] L'action de désactivation est tracée (qui, quand)

---

## E2 — Gestion des postes

### US-E2-01 — Création d'un poste
**En tant que** RH, **je veux** créer un poste avec un titre et une description, **afin de** pouvoir lui associer un profil Big Five cible.

**Critères d'acceptation :**
- [x] Le formulaire demande : titre du poste, description (libre), département (FK, optionnel), équipe cible (FK, optionnelle)
- [x] Le poste est créé avec le statut "actif"
- [x] Le titre et la description sont saisissables en FR et EN (champs bilingues)
- [x] Le poste apparaît dans la liste des postes de l'organisation

---

### US-E2-04 — Rattachement d'un poste à un département et une équipe
**En tant que** RH ou Manager, **je veux** rattacher un poste à un département et optionnellement à une équipe, **afin de** structurer l'organisation et de comparer le fit d'un candidat avec l'équipe cible.

**Critères d'acceptation :**
- [x] Un modèle `Department` existe (nom FR/EN, description, archivage) avec CRUD complet accessible aux RH
- [x] Une équipe peut être rattachée à un département (champ optionnel)
- [x] Un poste est rattaché à un département (optionnel, FK) et peut l'être à une équipe spécifique (FK optionnelle)
- [x] La migration de données convertit les anciennes valeurs texte `department` en objets `Department`
- [x] La fiche poste affiche le département et l'équipe cible dans l'en-tête
- [x] Le rapport de profil affiche le fit équipe cible en retrait sous le fit poste correspondant
- [x] Toutes les strings UI passent par i18n (FR/EN)
- [x] Le filtre multi-tenant s'applique sur `Department` via `OrgQuerySet`

---

### US-E2-05 — Classement des personnes par Fit sur la fiche poste
**En tant que** RH ou Manager, **je veux** voir sur la fiche d'un poste la liste des personnes ayant passé le questionnaire, classées par score de Fit décroissant, **afin d'** identifier immédiatement les meilleurs profils pour ce poste.

**Critères d'acceptation :**
- [x] La section "Classement" apparaît uniquement si le poste a un profil Big Five défini et qu'au moins un résultat de fit existe
- [x] Les personnes sont triées par `overall_fit` décroissant (meilleur en premier)
- [x] Chaque ligne affiche : rang, nom complet, type (Candidat/Collaborateur), barre de progression, score coloré (vert ≥ 80 %, amber 60–79 %, rouge < 60 %), lien vers le rapport détaillé
- [x] Trois boutons de filtre : Tous / Candidats / Collaborateurs (paramètre GET `?type=`)
- [x] Toutes les strings UI passent par i18n

---

### US-E2-02 — Définition du profil Big Five cible d'un poste
**En tant que** RH, **je veux** définir manuellement le niveau attendu sur chacune des 5 dimensions OCEAN pour un poste donné, **afin de** paramétrer le calcul de fit poste.

**Critères d'acceptation :**
- [x] Pour chaque dimension (O, C, E, A, N), le RH positionne un niveau cible sur une échelle (1–100)
- [x] Un texte explicatif de chaque dimension est affiché pour aider le RH à calibrer
- [x] Il est possible de définir une fourchette (min/max) plutôt qu'une valeur unique
- [x] Le profil cible peut être modifié après création
- [x] Un poste sans profil cible défini est clairement signalé comme "non configuré"

---

### US-E2-03 — Consultation et gestion de la liste des postes
**En tant que** RH, **je veux** consulter, modifier et archiver mes postes, **afin de** maintenir mon référentiel à jour.

**Critères d'acceptation :**
- [x] La liste des postes affiche : titre, statut (actif/archivé), date de création, profil cible configuré (oui/non)
- [x] Un poste archivé n'apparaît plus dans les listes de sélection mais ses données sont conservées
- [x] La liste est filtrable par statut

---

## E3 — Gestion des équipes

### US-E3-01 — Création d'une équipe
**En tant que** Manager, **je veux** créer une équipe avec un nom, **afin de** regrouper les collaborateurs qui y appartiennent.

**Critères d'acceptation :**
- [x] Le formulaire demande : nom de l'équipe, département (FK optionnelle), description (optionnel), Manager responsable (pré-rempli avec l'utilisateur connecté)
- [x] L'équipe est rattachée à l'organisation du tenant
- [x] Le RH peut aussi créer des équipes et les assigner à un Manager

---

### US-E3-02 — Ajout de membres à une équipe
**En tant que** Manager, **je veux** ajouter des collaborateurs existants dans le système à mon équipe, **afin de** constituer la composition de l'équipe.

**Critères d'acceptation :**
- [x] Un collaborateur peut être ajouté à une équipe s'il a complété le questionnaire Big Five (son profil est disponible)
- [x] Il est possible d'ajouter un collaborateur sans profil (en attente de questionnaire)
- [x] Un collaborateur peut appartenir à plusieurs équipes
- [x] L'ajout est tracé (qui a ajouté, quand)

---

### US-E3-03 — Retrait ou déplacement d'un membre
**En tant que** Manager, **je veux** retirer un collaborateur de mon équipe ou le déplacer vers une autre, **afin de** refléter les évolutions organisationnelles.

**Critères d'acceptation :**
- [x] Le retrait n'efface pas le profil Big Five du collaborateur
- [x] L'historique de l'appartenance à l'équipe est conservé (date left_at, traçabilité)
- [x] Le RH peut effectuer ces actions sur toutes les équipes

---

### US-E3-04 — Vue d'ensemble des équipes (RH)
**En tant que** RH, **je veux** accéder à la liste de toutes les équipes de l'organisation, **afin d'** avoir une vision globale de la structure.

**Critères d'acceptation :**
- [ ] La liste affiche : nom de l'équipe, Manager responsable, nombre de membres, nombre de membres avec profil complet
- [ ] Le RH peut consulter le détail de n'importe quelle équipe

---

## E4 — Questionnaire Big Five

### US-E4-01 — Envoi du lien de questionnaire
**En tant que** RH ou Manager, **je veux** envoyer un lien de questionnaire à un candidat ou collaborateur par email, **afin qu'**il puisse le compléter sans avoir de compte FitRadarHR.

**Critères d'acceptation :**
- [x] Le lien est généré depuis une fiche candidat/collaborateur ou depuis la fiche d'un poste
- [x] L'email est envoyé par FitRadarHR et mentionne : qui envoie (organisation), l'objet du questionnaire, la durée estimée
- [x] Le lien est unique, sécurisé et horodaté (expiration : 7 jours)
- [x] Le RH/Manager peut voir le statut du questionnaire : envoyé / en cours / complété
- [x] Il est possible de renvoyer le lien si non utilisé
- [x] Le formulaire d'envoi permet de saisir prénom + nom pour créer la personne à la volée si elle n'existe pas encore
- [x] Le formulaire permet d'associer un poste (optionnel) au questionnaire pour contextualiser le fit
- [x] Le poste associé est affiché dans le dashboard questionnaires

---

### US-E4-02 — Accès et passation du questionnaire
**En tant que** Candidat/Collaborateur, **je veux** accéder au questionnaire via mon lien et le compléter, **afin que** mon profil Big Five soit calculé.

**Critères d'acceptation :**
- [x] La page du questionnaire est accessible sans création de compte
- [x] Le questionnaire utilise les items IPIP (domaine public) — version 50 items (v1.0)
- [x] Les questions sont présentées par blocs de 10 avec une barre de progression
- [x] Le résultat est calculé côté serveur dès la soumission finale
- [x] L'accès expire après complétion ou après la date limite du lien

---

### US-E4-03 — Choix de la langue du questionnaire
**En tant que** Candidat/Collaborateur, **je veux** choisir la langue du questionnaire (FR ou EN), **afin de** répondre dans ma langue préférée.

**Critères d'acceptation :**
- [x] Le choix de langue est proposé dès l'arrivée sur la page du questionnaire (avant le début)
- [x] L'ensemble des questions, consignes et libellés d'échelle sont traduits (FR/EN)
- [x] Le choix de langue n'affecte pas le calcul du score (même items traduits)

---

### US-E4-04 — Reprise du questionnaire interrompu
**En tant que** Candidat/Collaborateur, **je veux** pouvoir interrompre et reprendre le questionnaire là où je m'étais arrêté, **afin de** ne pas avoir à tout recommencer si je suis interrompu.

**Critères d'acceptation :**
- [x] La progression est sauvegardée automatiquement à chaque page
- [x] En revenant sur le lien, le candidat reprend depuis sa dernière réponse enregistrée
- [x] La session de reprise est liée au même lien sécurisé (pas de compte nécessaire)

---

### US-E4-05 — Notification de complétion
**En tant que** RH ou Manager, **je veux** être notifié quand un questionnaire est complété, **afin de** consulter les résultats rapidement.

**Critères d'acceptation :**
- [x] Une notification email est envoyée à l'émetteur du lien dès la soumission du questionnaire
- [x] La notification contient un lien direct vers le rapport ou le profil du candidat/collaborateur
- [ ] La notification est également visible dans l'interface (centre de notifications) — reporté V2

---

## E5 — Moteur de calcul de Fit

### US-E5-01 — Calcul du Fit Poste
**En tant que** RH, **je veux** que le système calcule automatiquement le fit entre le profil Big Five d'une personne et le profil cible d'un poste, **afin d'** obtenir une aide à la décision structurée.

**Critères d'acceptation :**
- [x] Le calcul est déclenché automatiquement dès que le questionnaire est complété ET que le poste a un profil cible défini
- [x] Le calcul produit un score de proximité par dimension (pas un score unique agrégé opaque)
- [x] Le calcul est reproductible et tracé (version de l'algorithme v1.0, date, inputs)
- [x] Aucun score unique ne remplace la lecture humaine — le rapport associé (E6) contextualise toujours

---

### US-E5-02 — Calcul du Fit Équipe
**En tant que** Manager, **je veux** que le système calcule le fit entre le profil d'une personne et le profil agrégé de mon équipe, **afin d'** anticiper comment elle s'intégrera dans la dynamique existante.

**Critères d'acceptation :**
- [x] Le profil agrégé de l'équipe est calculé à partir de l'ensemble des profils complétés des membres actuels
- [x] Le calcul est disponible dès qu'au moins 1 autre membre de l'équipe a un profil complété
- [x] Le calcul est recalculé automatiquement à chaque complétion de questionnaire

---

### US-E5-03 — Complémentarité plutôt que similarité
**En tant que** Manager, **je veux** que le calcul de fit équipe prenne en compte la complémentarité des profils et pas uniquement la similarité, **afin d'** éviter les biais d'homogénéité et les angles morts collectifs.

**Critères d'acceptation :**
- [x] Le rapport de fit équipe indique explicitement les dimensions où l'équipe est homogène (signal complementarity)
- [x] Une personne très différente du profil dominant peut être présentée comme "complémentaire" plutôt que "non-fit"
- [x] La logique de complémentarité est expliquée en langage clair dans la restitution (E6)

---

## E6 — Rapports & restitution

### US-E6-01 — Visualisation du profil Big Five individuel
**En tant que** RH ou Manager, **je veux** visualiser le profil Big Five d'une personne sous forme de radar chart (pentagonal), **afin de** saisir rapidement ses caractéristiques sur les 5 dimensions.

**Critères d'acceptation :**
- [x] Le radar chart affiche les 5 dimensions OCEAN avec le score de la personne
- [x] Les libellés des dimensions sont affichés en clair (pas seulement les initiales)
- [x] Le graphique est accompagné de barres de score par dimension
- [x] Le rapport est affiché en FR ou EN selon la langue de l'utilisateur connecté

---

### US-E6-02 — Rapport de Fit Poste
**En tant que** RH, **je veux** consulter un rapport de fit poste qui présente les alignements, points de vigilance et de complémentarité en langage clair, **afin d'** enrichir mon analyse avant décision.

**Critères d'acceptation :**
- [x] Le rapport superpose sur un même radar le profil de la personne et le profil cible du poste
- [ ] Les zones d'alignement et d'écart sont identifiées visuellement et expliquées en texte
- [x] Le rapport ne contient pas de formulation du type "recommandé" / "non recommandé"
- [x] Une mention explicite rappelle que ce rapport est une aide à la décision, à interpréter avec le contexte humain
- [x] Le rapport est horodaté et identifie clairement la personne, le poste, et la version du calcul

---

### US-E6-03 — Rapport de Fit Équipe
**En tant que** Manager, **je veux** visualiser le profil agrégé de mon équipe et le résultat de fit d'un nouvel arrivant potentiel, **afin d'** anticiper la dynamique et les complémentarités.

**Critères d'acceptation :**
- [x] Le rapport affiche le profil agrégé de l'équipe (radar) et le profil de la personne évaluée en superposition
- [ ] Les zones de complémentarité et les zones d'homogénéité forte de l'équipe sont mises en évidence
- [x] Le rapport inclut les signaux de complémentarité par dimension (similar / different / complementary)
- [ ] La même mention "aide à la décision" est présente

---

### US-E6-04 — Export du rapport en PDF
**En tant que** RH ou Manager, **je veux** exporter un rapport au format PDF, **afin de** le partager avec d'autres parties prenantes (direction, équipe RH élargie).

**Critères d'acceptation :**
- [x] Le PDF généré contient le radar chart, les textes d'analyse et la mention "aide à la décision"
- [x] Le PDF est nommé automatiquement (ex. `fit-poste_nom-candidat_nom-poste_date.pdf`)
- [x] L'export est tracé (qui a exporté, quand)
- [x] Le PDF ne contient pas d'informations non visibles dans l'interface (pas de données brutes cachées)

---

### US-E6-05 — Infobulles d'aide sur les dimensions OCEAN
**En tant que** RH ou Manager, **je veux** comprendre la signification de chaque dimension OCEAN en passant la souris sur son libellé, **afin de** lire les rapports sans expertise psychométrique préalable.

**Critères d'acceptation :**
- [x] Chaque libellé de dimension (Ouverture, Conscienciosité, Extraversion, Agréabilité, Neuroticisme) affiche une infobulle au survol
- [x] L'infobulle décrit en une ou deux phrases ce qu'implique un score élevé et un score faible
- [x] Les infobulles sont disponibles sur toutes les pages de rapport (profil individuel, Fit Poste, Fit Équipe)
- [x] Les infobulles sont disponibles en FR et EN selon la langue de l'interface
- [x] Les infobulles n'apparaissent pas dans les exports PDF (pas de JS dans WeasyPrint)

---

### US-E6-06 — Points à approfondir en entretien
**En tant que** RH ou Manager, **je veux** voir sur les rapports de Fit une section identifiant les dimensions hors fourchette ou à fort écart, avec des suggestions de questions à explorer, **afin d'** enrichir ma préparation d'entretien sans que l'outil ne produise de verdict.**

**Critères d'acceptation :**
- [x] La section n'apparaît que s'il y a au moins une dimension hors plage (Fit Poste) ou à signal notable (Fit Équipe)
- [x] Le contenu est formulé en termes de questions à explorer, jamais de jugements ou de recommandations
- [x] Un disclaimer explicite rappelle que ces observations ne sont pas des verdicts
- [x] Les messages sont spécifiques à chaque dimension et au sens de l'écart (score trop haut / trop bas / complémentaire / différent)
- [x] La section apparaît également dans les exports PDF (Fit Poste et Fit Équipe)
- [x] Le contenu est disponible en FR et EN

---

### US-E6-07 — Fit inversé : postes recommandés pour une personne
**En tant que** RH ou Manager, **je veux**, à partir du profil d'une personne, voir un classement des postes actifs qui lui correspondent le mieux, **afin de** repérer des opportunités de mobilité interne sans avoir à parcourir poste par poste.

**Critères d'acceptation :**
- [x] Un lien "Voir le classement complet" est disponible depuis la section Fit Postes du profil individuel, ainsi qu'un accès direct depuis la liste des rapports
- [x] Le classement liste tous les postes actifs ayant un profil cible, triés par fit décroissant, avec un filtre optionnel par département
- [x] Aucun nouveau calcul de fit n'est introduit : la vue s'appuie sur les `PositionFitResult` déjà calculés par le moteur de fit (E5)
- [x] Un export PDF est disponible, cohérent avec les autres rapports
- [x] La consultation et l'export sont tracés dans le journal d'audit (EU AI Act)
- [x] Le disclaimer "aide à la décision, pas une recommandation" est rappelé sur la page comme sur l'export
- [x] Le contenu est disponible en FR/EN/ES/DE

---

## E7 — Internationalisation

### US-E7-01 — Choix de la langue de l'interface
**En tant qu'** utilisateur connecté (RH ou Manager), **je veux** choisir la langue de l'interface (FR, EN, ES ou DE), **afin d'** utiliser le produit dans ma langue.

**Critères d'acceptation :**
- [x] La langue est sélectionnable dans le sélecteur de la navbar (FR/EN/ES/DE)
- [x] Le choix est persistant (cookie de langue Django, mémorisé entre les sessions)
- [x] Toutes les pages et tous les composants sont traduits (pas de texte en dur dans le code — `{% trans %}`/`gettext_lazy` partout, `locale/{en,es,de}/LC_MESSAGES/django.po`)
- [ ] Les dates, nombres et formats régionaux s'adaptent à la langue choisie (non fait — dates toujours au format `d/m/Y`)

---

### US-E7-02 — Langue des communications vers les candidats
**En tant que** RH, **je veux** que les emails et le questionnaire envoyés à un candidat soient dans sa langue, **afin d'** offrir une expérience adaptée.

**Critères d'acceptation :**
- [x] Lors de l'envoi du lien questionnaire, le RH peut choisir la langue de l'email parmi FR/EN/ES/DE
- [x] Le candidat peut modifier la langue au moment d'ouvrir le questionnaire (indépendamment de la langue de l'email)
- [x] Les emails système (invitation, relance, notification de complétion) respectent la langue de l'utilisateur destinataire

---

### US-E7-03 — Parité complète ES/DE, questionnaire IPIP inclus
**En tant que** RH ou Candidat, **je veux** pouvoir utiliser FitRadarHR — interface *et* questionnaire Big Five — en espagnol et en allemand, **afin de** couvrir des organisations et candidats hispanophones et germanophones sans dégrader la rigueur scientifique de l'instrument.

**Contexte** : contrairement à une simple traduction d'interface, le questionnaire IPIP est
l'instrument qui *qualifie* le profil (règle non négociable #1 du cadrage) — sa traduction devait
donc être sourcée sur des traductions IPIP officielles plutôt que traduite librement.

**Critères d'acceptation :**
- [x] Les 100 items IPIP ont une traduction allemande sourcée sur la traduction officielle
  IPIP 100 items (Streib & Wiedmaier, 2001, Universität Bielefeld) — couverture 100/100
- [x] Les 100 items IPIP ont une traduction espagnole : sourcée sur la traduction officielle
  IPIP 50 items (de Oliveira et al., 2013, ACM TOCHI) pour les 50 premiers items officiels,
  complétée par une traduction maison pour les 50 items d'extension (pas de source officielle
  publiée à ce jour) — limite documentée dans `docs/user/about/big-five.md` et
  `docs/product/translations-ipip.md`
- [x] Les échelles de réponse (Likert 1-5) sont traduites en DE/ES (`SCALE_DE`/`SCALE_ES`)
- [x] Les contenus de rapport (libellés de dimension, infobulles, "points à approfondir")
  sont disponibles en DE/ES, pas seulement l'UI de navigation
- [x] `QuestionnaireLink.Language`, `Organization.Language` et `User.Language` proposent
  les 4 langues
- [x] Le catalogue UI complet (478 chaînes) est traduit en DE et en ES
- [x] Tests : couverture des traductions IPIP (aucun item DE/ES identique au FR/EN — garde-fou
  anti-oubli), scoring indépendant de la langue, rendu des pages de passation en DE/ES,
  couverture du catalogue UI

---

## E8 — Conformité & gouvernance

### US-E8-01 — Consentement explicite avant questionnaire
**En tant que** Candidat/Collaborateur, **je veux** donner mon consentement explicite avant de répondre au questionnaire, **afin d'** exercer mon droit à l'information sur l'usage de mes données.

**Critères d'acceptation :**
- [x] Une page de consentement précède le questionnaire : elle explique l'objet de la collecte, qui aura accès aux résultats, la durée de conservation, et les droits de la personne
- [x] Le consentement est recueilli par une case à cocher active (pas pré-cochée)
- [x] Le consentement est horodaté et conservé (preuve en cas de demande RGPD)
- [x] Sans consentement, le questionnaire ne peut pas être démarré
- [x] La page de consentement est disponible en FR, EN, ES et DE

---

### US-E8-02 — Droit à l'effacement des données (RGPD)
**En tant que** Candidat/Collaborateur, **je veux** pouvoir demander la suppression de mes données de personnalité, **afin d'** exercer mon droit à l'effacement.

**Critères d'acceptation :**
- [x] Une procédure d'anonymisation est accessible au RH depuis la liste des personnes (bouton 🔒)
- [x] La demande déclenche une anonymisation irréversible (prénom, nom, email remplacés)
- [ ] La confirmation de suppression est envoyée par email sous 72h *(V2)*
- [x] La suppression est tracée dans l'AuditLog (preuve de conformité)
- [x] Les profils Big Five et résultats de fit sont conservés de façon anonymisée (traçabilité)

---

### US-E8-03 — Traçabilité des actions (EU AI Act)
**En tant que** RH, **je veux** que toutes les actions liées aux évaluations soient tracées automatiquement, **afin de** garantir la traçabilité requise par l'EU AI Act et de pouvoir répondre à une contestation.

**Critères d'acceptation :**
- [x] Chaque rapport de fit (poste ou équipe) est associé à un log : qui l'a consulté, quand, pour quelle personne/poste/équipe
- [x] Chaque export PDF est tracé
- [x] La version de l'algorithme de calcul utilisée est consignée dans chaque rapport
- [x] Les logs ne peuvent pas être supprimés par un utilisateur standard (AuditLog immuable)
- [x] Un RH peut consulter les logs de son organisation (journal d'audit paginé)

---

### US-E8-04 — Mention obligatoire de supervision humaine
**En tant que** RH ou Manager, **je veux** que chaque rapport rappelle explicitement qu'une supervision humaine est obligatoire, **afin de** documenter que le système ne décide jamais seul.

**Critères d'acceptation :**
- [x] Une mention standardisée est présente sur chaque rapport (interface et PDF) précisant que le rapport est une aide à la décision, pas une décision de recrutement ou de mobilité
- [x] Cette mention n'est pas masquable ni supprimable par l'utilisateur
- [x] La mention est traduite en FR et EN

---

## Améliorations UX

### US-UX-01 — Pré-remplissage email dans le formulaire d'envoi de questionnaire
**En tant que** RH, **je veux** que le formulaire d'envoi soit pré-rempli avec l'email de la personne quand j'arrive depuis sa fiche, **afin de** gagner du temps et éviter les erreurs de saisie.

**Critères d'acceptation :**
- [x] Le lien "Envoyer questionnaire" dans la liste des personnes passe l'email en paramètre GET
- [x] Le formulaire pré-remplit le champ email si ce paramètre est présent
- [x] Les emails avec caractères spéciaux (ex. `+`) sont correctement encodés dans l'URL

---

### US-UX-02 — Autocomplétion dans le champ "Ajouter un membre"
**En tant que** RH ou Manager, **je veux** une autocomplétion sur le champ d'ajout de membre dans une équipe, **afin de** trouver rapidement une personne par nom, prénom ou email.

**Critères d'acceptation :**
- [x] La recherche s'active après 2 caractères saisis
- [x] Les suggestions filtrent par nom, prénom ou email (insensible à la casse)
- [x] Seules les personnes non encore membres actifs de l'équipe apparaissent
- [x] Cliquer sur une suggestion remplit le champ et soumet le formulaire
- [x] L'endpoint est protégé (login requis, filtre org)

---

### US-UX-03 — Modification des données d'une personne
**En tant que** RH ou Manager, **je veux** pouvoir modifier les données d'une personne, **afin de** corriger une erreur ou mettre à jour ses informations.

**Critères d'acceptation :**
- [x] Bouton "Modifier" sur chaque ligne de la liste des personnes
- [x] Formulaire pré-rempli avec les données actuelles
- [x] L'email doit être unique dans l'org, sauf pour la personne en cours de modification
- [x] Redirection vers la liste après sauvegarde avec message de confirmation

---

### US-UX-04 — Déduplication du dashboard questionnaires
**En tant que** RH, **je veux** voir uniquement le lien le plus récent par personne dans le dashboard questionnaires, **afin de** ne pas avoir de doublons après un renvoi ou une mise à jour de profil.

**Critères d'acceptation :**
- [x] Une seule ligne par personne dans le dashboard (le lien le plus récent)
- [x] Les anciens liens sont conservés en base mais non affichés
- [x] Le compteur "en attente" sur le dashboard principal applique la même déduplication

---

### US-UX-05 — Gestion des départements
**En tant que** RH, **je veux** créer et gérer des départements, **afin de** structurer l'organisation et de rattacher postes et équipes à une entité organisationnelle.

**Critères d'acceptation :**
- [x] CRUD complet : liste, création, détail, modification, archivage
- [x] Un département a un nom FR, un nom EN (optionnel) et une description
- [x] Lien "Départements" dans la navbar pour les RH
- [x] La fiche département liste les postes et équipes rattachés
- [x] Lien rapide "Créer un nouveau département" depuis les formulaires poste et équipe

---

*Dernière mise à jour : 2026-07-03*
