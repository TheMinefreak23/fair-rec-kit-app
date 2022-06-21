describe('Visit', () => {
  it('Visits the local app', () => {
    cy.visit('localhost:3000')
  })
})

it('findByText', () => {
  cy.findByText('Choose..').click().should('contain', 'Button Clicked')
})
