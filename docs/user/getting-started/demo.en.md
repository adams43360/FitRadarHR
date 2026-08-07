# Try the demo

FitRadarHR offers a **public demo environment**: one click is enough to explore
the tool with realistic data, without creating an account.

## Access the demo

On the login page or the home page, click **✨ Try the demo**.
You are immediately logged into the demo account, with the HR Manager role.

!!! info "No sign-up required"
    The demo account has no password: the button is the only way to access it.

## What the demo contains

The environment simulates **Nexatech**, a fictional software company of about a hundred people:

- 6 departments (Engineering, Product & Design, Sales, Customer Success, Finance, HR)
- 10 teams with their members and completed OCEAN profiles
- 9 open positions with target Big Five profiles and fit rankings
- Candidates being evaluated (completed, pending or in-progress questionnaires)
- Position and team fit reports viewable and exportable to PDF

Team profiles are deliberately contrasted (an extraverted sales team,
a highly conscientious finance team…) so that complementarity signals are meaningful.

## Demo environment rules

!!! warning "Fictional data, reset every 24 hours"
    All data is **fictional and deterministic**: it is deleted and recreated
    identically every day. Do not enter any real data in the demo.

In addition, some functions are adapted:

- **No email is sent** from the demo. When you send a questionnaire,
  the completion link is displayed on screen — you can open it yourself to test
  the candidate journey end to end (including GDPR consent).
- **GDPR erasure is disabled** (since the data is fictional and shared between
  all visitors).

## Want to go further?

Create your own free account ([see Create an account](signup.md)) or
[contact us](mailto:contact@fitradarhr.com) for a dedicated test environment for your team.

---

## For administrators (self-hosting)

Demo mode is configured via the environment:

```bash
# .env
DEMO_MODE=True
```

```bash
# Create or reset the demo org
python manage.py seed_demo

# In dev (Docker)
make seed-demo
```

In production, the `demo-reset` service in `docker-compose.yml` replays the seed every 24 hours:

```bash
docker compose -f docker/docker-compose.prod.yml --profile demo up -d
```
