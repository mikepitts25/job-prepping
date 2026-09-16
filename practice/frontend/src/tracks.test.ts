/**
 * Tests for the track view logic.
 *
 * Read these before the implementation. The edge cases they pin -- malformed
 * records, empty results, tie-breaking, staleness at the boundary -- are the
 * ones worth naming out loud in an interview.
 */

import { describe, expect, it } from 'vitest';

import type { Track } from './track.model';
import {
  ValidationError,
  ageSeconds,
  countByAffiliation,
  filterTracks,
  formatAltitude,
  isStale,
  parseTrack,
  parseTracks,
  sortForDisplay,
} from './tracks';

function track(overrides: Partial<Track> = {}): Track {
  return {
    trackId: 'T-001',
    affiliation: 'unknown',
    altitudeFt: 10_000,
    speedKt: 320,
    confidence: 0.9,
    lastSeen: '2026-09-16T12:00:00Z',
    ...overrides,
  };
}

describe('parseTrack', () => {
  const valid = {
    trackId: 'T-001',
    affiliation: 'hostile',
    altitudeFt: 12000,
    speedKt: 450,
    confidence: 0.8,
    lastSeen: '2026-09-16T12:00:00Z',
  };

  it('accepts a well-formed record', () => {
    expect(parseTrack(valid)).toEqual(valid);
  });

  it('trims surrounding whitespace on strings', () => {
    expect(parseTrack({ ...valid, trackId: '  T-001  ' }).trackId).toBe('T-001');
  });

  it.each([
    ['missing trackId', { ...valid, trackId: undefined }],
    ['empty trackId', { ...valid, trackId: '   ' }],
    ['numeric trackId', { ...valid, trackId: 42 }],
    ['unknown affiliation', { ...valid, affiliation: 'banana' }],
    ['altitude as a string', { ...valid, altitudeFt: '12000' }],
    ['altitude NaN', { ...valid, altitudeFt: Number.NaN }],
    ['confidence above one', { ...valid, confidence: 1.5 }],
    ['confidence below zero', { ...valid, confidence: -0.1 }],
  ])('rejects %s', (_name, raw) => {
    expect(() => parseTrack(raw as Record<string, unknown>)).toThrow(ValidationError);
  });

  it('names the offending field in the error', () => {
    expect(() => parseTrack({ ...valid, confidence: 9 })).toThrow(/confidence/);
  });
});

describe('parseTracks', () => {
  it('keeps the good records and collects the errors', () => {
    const { tracks, errors } = parseTracks([
      { trackId: 'A', affiliation: 'friend', altitudeFt: 1, speedKt: 1, confidence: 1, lastSeen: 'x' },
      { trackId: 'B', affiliation: 'nonsense', altitudeFt: 1, speedKt: 1, confidence: 1, lastSeen: 'x' },
    ]);
    expect(tracks).toHaveLength(1);
    expect(errors).toHaveLength(1);
    expect(errors[0].field).toBe('affiliation');
  });

  it('handles an empty payload', () => {
    expect(parseTracks([])).toEqual({ tracks: [], errors: [] });
  });
});

describe('filterTracks', () => {
  const tracks = [
    track({ trackId: 'T-001', affiliation: 'hostile', confidence: 0.9 }),
    track({ trackId: 'T-002', affiliation: 'friend', confidence: 0.4 }),
    track({ trackId: 'X-003', affiliation: 'hostile', confidence: 0.6 }),
  ];

  it('returns everything by default', () => {
    expect(filterTracks(tracks)).toHaveLength(3);
  });

  it('filters by affiliation', () => {
    expect(filterTracks(tracks, { affiliation: 'hostile' }).map((t) => t.trackId))
      .toEqual(['T-001', 'X-003']);
  });

  it('filters by minimum confidence', () => {
    expect(filterTracks(tracks, { minConfidence: 0.5 })).toHaveLength(2);
  });

  it('searches the track id case-insensitively', () => {
    expect(filterTracks(tracks, { search: 't-00' }).map((t) => t.trackId))
      .toEqual(['T-001', 'T-002']);
  });

  it('combines filters', () => {
    expect(filterTracks(tracks, { affiliation: 'hostile', minConfidence: 0.8 }))
      .toHaveLength(1);
  });

  it('does not mutate the input', () => {
    const original = [...tracks];
    filterTracks(tracks, { affiliation: 'friend' });
    expect(tracks).toEqual(original);
  });

  it('can return nothing', () => {
    expect(filterTracks(tracks, { minConfidence: 0.99 })).toEqual([]);
  });
});

describe('sortForDisplay', () => {
  it('puts hostile first and friend last', () => {
    const sorted = sortForDisplay([
      track({ trackId: 'A', affiliation: 'friend' }),
      track({ trackId: 'B', affiliation: 'hostile' }),
      track({ trackId: 'C', affiliation: 'neutral' }),
      track({ trackId: 'D', affiliation: 'unknown' }),
    ]);
    expect(sorted.map((t) => t.affiliation))
      .toEqual(['hostile', 'unknown', 'neutral', 'friend']);
  });

  it('breaks affiliation ties by altitude, highest first', () => {
    const sorted = sortForDisplay([
      track({ trackId: 'LOW', affiliation: 'hostile', altitudeFt: 1000 }),
      track({ trackId: 'HIGH', affiliation: 'hostile', altitudeFt: 30000 }),
    ]);
    expect(sorted.map((t) => t.trackId)).toEqual(['HIGH', 'LOW']);
  });

  it('breaks remaining ties by track id, so the order is stable', () => {
    const sorted = sortForDisplay([
      track({ trackId: 'T-B', affiliation: 'hostile', altitudeFt: 1000 }),
      track({ trackId: 'T-A', affiliation: 'hostile', altitudeFt: 1000 }),
    ]);
    expect(sorted.map((t) => t.trackId)).toEqual(['T-A', 'T-B']);
  });

  it('does not mutate the input', () => {
    const input = [track({ trackId: 'B' }), track({ trackId: 'A' })];
    const before = [...input];
    sortForDisplay(input);
    expect(input).toEqual(before);
  });
});

describe('countByAffiliation', () => {
  it('counts each affiliation, including the zeroes', () => {
    const counts = countByAffiliation([
      track({ affiliation: 'hostile' }),
      track({ affiliation: 'hostile' }),
      track({ affiliation: 'friend' }),
    ]);
    expect(counts).toEqual({ hostile: 2, friend: 1, neutral: 0, unknown: 0 });
  });

  it('reports all zeroes for no tracks', () => {
    const counts = countByAffiliation([]);
    expect(Object.values(counts).every((n) => n === 0)).toBe(true);
  });
});

describe('formatAltitude', () => {
  it.each<[number, string]>([
    [1000, '1,000 ft'],
    [0, '0 ft'],
    [12345.6, '12,346 ft'],
  ])('formats %d as %s', (input, expected) => {
    expect(formatAltitude(input)).toBe(expected);
  });
});

describe('staleness', () => {
  const now = new Date('2026-09-16T12:00:30Z');

  it('measures age against the supplied clock, not the real one', () => {
    expect(ageSeconds(track({ lastSeen: '2026-09-16T12:00:00Z' }), now)).toBe(30);
  });

  it('is not stale exactly at the threshold', () => {
    expect(isStale(track({ lastSeen: '2026-09-16T12:00:00Z' }), now, 30)).toBe(false);
  });

  it('is stale one second past the threshold', () => {
    expect(isStale(track({ lastSeen: '2026-09-16T11:59:59Z' }), now, 30)).toBe(true);
  });
});
