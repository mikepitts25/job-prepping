package lm.prep;

/**
 * One normalized sensor report.
 *
 * <p>A record because this is an immutable value carried across threads and
 * queues. Immutability is the cheapest thread-safety strategy there is, and the
 * compact constructor makes an out-of-range confidence unrepresentable rather
 * than something the correlator has to defend against later.
 */
public record Detection(String sensorId, long timestampMillis, double confidence) {

    public Detection {
        if (sensorId == null || sensorId.isBlank()) {
            throw new IllegalArgumentException("sensorId must not be blank");
        }
        if (Double.isNaN(confidence) || confidence < 0.0 || confidence > 1.0) {
            throw new IllegalArgumentException("confidence out of range: " + confidence);
        }
    }

    public boolean isHighConfidence() {
        return confidence >= 0.8;
    }

    /** Parses {@code sensorId,timestampMillis,confidence}. */
    public static Detection parse(String line) {
        String[] parts = line.split(",");
        if (parts.length != 3) {
            throw new IllegalArgumentException("expected 3 fields, got " + parts.length + ": " + line);
        }
        try {
            return new Detection(parts[0].trim(),
                                 Long.parseLong(parts[1].trim()),
                                 Double.parseDouble(parts[2].trim()));
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("unparseable numeric field in: " + line, e);
        }
    }
}
