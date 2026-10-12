import { afterEach, expect, it, vi } from "vitest";
import { sessionHeaders } from "./api-session";
import { GET } from "../app/api/orbit/connections/route";

vi.mock("next/headers", () => ({ cookies: async () => ({ get: () => ({ value: "expired-or-other-organization" }) }) }));
afterEach(() => vi.unstubAllGlobals());

it("uses the public workspace even when an old account cookie exists", async () => {
  const headers = await sessionHeaders({ "content-type": "application/json" });
  expect(headers.get("authorization")).toBe("Bearer sentinel-public-dashboard");
  expect(headers.get("content-type")).toBe("application/json");
});

it("loads Orbit connections without forwarding a browser session", async () => {
  vi.stubGlobal("fetch", async (_input: string, init: RequestInit) => {
    if (new Headers(init.headers).get("authorization") !== "Bearer sentinel-public-dashboard") {
      return Response.json({ detail: "Sign in required" }, { status: 401 });
    }
    return Response.json([]);
  });
  const response = await GET();
  expect(response.status).toBe(200);
  expect(await response.json()).toEqual([]);
});
