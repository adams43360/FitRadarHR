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
- [ ] Le formulaire demande : titre du poste, description (libre), département (optionnel)
- [ ] Le poste est créé avec le statut "actif"
- [ ] Le titre et la description sont saisissables en FR et EN (champs bilingues)
- [ ] Le poste apparaît dans la liste des postes de l'organisation

---

### US-E2-02 — Définition du profil Big Five cible d'un poste
**En tant que** RH, **je veux** définir manuellement le niveau attendu sur chacune des 5 dimensions OCEAN pour un poste donné, **afin de** paramétrer le calcul de fit poste.

**Critères d'acceptation :**
- [ ] Pour chaque dimension (O, C, E, A, N), le RH positionne un niveau cible sur une échelle (ex. 1–100 ou bas/moyen/haut)
- [ ] Un texte explicatif de chaque dimension est affiché pour aider le RH à calibrer
- [ ] Il est possible de définir une fourchette (min/max) plutôt qu'une valeur unique
- [ ] Le profil cible peut être modifié après création
- [ ] Un poste sans profil cible défini est clairement signalé comme "non configuré"

---

### US-E2-03 — Consultation et gestion de la liste des postes
**En tant que** RH, **je veux** consulter, modifier et archiver mes postes, **afin de** maintenir mon référentiel à jour.

**Critères d'acceptation :**
- [ ] La liste des postes affiche : titre, statut (actif/archivé), date de création, profil cible configuré (oui/non)
- [ ] Un poste archivé n'apparaît plus dans les listes de sélection mais ses données sont conservées
- [ ] La liste est filtrable par statut

---

## E3 — Gestion des équipes

### US-E3-01 — Création d'une équipe
**En tant que** Manager, **je veux** créer une équipe avec un nom, **afin de** regrouper les collaborateurs qui y appartiennent.

**Critères d'acceptation :**
- [ ] Le formulaire demande : nom de l'équipe, description (optionnel), Manager responsable (pré-rempli avec l'utilisateur connecté)
- [ ] L'équipe est rattachée à l'organisation du tenant
- [ ] Le RH peut aussi créer des équipes et les assigner à un Manager

---

### US-E3-02 — Ajout de membres à une équipe
**En tant que** Manager, **je veux** ajouter des collaborateurs existants dans le système à mon équipe, **afin de** constituer la composition de l'équipe.

**Critères d'acceptation :**
- [ ] Un collaborateur peut être ajouté à une équipe s'il a complété le questionnaire Big Five (son profil est disponible)
- [ ] Il est possible d'ajouter un collaborateur sans profil (en attente de questionnaire)
- [ ] Un collaborateur peut appartenir à plusieurs équipes
- [ ] L'ajout est tracé (qui a ajouté, quand)

---

### US-E3-03 — Retrait ou déplacement d'un membre
**En tant que** Manager, **je veux** retirer un collaborateur de mon équipe ou le déplacer vers une autre, **afin de** refléter les évolutions organisationnelles.

**Critères d'acceptation :**
- [ ] Le retrait n'efface pas le profil Big Five du collaborateur
- [ ] L'historique de l'appartenance à l'équipe est conservé (à des fins de traçabilité)
- [ ] Le RH peut effectuer ces actions sur toutes les équipes

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
- [ ] Le lien est généré depuis une fiche candidat/collaborateur ou depuis la fiche d'un poste
- [ ] L'email est envoyé par FitRadarHR et mentionne : qui envoie (organisation), l'objet du questionnaire, la durée estimée
- [ ] Le lien est unique, sécurisé et horodaté (expiration configurable, défaut : 30 jours)
- [ ] Le RH/Manager peut voir le statut du questionnaire : envoyé / en cours / complété
- [ ] Il est possible de renvoyer le lien si non utilisé

---

### US-E4-02 — Accès et passation du questionnaire
**En tant que** Candidat/Collaborateur, **je veux** accéder au questionnaire via mon lien et le compléter, **afin que** mon profil Big Five soit calculé.

