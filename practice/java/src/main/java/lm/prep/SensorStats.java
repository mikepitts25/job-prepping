package lm.prep;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Stream-based aggregation over detections.
 *
 * <p>The Java equivalents of the Python practice problems, so you can answer a
 * "now do it in Java" follow-up without stalling.
 */
public final class SensorStats {

    private SensorStats() {
    }

    /** Detection count per sensor. */
    public static Map<String, Long> countsBySensor(List<Detection> detections) {
        return detections.stream()
                .collect(Collectors.groupingBy(Detection::sensorId, Collectors.counting()));
    }

    /** Mean confidence per sensor. */
    public static Map<String, Double> averageConfidence(List<Detection> detections) {
        return detections.stream()
                .collect(Collectors.groupingBy(Detection::sensorId,
                        Collectors.averagingDouble(Detection::confidence)));
    }

    /**
     * The k sensors with the highest mean confidence, best first.
     *
     * <p>Ties break by sensor id so the result is deterministic. A
     * non-deterministic result is untestable, which is the reason to care.
     */
    public static List<String> topSensors(List<Detection> detections, int k, long minRecords) {
        Map<String, Long> counts = countsBySensor(detections);
        return averageConfidence(detections).entrySet().stream()
                .filter(e -> counts.getOrDefault(e.getKey(), 0L) >= minRecords)
                .sorted(Comparator.<Map.Entry<String, Double>>comparingDouble(Map.Entry::getValue)
                        .reversed()
                        .thenComparing(Map.Entry::getKey))
                .limit(k)
                .map(Map.Entry::getKey)
                .toList();
    }

    /** Parses lines, skipping malformed ones. Returns only the good records. */
    public static List<Detection> parseAll(List<String> lines) {
        return lines.stream()
                .map(String::trim)
                .filter(line -> !line.isEmpty() && !line.startsWith("#"))
                .map(SensorStats::parseOrNull)
                .filter(java.util.Objects::nonNull)
                .toList();
    }

    private static Detection parseOrNull(String line) {
        try {
            return Detection.parse(line);
        } catch (IllegalArgumentException e) {
            return null;
        }
    }
}
