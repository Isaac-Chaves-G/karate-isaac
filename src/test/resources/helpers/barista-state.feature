@ignore
Feature: Establecer una precondición independiente usando la API pública
  Scenario:
    * def routes =
      """
      {
        'En Espera': [],
        'Moliendo': [
          { anterior: 'En Espera', evento: 'Iniciar Pedido', siguiente: 'Moliendo' }
        ],
        'Calentando Agua': [
          { anterior: 'En Espera', evento: 'Iniciar Pedido', siguiente: 'Moliendo' },
          { anterior: 'Moliendo', evento: 'Terminar Molienda', siguiente: 'Calentando Agua' }
        ],
        'Sirviendo': [
          { anterior: 'En Espera', evento: 'Iniciar Pedido', siguiente: 'Moliendo' },
          { anterior: 'Moliendo', evento: 'Terminar Molienda', siguiente: 'Calentando Agua' },
          { anterior: 'Calentando Agua', evento: 'Alcanzar Temperatura', siguiente: 'Sirviendo' }
        ],
        'Error de Insumos': [
          { anterior: 'En Espera', evento: 'Iniciar Pedido', siguiente: 'Moliendo' },
          { anterior: 'Moliendo', evento: 'Sin Ingredientes', siguiente: 'Error de Insumos' }
        ]
      }
      """
    * def route = routes[estado]
    * assert route != null
    Given url baseUrl
    And path 'barista-bot', 'reiniciar'
    When method post
    Then status 200
    And match response.estadoActual == 'En Espera'
    * def preparation = call read('classpath:helpers/barista-event.feature') route
    Given path 'barista-bot', 'estado'
    When method get
    Then status 200
    And match response.estadoActual == estado
