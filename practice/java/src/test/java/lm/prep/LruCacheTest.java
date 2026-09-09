package lm.prep;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class LruCacheTest {

    @Test
    void evictsTheLeastRecentlyUsedEntry() {
        var cache = new LruCache<String, Integer>(2);
        cache.put("a", 1);
        cache.put("b", 2);
        cache.get("a");            // "a" is now the most recently used
        cache.put("c", 3);         // evicts "b", not "a"

        assertTrue(cache.containsKey("a"));
        assertFalse(cache.containsKey("b"));
        assertTrue(cache.containsKey("c"));
        assertEquals(2, cache.size());
    }

    @Test
    void rejectsNonPositiveCapacity() {
        assertThrows(IllegalArgumentException.class, () -> new LruCache<String, String>(0));
    }
}