**Critères d'acceptation :**
- [ ] La page du questionnaire est accessible sans création de compte
- [ ] Le questionnaire utilise les items IPIP (domaine public) — version 50 ou 100 items (à arbitrer, cf. question ouverte dans le cadrage)
- [ ] Les questions sont présentées par blocs (pas toutes d'un coup) avec une barre de progression
- [ ] Le résultat est calculé côté serveur dès la soumission finale
- [ ] L'accès expire après complétion ou après la date limite du lien

---

### US-E4-03 — Choix de la langue du questionnaire
**En tant que** Candidat/Collaborateur, **je veux** choisir la langue du questionnaire (FR ou EN), **afin de** répondre dans ma langue préférée.

**Critères d'acceptation :**
- [ ] Le choix de langue est proposé dès l'arrivée sur la page du questionnaire (avant le début)
- [ ] L'ensemble des questions, consignes et libellés d'échelle sont traduits
- [ ] Le choix de langue n'affecte pas le calcul du score (même items traduits)

---

### US-E4-04 — Reprise du questionnaire interrompu
**En tant que** Candidat/Collaborateur, **je veux** pouvoir interrompre et reprendre le questionnaire là où je m'étais arrêté, **afin de** ne pas avoir à tout recommencer si je suis interrompu.

**Critères d'acceptation :**
- [ ] La progression est sauvegardée automatiquement (toutes les X questions ou à chaque page)
- [ ] En revenant sur le lien, le candidat reprend depuis sa dernière réponse enregistrée
- [ ] La session de reprise est liée au même lien sécurisé (pas de compte nécessaire)

---

### US-E4-05 — Notification de complétion
**En tant que** RH ou Manager, **je veux** être notifié quand un questionnaire est complété, **afin de** consulter les résultats rapidement.

**Critères d'acceptation :**
- [ ] Une notification email est envoyée à l'émetteur du lien dès la soumission du questionnaire
- [ ] La notification contient un lien direct vers le rapport ou le profil du candidat/collaborateur
- [ ] La notification est également visible dans l'interface (centre de notifications)

---

## E5 — Moteur de calcul de Fit

### US-E5-01 — Calcul du Fit Poste
**En tant que** RH, **je veux** que le système calcule automatiquement le fit entre le profil Big Five d'une personne et le profil cible d'un poste, **afin d'** obtenir une aide à la décision structurée.

**Critères d'acceptation :**
- [ ] Le calcul est déclenché automatiquement dès que le questionnaire est complété ET que le poste a un profil cible défini
- [ ] Le calcul produit un score de proximité par dimension (pas un score unique agrégé opaque)
- [ ] Le calcul est reproductible et tracé (version de l'algorithme, date, inputs)
- [ ] Aucun score unique ne remplace la lecture humaine — le rapport associé (E6) contextualise toujours

---

### US-E5-02 — Calcul du Fit Équipe
**En tant que** Manager, **je veux** que le système calcule le fit entre le profil d'une personne et le profil agrégé de mon équipe, **afin d'** anticiper comment elle s'intégrera dans la dynamique existante.

**Critères d'acceptation :**
- [ ] Le profil agrégé de l'équipe est calculé à partir de l'ensemble des profils complétés des membres actuels
- [ ] Le calcul est disponible dès qu'au moins 2 membres de l'équipe ont un profil complété
- [ ] Le calcul est recalculé automatiquement si la composition de l'équipe change

---

### US-E5-03 — Complémentarité plutôt que similarité
**En tant que** Manager, **je veux** que le calcul de fit équipe prenne en compte la complémentarité des profils et pas uniquement la similarité, **afin d'** éviter les biais d'homogénéité et les angles morts collectifs.

**Critères d'acceptation :**
- [ ] Le rapport de fit équipe indique explicitement les dimensions où l'équipe est homogène (et les risques associés)
- [ ] Une personne très différente du profil dominant peut être présentée comme "complémentaire" plutôt que "non-fit"
- [ ] La logique de complémentarité est expliquée en langage clair dans la restitution

---

## E6 — Rapports & restitution

### US-E6-01 — Visualisation du profil Big Five individuel
**En tant que** RH ou Manager, **je veux** visualiser le profil Big Five d'une personne sous forme de radar chart (pentagonal), **afin de** saisir rapidement ses caractéristiques sur les 5 dimensions.

**Critères d'acceptation :**
- [ ] Le radar chart affiche les 5 dimensions OCEAN avec le score de la personne
- [ ] Les libellés des dimensions sont affichés en clair (pas seulement les initiales)
- [ ] Le graphique est accompagné d'une brève description textuelle de chaque dimension et de ce qu'implique le niveau obtenu
- [ ] Le rapport est affiché en FR ou EN selon la langue de l'utilisateur connecté

---

### US-E6-02 — Rapport de Fit Poste
**En tant que** RH, **je veux** consulter un rapport de fit poste qui présente les alignements, points de vigilance et de complémentarité en langage clair, **afin d'** enrichir mon analyse avant décision.

**Critères d'acceptation :**
- [ ] Le rapport superpose sur un même radar le profil de la personne et le profil cible du poste
- [ ] Les zones d'alignement et d'écart sont identifiées visuellement et expliquées en texte
- [ ] Le rapport ne contient pas de formulation du type "recommandé" / "non recommandé"
- [ ] Une mention explicite rappelle que ce rapport est une aide à la décision, à interpréter avec le contexte humain
- [ ] Le rapport est horodaté et identifie clairement la personne, le poste, et la version du calcul

---

### US-E6-03 — Rapport de Fit Équipe
**En tant que** Manager, **je veux** visualiser le profil agrégé de mon équipe et le résultat de fit d'un nouvel arrivant potentiel, **afin d'** anticiper la dynamique et les complémentarités.

**Critères d'acceptation :**
- [ ] Le rapport affiche le profil agrégé de l'équipe (radar) et le profil de la personne évaluée en superposition
- [ ] Les zones de complémentarité et les zones d'homogénéité forte de l'équipe sont mises en évidence
- [ ] Le rapport inclut une lecture qualitative (ex. grille Watzlawick en couche explicative, pas comme score)
- [ ] La même mention "aide à la décision" est présente

---

### US-E6-04 — Export du rapport en PDF
**En tant que** RH ou Manager, **je veux** exporter un rapport au format PDF, **afin de** le partager avec d'autres parties prenantes (direction, équipe RH élargie).

**Critères d'acceptation :**
- [ ] Le PDF généré contient le radar chart, les textes d'analyse et la mention "aide à la décision"
- [ ] Le PDF est nommé automatiquement (ex. `fit-poste_nom-candidat_nom-poste_date.pdf`)
- [ ] L'export est tracé (qui a exporté, quand)
- [ ] Le PDF ne contient pas d'informations non visibles dans l'interface (pas de données brutes cachées)

---

## E7 — Internationalisation

### US-E7-01 — Choix de la langue de l'interface
**En tant qu'** utilisateur connecté (RH ou Manager), **je veux** choisir la langue de l'interface (FR ou EN), **afin d'** utiliser le produit dans ma langue.

**Critères d'acceptation :**
- [ ] La langue est sélectionnable dans les préférences du compte
- [ ] Le choix est persistant (mémorisé entre les sessions)
- [ ] Toutes les pages et tous les composants sont traduits (pas de texte en dur dans le code)
- [ ] Les dates, nombres et formats régionaux s'adaptent à la langue choisie

---

### US-E7-02 — Langue des communications vers les candidats
**En tant que** RH, **je veux** que les emails et le questionnaire envoyés à un candidat soient dans sa langue, **afin d'** offrir une expérience adaptée.

**Critères d'acceptation :**
- [ ] Lors de l'envoi du lien questionnaire, le RH peut choisir la langue de l'email (FR ou EN)
- [ ] Le candidat peut modifier la langue au moment d'ouvrir le questionnaire (indépendamment de la langue de l'email)
- [ ] Les emails système (invitation, notification de complétion) respectent la langue de l'utilisateur destinataire

---

## E8 — Conformité & gouvernance

### US-E8-01 — Consentement explicite avant questionnaire
**En tant que** Candidat/Collaborateur, **je veux** donner mon consentement explicite avant de répondre au questionnaire, **afin d'** exercer mon droit à l'information sur l'usage de mes données.

**Critères d'acceptation :**
- [ ] Une page de consentement précède le questionnaire : elle explique l'objet de la collecte, qui aura accès aux résultats, la durée de conservation, et les droits de la personne
- [ ] Le consentement est recueilli par une case à cocher active (pas pré-cochée)
- [ ] Le consentement est horodaté et conservé (preuve en cas de demande RGPD)
- [ ] Sans consentement, le questionnaire ne peut pas être démarré
- [ ] La page de consentement est disponible en FR et EN

---

### US-E8-02 — Droit à l'effacement des données (RGPD)
**En tant que** Candidat/Collaborateur, **je veux** pouvoir demander la suppression de mes données de personnalité, **afin d'** exercer mon droit à l'effacement.

**Critères d'acceptation :**
- [ ] Une procédure de demande de suppression est accessible (ex. via un lien dans les emails reçus ou une page publique)
- [ ] La demande déclenche une suppression (ou anonymisation irréversible) du profil Big Five et des scores associés
- [ ] La confirmation de suppression est envoyée par email sous 72h
- [ ] La suppression est tracée pour preuve de conformité (sans conserver les données supprimées)
- [ ] Le RH est notifié si des rapports liés à ce profil sont affectés

---

### US-E8-03 — Traçabilité des actions (EU AI Act)
**En tant que** RH, **je veux** que toutes les actions liées aux évaluations soient tracées automatiquement, **afin de** garantir la traçabilité requise par l'EU AI Act et de pouvoir répondre à une contestation.

**Critères d'acceptation :**
- [ ] Chaque rapport de fit (poste ou équipe) est associé à un log : qui l'a consulté, quand, pour quelle personne/poste/équipe
- [ ] Chaque export PDF est tracé
- [ ] La version de l'algorithme de calcul utilisée est consignée dans chaque rapport
- [ ] Les logs ne peuvent pas être supprimés par un utilisateur standard (conservation minimale réglementaire)
- [ ] Un RH ADMIN peut consulter les logs de son organisation

---

### US-E8-04 — Mention obligatoire de supervision humaine
**En tant que** RH ou Manager, **je veux** que chaque rapport rappelle explicitement qu'une supervision humaine est obligatoire, **afin de** documenter que le système ne décide jamais seul.

**Critères d'acceptation :**
- [ ] Une mention standardisée est présente sur chaque rapport (interface et PDF) : le texte exact est à valider mais doit préciser que le rapport est une aide à la décision et ne constitue pas une décision de recrutement ou de mobilité
- [ ] Cette mention n'est pas masquable ni supprimable par l'utilisateur
- [ ] La mention est traduite en FR et EN

---

*Dernière mise à jour : 2026-06-30*
