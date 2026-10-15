package runner;

import com.intuit.karate.Results;
import com.intuit.karate.Runner;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ApiTest {
    @Test
    void runApiScenarios() {
        Results results = Runner.path("classpath:features")
                .reportDir("target/karate-reports")
                .outputCucumberJson(true)
                .outputJunitXml(true)
                .parallel(1);
        assertTrue(results.getScenariosTotal() > 0, "El filtro no seleccionó escenarios: no es una ejecución exitosa.");
        assertEquals(0, results.getFailCount(), results.getErrorMessages());
    }
}
