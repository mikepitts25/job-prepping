package lm.prep;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

/**
 * A bounded queue that drops the oldest entry on overflow.
 *
 * <p>The design point worth stating in an interview: an unbounded queue turns a
 * fast producer into an out-of-memory crash. Bounding it forces a conscious
 * choice, and for position reports dropping the oldest is right, because a
 * stale position has no operational value. The drop counter is what keeps the
 * condition visible in monitoring rather than silent.
 */
public final class BoundedIngestQueue {

    private final Deque<Detection> items = new ArrayDeque<>();
    private final int capacity;
    private final AtomicLong dropped = new AtomicLong();

    public BoundedIngestQueue(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("capacity must be positive");
        }
        this.capacity = capacity;
    }

    public synchronized void offer(Detection detection) {
        if (items.size() == capacity) {
            items.removeFirst();
            dropped.incrementAndGet();
        }
        items.addLast(detection);
    }

    public synchronized List<Detection> drain() {
        List<Detection> out = new ArrayList<>(items);
        items.clear();
        return out;
    }

    public long droppedCount() {
        return dropped.get();
    }

    public synchronized int size() {
        return items.size();
    }
}
