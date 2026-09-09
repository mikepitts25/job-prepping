package lm.prep;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class SensorStatsTest {

    private static final List<Detection> SAMPLE = List.of(
            new Detection("A", 1L, 0.2),
            new Detection("A", 2L, 0.4),
            new Detection("B", 1L, 0.9),
            new Detection("C", 1L, 0.5));

    @Test
    void countsPerSensor() {
        assertEquals(2L, SensorStats.countsBySensor(SAMPLE).get("A"));
        assertEquals(1L, SensorStats.countsBySensor(SAMPLE).get("B"));
    }

    @Test
    void averagesPerSensor() {
        assertEquals(0.3, SensorStats.averageConfidence(SAMPLE).get("A"), 1e-9);
    }

    @Test
    void ranksByAverageConfidence() {
        assertEquals(List.of("B", "C", "A"), SensorStats.topSensors(SAMPLE, 3, 1));
    }

    @Test
    void appliesMinimumRecordCount() {
        assertEquals(List.of("A"), SensorStats.topSensors(SAMPLE, 3, 2));
    }

    @Test
    void tiesBreakBySensorIdForDeterminism() {
        var tied = List.of(new Detection("B", 1L, 0.5), new Detection("A", 1L, 0.5));
        assertEquals(List.of("A", "B"), SensorStats.topSensors(tied, 2, 1));
    }

    @Test
    void skipsMalformedAndCommentLines() {
        var parsed = SensorStats.parseAll(List.of(
                "# header", "", "A,1,0.5", "bad line", "B,notanumber,0.5", "C,2,0.7"));
        assertEquals(List.of("A", "C"), parsed.stream().map(Detection::sensorId).toList());
    }

    @Test
    void emptyInputProducesEmptyOutput() {
        assertTrue(SensorStats.topSensors(List.of(), 3, 1).isEmpty());
    }
}
