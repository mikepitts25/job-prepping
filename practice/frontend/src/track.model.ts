/** The shape of a track as the API returns it. */

export type Affiliation = 'friend' | 'hostile' | 'neutral' | 'unknown';

export interface Track {
  readonly trackId: string;
  readonly affiliation: Affiliation;
  readonly altitudeFt: number;
  readonly speedKt: number;
  readonly confidence: number;
  /** ISO 8601, UTC. */
  readonly lastSeen: string;
}

/**
 * A raw record straight off the wire, before validation.
 *
 * `unknown` rather than `any` is deliberate: `any` switches type checking off
 * and lets bad data through silently, while `unknown` forces you to prove what
 * a value is before using it. On a system fed by external interfaces, that
 * distinction is the whole point of using TypeScript.
 */
export type RawTrack = Record<string, unknown>;
