# Public roadmap

FitRadarHR's V1 is complete (epics E1–E8 delivered) and **V2 is fully
delivered** (9/9 items). This page also presents candidate ideas for a
**V3**, prioritized using the **RICE** method — in full transparency, like
the rest of the project.

## How to read the RICE score

**RICE = (Reach × Impact × Confidence) / Effort**

- **Reach** — how many users are affected per quarter (scale 1–10)
- **Impact** — effect on the North Star (reports viewed / week): 0.5 = low, 1 = medium, 2 = high, 3 = massive
- **Confidence** — confidence in the estimates: 50% / 80% / 100%
- **Effort** — workload in person-weeks

## V2 prioritization

| # | Feature | Reach | Impact | Conf. | Effort | RICE score | Status |
|---|---|---|---|---|---|---|---|
| 1 | Automatic questionnaire reminders | 8 | 2 | 80% | 1 | **12.8** | ✅ Delivered |
| 2 | Inviting managers into the org | 7 | 2 | 80% | 2 | **5.6** | ✅ Delivered |
| 3 | Comparing candidates for a position | 6 | 2 | 80% | 2 | **4.8** | ✅ Delivered |
| 4 | CSV import of people | 6 | 1 | 100% | 1.5 | **4.0** | ✅ Delivered |
| 5 | Re-take & longitudinal tracking | 5 | 2 | 50% | 2 | **2.5** | ✅ Delivered |
| 6 | Retention cohorts in Analytics | 4 | 1 | 80% | 1.5 | **2.1** | ✅ Delivered |
| 7 | SSO Keycloak / OIDC | 3 | 1 | 80% | 3 | **0.8** | ✅ Delivered |
| 8 | ES / DE translations | 2 | 1 | 80% | 2 | **0.8** | ✅ Delivered |
| 9 | Public API (read-only) | 2 | 1 | 50% | 3 | **0.3** | ✅ Delivered |

## The arguments, item by item

**1. Automatic reminders** — the Analytics funnel shows most of the drop-off
happens between sending the link and starting it. A reminder at D+3 directly
addresses the completion rate, for minimal effort. Best value/effort ratio
on the list.

**2. Inviting managers** — today an org lives with a single HR account most
of the time. Each invited manager is one more consumer of reports: this is
the "referral" lever of the AARRR funnel.

**3. Comparing candidates** — the fit ranking already exists on the position
page; the side-by-side view (overlaid radars, complementarities) is the
natural next step demanded by the recruitment use case. High impact on
report consultation.

**4. CSV import** — onboarding friction: entering 50 employees by hand is
discouraging. Indirect impact on the North Star but maximum confidence
(obvious need).

**5. Re-take** — Big Five profiles evolve slowly but they do evolve; useful
for internal mobility. 50% confidence: the real need still needs to be
validated in discovery.

**6. Retention cohorts** — deepens the Analytics page for mature orgs.
Reserved for already-activated orgs, hence lower reach.

**7. SSO / OIDC** — necessary for larger organizations; lower reach on the
current target (SMBs/scale-ups) but one IdP per organization, additive to
the password (never a replacement), keeps maintenance cost acceptable.
Delivered, not yet validated with a real IdP in production.

**8. ES/DE translations** — full parity, including the IPIP questionnaire,
not just the interface. The German questionnaire is fully sourced from the
official IPIP translation (100/100 items); Spanish is for the short version
(50 items) but the long version introduces an in-house translated area,
for lack of a published official source — see `docs/user/about/big-five.md`.

**9. Public API (read-only)** — real value but not differentiating today.
Delivered with a deliberately restricted scope: positions/teams, people +
questionnaire status, fit results — never raw Big Five profiles (GDPR
minimization). API key authentication per organization.

## V3 prioritization

Items #1 and #2 are delivered; items 3 to 8 remain undecided candidates.

