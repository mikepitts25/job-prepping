package lm.prep;

import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.*;

class BoundedIngestQueueTest {

    @Test
    void dropsOldestOnOverflowAndCountsTheDrops() {
        var queue = new BoundedIngestQueue(3);
        for (int i = 0; i < 5; i++) {
            queue.offer(new Detection("RDR-1", i, 0.5));
        }

        List<Detection> drained = queue.drain();
        assertEquals(3, drained.size());
        assertEquals(2L, drained.get(0).timestampMillis(), "oldest two were dropped");
        assertEquals(2L, queue.droppedCount());
    }

    @Test
    void memoryStaysBoundedUnderABurst() {
        var queue = new BoundedIngestQueue(100);
        for (int i = 0; i < 100_000; i++) {
            queue.offer(new Detection("RDR-1", i, 0.5));
        }
        assertEquals(100, queue.size());
        assertEquals(99_900L, queue.droppedCount());
    }

    @Test
    void concurrentProducersDoNotLoseAccounting() throws Exception {
        var queue = new BoundedIngestQueue(50);
        int threads = 4;
        int perThread = 1_000;
        var start = new CountDownLatch(1);         // latch, not sleep
        ExecutorService pool = Executors.newFixedThreadPool(threads);

        for (int t = 0; t < threads; t++) {
            pool.submit(() -> {
                start.await();
                for (int i = 0; i < perThread; i++) {
                    queue.offer(new Detection("RDR-1", i, 0.5));
                }
                return null;
            });
        }
        start.countDown();
        pool.shutdown();
        assertTrue(pool.awaitTermination(30, TimeUnit.SECONDS));

        assertEquals(50, queue.size());
        assertEquals(threads * perThread - 50L, queue.droppedCount());
    }

    @Test
    void rejectsNonPositiveCapacity() {
        assertThrows(IllegalArgumentException.class, () -> new BoundedIngestQueue(0));
    }
}
