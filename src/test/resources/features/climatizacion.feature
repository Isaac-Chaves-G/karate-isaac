@api @climatizacion
Feature: Decisiones de climatización de Smart Home
  Las entradas booleanas representan temperatura mayor a 26 grados,
  presencia humana y aperturas superiores a tres minutos, en ese orden.

  Background:
    * url baseUrl

  @TC14 @REQ-CLI-04 @positivo @GH-14
  Scenario: Temperatura alta=false, presencia=false, apertura prolongada=false
    Given path 'decision', 'climatizacion', 'evaluar'
    And request { valores: [false, false, false] }
    When method post
    Then status 200
    And match response == { valores: [false, false, false], accion: 'Mantener sistema apagado', reglaIndex: 3, noDefinida: false }

  @TC15 @REQ-CLI-01 @positivo @smoketest @GH-15
  Scenario: Temperatura alta=false, presencia=false, apertura prolongada=true
    Given path 'decision', 'climatizacion', 'evaluar'
    And request { valores: [false, false, true] }
    When method post
    Then status 200
    And match response == { valores: [false, false, true], accion: 'Apagar sistema de climatización y emitir alerta sonora', reglaIndex: 0, noDefinida: false }

  @TC16 @REQ-CLI-04 @positivo @GH-16
  Scenario: Temperatura alta=false, presencia=true, apertura prolongada=false
    Given path 'decision', 'climatizacion', 'evaluar'
    And request { valores: [false, true, false] }
    When method post
    Then status 200
    And match response == { valores: [false, true, false], accion: 'Mantener sistema apagado', reglaIndex: 3, noDefinida: false }

  @TC17 @REQ-CLI-01 @positivo @GH-17
  Scenario: Temperatura alta=false, presencia=true, apertura prolongada=true
    Given path 'decision', 'climatizacion', 'evaluar'
    And request { valores: [false, true, true] }
    When method post
    Then status 200
    And match response == { valores: [false, true, true], accion: 'Apagar sistema de climatización y emitir alerta sonora', reglaIndex: 0, noDefinida: false }

  @TC18 @REQ-CLI-03 @positivo @GH-18
  Scenario: Temperatura alta=true, presencia=false, apertura prolongada=false
    Given path 'decision', 'climatizacion', 'evaluar'
    And request { valores: [true, false, false] }
    When method post
    Then status 200
    And match response == { valores: [true, false, false], accion: 'Mantener en modo de bajo consumo energético', reglaIndex: 2, noDefinida: false }

  @TC19 @REQ-CLI-01 @positivo @GH-19
  Scenario: Temperatura alta=true, presencia=false, apertura prolongada=true
    Given path 'decision', 'climatizacion', 'evaluar'
    And request { valores: [true, false, true] }
    When method post
    Then status 200
    And match response == { valores: [true, false, true], accion: 'Apagar sistema de climatización y emitir alerta sonora', reglaIndex: 0, noDefinida: false }

  @TC20 @REQ-CLI-02 @positivo @smoketest @GH-20
  Scenario: Temperatura alta=true, presencia=true, apertura prolongada=false
    Given path 'decision', 'climatizacion', 'evaluar'
    And request { valores: [true, true, false] }
    When method post
    Then status 200
    And match response == { valores: [true, true, false], accion: 'Encender aire acondicionado en modo refrigeración', reglaIndex: 1, noDefinida: false }

  @TC21 @REQ-CLI-01 @positivo @GH-21
  Scenario: Temperatura alta=true, presencia=true, apertura prolongada=true
    Given path 'decision', 'climatizacion', 'evaluar'
    And request { valores: [true, true, true] }
    When method post
    Then status 200
    And match response == { valores: [true, true, true], accion: 'Apagar sistema de climatización y emitir alerta sonora', reglaIndex: 0, noDefinida: false }

  @TC22 @REQ-CLI-05 @negativo @GH-22
  Scenario Outline: Rechazar un contrato de entrada inválido - <caso>
    Given path 'decision', 'climatizacion', 'evaluar'
    And request <payload>
    When method post
    Then status 400
    And match response.error == 'Se esperaban 3 valores booleanos'

    Examples:
      | caso             | payload                           |
      | campo ausente    | {}                                |
      | lista vacía      | { valores: [] }                   |
      | faltan valores   | { valores: [true, false] }        |
      | sobran valores   | { valores: [true,true,true,true] } |
      | valor nulo       | { valores: null }                 |
      | valor no booleano | { valores: [true, 'si', false] }  |
