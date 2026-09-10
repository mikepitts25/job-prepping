package lm.prep;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;

class DetectionTest {

    @Test
    @DisplayName("a confidence outside 0..1 cannot be constructed")
    void rejectsOutOfRangeConfidence() {
        assertThrows(IllegalArgumentException.class,
                () -> new Detection("RDR-1", 0L, 1.5));
        assertThrows(IllegalArgumentException.class,
                () -> new Detection("RDR-1", 0L, -0.1));
        assertThrows(IllegalArgumentException.class,
                () -> new Detection("RDR-1", 0L, Double.NaN));
    }

    @Test
    void rejectsBlankSensorId() {
        assertThrows(IllegalArgumentException.class, () -> new Detection("  ", 0L, 0.5));
    }

    @ParameterizedTest
    @CsvSource({"0.9, true", "0.8, true", "0.79, false", "0.0, false"})
    void highConfidenceThresholdIsInclusive(double confidence, boolean expected) {
        assertEquals(expected, new Detection("RDR-1", 0L, confidence).isHighConfidence());
    }

    @Test
    void parsesAWellFormedLine() {
        Detection d = Detection.parse("RDR-1, 1000, 0.75");
        assertEquals("RDR-1", d.sensorId());
        assertEquals(1000L, d.timestampMillis());
        assertEquals(0.75, d.confidence(), 1e-9);
    }

    @Test
    void parseFailureKeepsTheCause() {
        var thrown = assertThrows(IllegalArgumentException.class,
                () -> Detection.parse("RDR-1,notanumber,0.5"));
        assertNotNull(thrown.getCause(), "the NumberFormatException should be chained");
    }

    @Test
    @DisplayName("records give equals and hashCode consistent for free")
    void recordEqualityIsValueBased() {
        var a = new Detection("RDR-1", 1L, 0.5);
        var b = new Detection("RDR-1", 1L, 0.5);
        assertEquals(a, b);
        assertEquals(a.hashCode(), b.hashCode());
    }
}
