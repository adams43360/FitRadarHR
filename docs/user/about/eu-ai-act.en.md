# The EU AI Act and recruitment

!!! danger "This is not legal advice"
    This page is for informational purposes. The timeline and content of the EU AI Act have changed several times since its adoption and may change again. For any compliance decision affecting your organization, consult a lawyer or your DPO — FitRadarHR does not replace that advice.

## Why recruitment is affected

The **EU AI Act** (Regulation (EU) 2024/1689) classifies AI systems used for recruitment and HR management — candidate selection, promotion, task allocation, contract termination, performance evaluation — as **"high-risk"** (Annex III). It is this classification, not the fact of using this or that specific tool, that triggers the regulation's heaviest obligations.

FitRadarHR was designed anticipating this classification from the start — see the "never an automated decision score" rule in the [product principles](../index.md) — rather than as a reaction to a regulatory deadline.

## Where the timeline stands (as of August 7, 2026)

The timeline has changed recently. Originally, the "high-risk" obligations were due to apply from **August 2, 2026**. A simplification package (the *Digital Omnibus AI*) changed this timeline:

- Provisional political agreement between the European Parliament and the Council: **May 7, 2026**
- Formal adoption by the European Parliament: **June 16, 2026**
- Final approval by the Council of the EU: **June 29, 2026**, followed by publication in the EU Official Journal

Result: the "high-risk" obligations for stand-alone systems (including HR/recruitment tools) are **postponed to December 2, 2027**. For high-risk AI systems embedded in a broader product, the deadline is **August 2, 2028**.

!!! info "This postponement doesn't change what's already in force"
    The postponement specifically concerns the obligations tied to the "high-risk" classification (Annex III). It does not suspend the GDPR, French labor law, or the AI practice prohibitions already in force since February 2025 (for example emotion recognition in the workplace, banned as soon as the regulation entered into application).

## What already applies, independently of the AI Act

Two legal frameworks already govern tool-assisted recruitment today, without waiting for December 2027:

**GDPR, Article 22** — everyone has the right not to be subject to a decision based solely on automated processing that produces legal effects or significantly affects them, when no human intervention takes place. This is the structural reason FitRadarHR never displays a decision score ("recommended" / "not recommended"): see [privacy and GDPR](privacy.md).

**French Labor Code, Articles L.1221-8 and L.1221-9** — a candidate must be informed, before their implementation, of the techniques and methods used for their evaluation and recruitment, including when automated processing contributes to it. The results obtained must remain confidential and the candidate may request communication of the information concerning them.

## What the "high-risk" classification will require from 2027

Once the obligations apply, a high-risk AI system used for recruitment will notably need to have:

- a risk management system documented across the tool's entire lifecycle,
- effective **human oversight** — the person using the tool must be able to understand its limits and not rely on it blindly,
- **traceability** (logging) of usage,
- technical documentation and a conformity assessment before being placed on the market,
- clear information for the people concerned.

## How FitRadarHR fits into this framework

These principles aren't new to the product — they overlap with design choices already made:

| Upcoming obligation (Annex III) | What FitRadarHR already does |
|---|---|
| Documented human oversight | No automated decision score — the product informs, it never decides |
| Traceability of usage | Immutable audit log of consultations, exports and link sends |
| Minimization / consent | Explicit timestamped consent before the questionnaire, right to erasure |
| Scientifically validated instrument | Big Five questionnaire (IPIP), never a CV analysis nor an unvalidated typology — see [Big Five vs MBTI](big-five-vs-mbti.md) |

This doesn't exempt your organization from its own compliance analysis: the "high-risk" classification is about the use *you* make of the tool in your recruitment process, not just the tool itself.

## Sources

- [Digital Omnibus AI — postponement of high-risk obligations to December 2027 (Gibson Dunn)](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/){ target="_blank" }
- [EU Nears Approval of Agreement to Delay Rules for AI Use in Employment Decisions (Ogletree Deakins)](https://ogletree.com/insights-resources/blog-posts/eu-nears-approval-of-agreement-to-delay-rules-for-ai-use-in-employment-decisions/){ target="_blank" }
- [HR Tools and Artificial Intelligence: Europe Delays High-Risk Obligations to December 2027 (actuIA)](https://www.actuia.com/en/news/hr-tools-and-artificial-intelligence-europe-delays-high-risk-obligations-to-december-2027/){ target="_blank" }
- Regulation (EU) 2024/1689 (EU AI Act), Annex III
- French Labor Code, Articles L.1221-8 and L.1221-9
- Regulation (EU) 2016/679 (GDPR), Article 22