| # | Feature | Reach | Impact | Conf. | Effort | RICE score | Status |
|---|---|---|---|---|---|---|---|
| 1 | Reverse fit — best positions for a person | 5 | 2 | 90% | 1.5 | **6.0** | ✅ Delivered |
| 2 | Monetization (free plan → subscription) | 8 | 3 | 80% | 5 | **3.84** | ✅ Delivered |
| 3 | Mapping a team's gaps | 5 | 2 | 60% | 2 | **3.0** | ✅ Delivered |
| 4 | Candidate/employee portal (access to their profile) | 6 | 2 | 70% | 3 | **2.8** | Candidate |
| 5 | Exportable AI Act compliance dossier | 3 | 2 | 70% | 2 | **2.1** | Candidate |
| 6 | Webhooks (complement to the public API) | 3 | 1 | 70% | 2 | **1.05** | Candidate |
| 7 | Claude MCP — check your activity outside the site | 2 | 1 | 60% | 2 | **0.6** | Candidate |
| 8 | Anonymized cross-organization benchmarks | 4 | 1 | 40% | 4 | **0.4** | Candidate |
| 9 | Native connectors (Workday, BambooHR, Personio…) | 3 | 2 | 30% | 5 | **0.36** | Candidate |

### The arguments, item by item

**1. Reverse fit** — today you start from a position to rank people; the
reverse (starting from a person and seeing which open positions fit them
best) serves internal mobility, without collecting any additional data:
it's a new view on the existing fit engine. Best value/effort ratio on the
list. Delivered: no new calculation, reuses fit results already produced by
the engine (E5).

**2. Monetization** — this is the very reason for the move to the Fair
Source license (FSL-1.1-MIT): Damien explicitly considered a free trial then
a subscription. High reach (potentially touches all orgs eventually) and
strong impact (it's the business model), but significant effort: Stripe
integration, per-plan quotas, billing screens, overage handling. Delivered:
a single paid plan (€39/month, Stripe Checkout + Customer Portal) and a
permanent free plan (single threshold of 25 people — unlimited positions
and questionnaires). The initial 14-day trial model was abandoned in favor
of freemium: simpler to understand, without artificial pressure to convert.

**3. Mapping a team's gaps** — extends the complementarity already
calculated: from a team's aggregate profile, surfacing under-represented
OCEAN dimensions. Stays within the product's scope — presented as avenues
to explore for a recruitment plan, never as a firm recommendation
(consistent with the "never an automated decision score" rule). Delivered:
accessible directly from the team page, without selecting a person — see
`docs/user/reports/team-gaps.md`.

**4. Candidate/employee portal** — today only HR/managers view reports.
Giving the person themselves access to their profile and report reinforces
the "human in the loop" principle and the GDPR access right already
implemented (E8). Medium confidence: requires a new access model for
`Person` records that don't necessarily have a `User` account.

**5. Exportable AI Act compliance dossier** — an export (PDF/JSON) of the
"traceability file" — who viewed what, documented human oversight — for
organizations that need to justify their compliance under the "high-risk"
classification. Directly extends E8, mainly targets more regulated
organizations (lower reach).

**6. Webhooks** — natural complement to the public API (V2 item #9):
notifying a third-party system when a questionnaire is completed or a fit
is recalculated, rather than polling. Useful only for orgs already using
the API, hence restricted reach.

**7. Claude MCP** — expose an MCP server as a complement to the public API
(V2 item #9), to check your FitRadarHR activity directly from Claude
(questionnaire status, fit results, reminders to send) without opening the
site. Technically a thin wrapper around the existing v1 API: same API key
authentication scoped to an organization, same minimization rules (never
raw Big Five scores, only derived results). The point of vigilance isn't
data access but how the model uses it: deliberately narrow and structured
tools (list pending questionnaires, get a position's or team's fit summary)
rather than a single open-ended tool like "ask any question about this
organization," so as not to let the agent drift toward a firm
recommendation — contrary to the "never an automated decision score" rule.
Modest reach (early-adopter public/orgs already comfortable with AI tools),
limited effort by reusing the existing API.

**8. Anonymized benchmarks** — comparing an organization's OCEAN
distribution to an aggregated cross-organization average, opt-in and
anonymized. Real analytical value but low confidence: raises data
governance questions (cross-tenant aggregation, consent) that still need to
be scoped before any development.

**9. Native connectors** — beyond the generic API, pre-built integrations
with specific HRIS/ATS systems would reduce adoption friction. Lowest
confidence of the lot: demand not yet validated by a real customer use
case, high effort (one connector = a project in its own right). To be
reserved if an organization expresses a concrete need.

## What will never be built

See the [anti-metrics](https://github.com/adams43360/FitRadarHR/blob/main/docs/product/metrics.md)
and the project's non-negotiable rules: no CV analysis, no automated
decision score, no scientifically unvalidated typology (MBTI…).

---

*This roadmap is indicative and re-evaluated based on user feedback —
the [feedback widget](../index.md) built into the app directly feeds
this prioritization.*
