import { sessionHeaders } from "../../../../lib/api-session";

export const dynamic = "force-dynamic";

const api = process.env.SENTINEL_API_URL ?? "http://127.0.0.1:8000";

export async function GET() {
  try {
    const response = await fetch(api + "/api/orbit/connections", {
      cache: "no-store",
      headers: await sessionHeaders(),
    });
    return new Response(await response.text(), {
      status: response.status,
      headers: { "content-type": "application/json" },
    });
  } catch {
    return Response.json({ error: "Orbit connections are unavailable" }, { status: 503 });
  }
}

export async function POST(request: Request) {
  try {
    const response = await fetch(api + "/api/orbit/connections", {
      method: "POST",
      headers: await sessionHeaders({ "content-type": "application/json" }),
      body: await request.text(),
    });
    return new Response(await response.text(), {
      status: response.status,
      headers: { "content-type": "application/json" },
    });
  } catch {
    return Response.json({ error: "Orbit connections are unavailable" }, { status: 503 });
  }
}
