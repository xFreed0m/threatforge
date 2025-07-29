describe('Threat Model Upload', () => {
  beforeEach(() => {
    cy.visit('/')
    cy.get('[data-testid="threat-model-btn"]').click()
  })

  it('should upload a diagram file and generate threat model', () => {
    // Upload a file
    cy.get('input[type="file"]').attachFile('sample.drawio')
    cy.get('.upload-btn').click()
    cy.get('.file-list').should('contain', 'sample.drawio')

    // Fill in the threat model form
    cy.get('#content').type('A web application with user authentication and database storage')
    cy.get('#framework').click()
    cy.get('.p-dropdown-item').contains('STRIDE').click()
    cy.get('#file').click()
    cy.get('.p-dropdown-item').first().click()
    cy.get('#provider').click()
    cy.get('.p-dropdown-item').contains('openai').click()

    // Generate threat model
    cy.get('.generate-button').click()

    // Check that threat model was generated
    cy.get('.threat-model-results').should('be.visible')
    cy.get('.threat-model-title').should('contain', 'Generated Threat Model')
  })

  it('should generate threat model with text only', () => {
    // Fill in the threat model form with text only
    cy.get('#content').type('A cloud-based microservices application with API gateway and database')
    cy.get('#framework').click()
    cy.get('.p-dropdown-item').contains('STRIDE').click()
    cy.get('#provider').click()
    cy.get('.p-dropdown-item').contains('openai').click()

    // Generate threat model
    cy.get('.generate-button').click()

    // Check that threat model was generated
    cy.get('.threat-model-results').should('be.visible')
    cy.get('.threat-model-title').should('contain', 'Generated Threat Model')
  })

  it('should support drag and drop upload', () => {
    cy.get('.drop-area').attachFile('sample.drawio', { subjectType: 'drag-n-drop' })
    cy.get('.upload-btn').click()
    cy.get('.file-list').should('contain', 'sample.drawio')
  })

  it('should delete uploaded files', () => {
    // Upload a file first
    cy.get('input[type="file"]').attachFile('sample.drawio')
    cy.get('.upload-btn').click()
    cy.get('.file-list').should('contain', 'sample.drawio')

    // Delete the file
    cy.get('.delete-btn').first().click()
    cy.get('.file-list').should('not.contain', 'sample.drawio')
  })

  it('should support bulk delete', () => {
    // Upload multiple files
    cy.get('input[type="file"]').attachFile(['sample.drawio', 'sample2.drawio'])
    cy.get('.upload-btn').click()
    cy.get('.file-list').should('have.length', 2)

    // Select files and bulk delete
    cy.get('input[type="checkbox"]').first().check()
    cy.get('input[type="checkbox"]').last().check()
    cy.get('.bulk-delete-btn').click()
    cy.get('.file-list').should('not.exist')
  })

  it('should validate form before generation', () => {
    // Try to generate without content
    cy.get('.generate-button').should('be.disabled')
    
    // Add content and enable button
    cy.get('#content').type('Test content')
    cy.get('.generate-button').should('not.be.disabled')
  })

  it('should show different frameworks', () => {
    cy.get('#framework').click()
    cy.get('.p-dropdown-item').should('contain', 'STRIDE')
    cy.get('.p-dropdown-item').should('contain', 'LINDDUN')
    cy.get('.p-dropdown-item').should('contain', 'PASTA')
    cy.get('.p-dropdown-item').should('contain', 'Attack Trees')
  })
}) 