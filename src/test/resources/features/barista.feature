@api @barista
Feature: Transiciones de Barista Bot
  Cada caso reinicia el robot y establece su propio estado inicial.

  Background:
    * url baseUrl

  @TC01 @REQ-BAR-01 @positivo @smoketest @GH-1
  Scenario: En Espera - Iniciar Pedido - Moliendo
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'En Espera' }
    Given path 'barista-bot', 'evento'
    And request { evento: 'Iniciar Pedido' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'En Espera', evento: 'Iniciar Pedido', estadoNuevo: 'Moliendo', valida: true, accion: null }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'Moliendo'

  @TC02 @REQ-BAR-02 @positivo @GH-2
  Scenario: Moliendo - Terminar Molienda - Calentando Agua
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'Moliendo' }
    Given path 'barista-bot', 'evento'
    And request { evento: 'Terminar Molienda' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'Moliendo', evento: 'Terminar Molienda', estadoNuevo: 'Calentando Agua', valida: true, accion: null }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'Calentando Agua'

  @TC03 @REQ-BAR-03 @positivo @GH-3
  Scenario: Calentando Agua - Alcanzar Temperatura - Sirviendo
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'Calentando Agua' }
    Given path 'barista-bot', 'evento'
    And request { evento: 'Alcanzar Temperatura' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'Calentando Agua', evento: 'Alcanzar Temperatura', estadoNuevo: 'Sirviendo', valida: true, accion: null }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'Sirviendo'

  @TC04 @REQ-BAR-04 @positivo @GH-4
  Scenario: Sirviendo - Terminar Llenado - En Espera
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'Sirviendo' }
    Given path 'barista-bot', 'evento'
    And request { evento: 'Terminar Llenado' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'Sirviendo', evento: 'Terminar Llenado', estadoNuevo: 'En Espera', valida: true, accion: null }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'En Espera'

  @TC05 @REQ-BAR-05 @positivo @GH-5
  Scenario: Moliendo - Sin Ingredientes - Error de Insumos
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'Moliendo' }
    Given path 'barista-bot', 'evento'
    And request { evento: 'Sin Ingredientes' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'Moliendo', evento: 'Sin Ingredientes', estadoNuevo: 'Error de Insumos', valida: true, accion: 'Interrumpir flujo' }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'Error de Insumos'

  @TC06 @REQ-BAR-05 @positivo @GH-6
  Scenario: Calentando Agua - Sin Ingredientes - Error de Insumos
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'Calentando Agua' }
    Given path 'barista-bot', 'evento'
    And request { evento: 'Sin Ingredientes' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'Calentando Agua', evento: 'Sin Ingredientes', estadoNuevo: 'Error de Insumos', valida: true, accion: 'Interrumpir flujo' }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'Error de Insumos'

  @TC07 @REQ-BAR-05 @positivo @GH-7
  Scenario: Sirviendo - Sin Ingredientes - Error de Insumos
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'Sirviendo' }
    Given path 'barista-bot', 'evento'
    And request { evento: 'Sin Ingredientes' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'Sirviendo', evento: 'Sin Ingredientes', estadoNuevo: 'Error de Insumos', valida: true, accion: 'Interrumpir flujo' }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'Error de Insumos'

  @TC08 @REQ-BAR-06 @positivo @smoketest @GH-8
  Scenario: Error de Insumos - Recargar y Reiniciar - En Espera
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'Error de Insumos' }
    Given path 'barista-bot', 'evento'
    And request { evento: 'Recargar y Reiniciar' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'Error de Insumos', evento: 'Recargar y Reiniciar', estadoNuevo: 'En Espera', valida: true, accion: 'Restaurar servicio' }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'En Espera'

  @TC09 @REQ-BAR-07 @negativo @GH-9
  Scenario Outline: Rechazar <evento> desde En Espera sin cambiar el estado
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'En Espera' }
    Given path 'barista-bot', 'evento'
    And request { evento: '<evento>' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'En Espera', evento: '<evento>', estadoNuevo: 'En Espera', valida: false, noDefinida: true }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'En Espera'
    * def ultimo = response.historial[response.historial.length - 1]
    And match ultimo contains { evento: '<evento>', estadoNuevo: 'En Espera', valida: false }

    Examples:
      | evento |
      | Terminar Molienda |
      | Alcanzar Temperatura |
      | Terminar Llenado |
      | Sin Ingredientes |
      | Recargar y Reiniciar |

  @TC10 @REQ-BAR-07 @negativo @GH-10
  Scenario Outline: Rechazar <evento> desde Moliendo sin cambiar el estado
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'Moliendo' }
    Given path 'barista-bot', 'evento'
    And request { evento: '<evento>' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'Moliendo', evento: '<evento>', estadoNuevo: 'Moliendo', valida: false, noDefinida: true }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'Moliendo'
    * def ultimo = response.historial[response.historial.length - 1]
    And match ultimo contains { evento: '<evento>', estadoNuevo: 'Moliendo', valida: false }

    Examples:
      | evento |
      | Iniciar Pedido |
      | Alcanzar Temperatura |
      | Terminar Llenado |
      | Recargar y Reiniciar |

  @TC11 @REQ-BAR-07 @negativo @GH-11
  Scenario Outline: Rechazar <evento> desde Calentando Agua sin cambiar el estado
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'Calentando Agua' }
    Given path 'barista-bot', 'evento'
    And request { evento: '<evento>' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'Calentando Agua', evento: '<evento>', estadoNuevo: 'Calentando Agua', valida: false, noDefinida: true }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'Calentando Agua'
    * def ultimo = response.historial[response.historial.length - 1]
    And match ultimo contains { evento: '<evento>', estadoNuevo: 'Calentando Agua', valida: false }

    Examples:
      | evento |
      | Iniciar Pedido |
      | Terminar Molienda |
      | Terminar Llenado |
      | Recargar y Reiniciar |

  @TC12 @REQ-BAR-07 @negativo @GH-12
  Scenario Outline: Rechazar <evento> desde Sirviendo sin cambiar el estado
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'Sirviendo' }
    Given path 'barista-bot', 'evento'
    And request { evento: '<evento>' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'Sirviendo', evento: '<evento>', estadoNuevo: 'Sirviendo', valida: false, noDefinida: true }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'Sirviendo'
    * def ultimo = response.historial[response.historial.length - 1]
    And match ultimo contains { evento: '<evento>', estadoNuevo: 'Sirviendo', valida: false }

    Examples:
      | evento |
      | Iniciar Pedido |
      | Terminar Molienda |
      | Alcanzar Temperatura |
      | Recargar y Reiniciar |

  @TC13 @REQ-BAR-07 @negativo @GH-13
  Scenario Outline: Rechazar <evento> desde Error de Insumos sin cambiar el estado
    * def setup = call read('classpath:helpers/barista-state.feature') { estado: 'Error de Insumos' }
    Given path 'barista-bot', 'evento'
    And request { evento: '<evento>' }
    When method post
    Then status 200
    And match response contains { estadoAnterior: 'Error de Insumos', evento: '<evento>', estadoNuevo: 'Error de Insumos', valida: false, noDefinida: true }
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == 'Error de Insumos'
    * def ultimo = response.historial[response.historial.length - 1]
    And match ultimo contains { evento: '<evento>', estadoNuevo: 'Error de Insumos', valida: false }

    Examples:
      | evento |
      | Iniciar Pedido |
      | Terminar Molienda |
      | Alcanzar Temperatura |
      | Terminar Llenado |
      | Sin Ingredientes |

