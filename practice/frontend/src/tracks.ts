/**
 * The logic behind a track list view.
 *
 * None of this touches the DOM or Angular. That is the point: the filtering,
 * sorting, formatting and validation are where the bugs live, and keeping them
 * in plain functions means they can be tested in milliseconds without a
 * browser. The component becomes a thin shell that calls these.
 *
 * "Push the logic out of the component" is the single most useful piece of
 * frontend advice there is, and it is worth saying in an interview.
 */

import type { Affiliation, RawTrack, Track } from './track.model';

const AFFILIATIONS: readonly Affiliation[] = ['friend', 'hostile', 'neutral', 'unknown'];

/** Threat ordering for display: most urgent first. */
const AFFILIATION_RANK: Record<Affiliation, number> = {
  hostile: 0,
  unknown: 1,
  neutral: 2,
  friend: 3,
};

export class ValidationError extends Error {
  constructor(public readonly field: string, message: string) {
    super(`${field}: ${message}`);
    this.name = 'ValidationError';
  }
}

function requireString(raw: RawTrack, field: string): string {
  const value = raw[field];
  if (typeof value !== 'string' || value.trim() === '') {
    throw new ValidationError(field, `expected a non-empty string, got ${JSON.stringify(value)}`);
  }
  return value.trim();
}

function requireNumber(raw: RawTrack, field: string): number {
  const value = raw[field];
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    throw new ValidationError(field, `expected a finite number, got ${JSON.stringify(value)}`);
  }
  return value;
}

/**
 * Turn one untrusted record into a Track, or throw.
 *
 * Validate at the boundary. A malformed record rejected here names the real
 * problem; the same record accepted and rendered produces a blank cell or
 * "NaN ft" on an operator's screen, which is worse than an error because
 * nobody knows it is wrong.
 */
export function parseTrack(raw: RawTrack): Track {
  const affiliation = requireString(raw, 'affiliation');
  if (!AFFILIATIONS.includes(affiliation as Affiliation)) {
    throw new ValidationError('affiliation', `not one of ${AFFILIATIONS.join(', ')}`);
  }

  const confidence = requireNumber(raw, 'confidence');
  if (confidence < 0 || confidence > 1) {
    throw new ValidationError('confidence', `out of range: ${confidence}`);
  }

  return {
    trackId: requireString(raw, 'trackId'),
    affiliation: affiliation as Affiliation,
    altitudeFt: requireNumber(raw, 'altitudeFt'),
    speedKt: requireNumber(raw, 'speedKt'),
    confidence,
    lastSeen: requireString(raw, 'lastSeen'),
  };
}

/**
 * Parse a whole payload, keeping the good records and reporting the bad.
 *
 * One corrupt record must not blank the operator's screen.
 */
export function parseTracks(rawList: readonly RawTrack[]): {
  tracks: Track[];
  errors: ValidationError[];
} {
  const tracks: Track[] = [];
  const errors: ValidationError[] = [];

  for (const raw of rawList) {
    try {
      tracks.push(parseTrack(raw));
    } catch (err) {
      if (err instanceof ValidationError) {
        errors.push(err);
      } else {
        throw err;
      }
    }
  }

  return { tracks, errors };
}

export interface TrackFilter {
  readonly affiliation?: Affiliation | 'all';
  readonly minConfidence?: number;
  readonly search?: string;
}

/** Apply the view's filters. Returns a new array; never mutates the input. */
export function filterTracks(tracks: readonly Track[], filter: TrackFilter = {}): Track[] {
  const { affiliation = 'all', minConfidence = 0, search = '' } = filter;
  const needle = search.trim().toLowerCase();

  return tracks.filter((track) => {
    if (affiliation !== 'all' && track.affiliation !== affiliation) return false;
    if (track.confidence < minConfidence) return false;
    if (needle && !track.trackId.toLowerCase().includes(needle)) return false;
    return true;
  });
}

/**
 * Sort for display: most threatening first, then highest, then by id.
 *
 * The id tiebreak is not decoration. Without it the order of equal rows is
 * unspecified, the list reshuffles on every refresh, and an operator loses
 * their place. Deterministic output is also what makes this testable.
 */
export function sortForDisplay(tracks: readonly Track[]): Track[] {
  return [...tracks].sort((a, b) => {
    const byThreat = AFFILIATION_RANK[a.affiliation] - AFFILIATION_RANK[b.affiliation];
    if (byThreat !== 0) return byThreat;
    const byAltitude = b.altitudeFt - a.altitudeFt;
    if (byAltitude !== 0) return byAltitude;
    return a.trackId.localeCompare(b.trackId);
  });
}

/** Group tracks by affiliation, for a summary panel. */
export function countByAffiliation(tracks: readonly Track[]): Record<Affiliation, number> {
  const counts: Record<Affiliation, number> = {
    friend: 0, hostile: 0, neutral: 0, unknown: 0,
  };
  for (const track of tracks) counts[track.affiliation] += 1;
  return counts;
}

/** Format an altitude for display, with thousands separators. */
export function formatAltitude(altitudeFt: number): string {
  return `${Math.round(altitudeFt).toLocaleString('en-US')} ft`;
}

/**
 * How stale is this track, in seconds, relative to `now`.
 *
 * `now` is a parameter rather than a call to Date.now() inside. That is what
 * makes it testable without waiting, and it is the same discipline as
 * injecting a clock in Python.
 */
export function ageSeconds(track: Track, now: Date): number {
  return (now.getTime() - new Date(track.lastSeen).getTime()) / 1000;
}

/** A track nobody has heard from recently is the failure operators must see. */
export function isStale(track: Track, now: Date, maxAgeSeconds = 30): boolean {
  return ageSeconds(track, now) > maxAgeSeconds;
}
