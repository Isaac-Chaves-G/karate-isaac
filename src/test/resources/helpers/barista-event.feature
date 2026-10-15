@ignore
Feature: Ejecutar y comprobar un evento de preparación
  Scenario:
    Given url baseUrl
    And path 'barista-bot', 'evento'
    And request { evento: '#(evento)' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: '#(anterior)', estadoNuevo: '#(siguiente)', valida: true }
