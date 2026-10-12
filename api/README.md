# Independent Railway API

Build from the repository root using `api/Dockerfile` (set `RAILWAY_DOCKERFILE_PATH=api/Dockerfile`). The Docker image includes the SQL migrations and synthetic challenge CSVs.

Configure the API service:

- `DATABASE_URL=${{Postgres.DATABASE_URL}}` referencing your own Postgres service
- `ORBIT_CATALOG=postgres`
- `CORS_ORIGINS=https://getsentinel.us,http://localhost:3000`
- Pre-deploy command: `python -m app.migrate --seed-demo`
- Health-check path: `/health`
- Root directory: `/`
- Dockerfile path: `api/Dockerfile`
- Watch paths: `/api/**`, `/database/**`, `/SPOT_KnightHacks_Challenge_Kit Part One/02_DATA/**`

The migration runner records applied files in `sentinel.schema_migrations`. It is intended for a new database managed by this runner. Challenge data is seeded only when no kit missions exist in the demo workspace. Deployments do not replace existing inspection data.

Without `DATABASE_URL`, the API retains the original Databricks Lakebase connection configuration.

Once `/dataset?source=kit` and `/queue` return data using `Authorization: Bearer sentinel-public-dashboard`, set Vercel's production `SENTINEL_API_URL` to the generated API domain and redeploy the frontend. No login cookie is needed.

Chat needs a separately deployed agent and `SENTINEL_AGENT_URL`. The agent requires your own model-provider credentials; deploying this API and database alone does not enable AI chat.

## Current deployment

- Railway project: `discerning-abundance` (`00f7812c-1335-4990-83b0-be2d0932f206`)
- API service: `api` (`51cd3398-1268-4866-aa2e-eaf33322d049`)
- API URL: https://api-production-09f5.up.railway.app
- Database service: `Postgres` (private networking; no public database endpoint)
- Source: `gabrieljcontreras/SENTINEL`, branch `main`

Service build, pre-deploy, and health-check settings are stored in Railway. The current Railway API rejects legacy `railway.json` configuration, so no such file is required. The API's Dockerfile remains in this repository.
