import { createApiClient } from "@sentinel/core/api";

// Public workspace selector, not a credential. Browser cookies never change
// which workspace the dashboard accesses.
export async function sessionHeaders(extra?: HeadersInit) {
  const headers = new Headers(extra);
  headers.set("authorization", "Bearer sentinel-public-dashboard");
  return headers;
}

export async function createSessionClient() {
  return createApiClient(process.env.SENTINEL_API_URL ?? "http://127.0.0.1:8000", async (input, init) => {
    const headers = await sessionHeaders(init?.headers);
    return fetch(input, { ...init, headers, cache: "no-store" });
  });
}
