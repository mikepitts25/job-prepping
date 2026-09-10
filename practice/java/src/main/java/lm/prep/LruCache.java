package lm.prep;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * A bounded least-recently-used cache.
 *
 * <p>The idiomatic Java answer: {@code LinkedHashMap} in access order, with
 * {@code removeEldestEntry} overridden. Worth knowing because an unbounded
 * cache is one of the standard ways a long-running Java service leaks memory.
 *
 * <p>Not thread-safe. Wrap with {@code Collections.synchronizedMap} or use a
 * purpose-built concurrent cache if several threads share it, and say which you
 * chose and why.
 */
public final class LruCache<K, V> extends LinkedHashMap<K, V> {

    private final int capacity;

    public LruCache(int capacity) {
        super(16, 0.75f, true);   // true == access order, not insertion order
        if (capacity <= 0) {
            throw new IllegalArgumentException("capacity must be positive");
        }
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
