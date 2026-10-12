"use client";

import { useEffect, useState } from "react";
import { PageHeading, Panel } from "../components/ui";

type Session = {
  user: { id: string; email: string; name: string };
  organization: { id: string; name: string };
};

export function UserSettings() {
  return (
    <>
      <PageHeading title="User settings" subtitle="Dashboard access does not require an account." />
      <Panel title="Access">
        <dl className="grid gap-3 p-4 text-sm">
          <Row label="Access" value="Public workspace" />
          <Row label="Sign-in" value="Not required" />
        </dl>
      </Panel>
    </>
  );
}

export function OrganizationSettings() {
  const session = useSession();
  return (
    <>
      <PageHeading
        title="Organization settings"
        subtitle="This organization owns the kit dataset and one Orbit connection."
      />
      <Panel title="Organization">
        <dl className="grid gap-3 p-4 text-sm">
          <Row label="Name" value={session?.organization.name} />
          <Row label="Organization id" value={session?.organization.id} />
        </dl>
      </Panel>
    </>
  );
}

function useSession() {
  const [session, setSession] = useState<Session | null>(null);
  useEffect(() => {
    let active = true;
    void fetch("/api/auth/session")
      .then((response) => (response.ok ? response.json() : null))
      .then((body) => {
        if (active && body?.user && body?.organization) setSession(body);
      })
      .catch(() => undefined);
    return () => {
      active = false;
    };
  }, []);
  return session;
}

function Row({ label, value }: { label: string; value?: string }) {
  return (
    <div>
      <dt className="text-xs text-muted-foreground">{label}</dt>
      <dd className="mt-0.5">{value || "—"}</dd>
    </div>
  );
}
