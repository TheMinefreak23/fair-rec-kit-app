/**
 * Performs a full e2e test of the application.
 */
Cypress.config('viewportWidth', 1920)
Cypress.config('viewportHeight', 1080)


describe('Visit', () => {
    it('Visits the local app', () => {
        cy.visit('localhost:3000')
    })
})

describe('New Experiment', () => {
    it('Fill in metadata', () => {
        cy.viewport(1920, 1080)
        cy.get('#new-experiment').within(($form) => {
            cy.get('input[placeholder="New experiment"]').type('Cypress Test')
            cy.get('input[value="prediction"]').click()
            let rec = cy.get('input[value="recommendation"]')
            rec.should('not.be.checked')
            rec.click()
            cy.get('input[placeholder*="mail"]').type('Raja@limburg.nl')
            cy.get('input[placeholder*="tag"]').type('Test ')
        })
    })
    it('Select Datasets', () => {
        cy.get('#datasets').within(($datasets) => {
            cy.get('button').contains('Add dataset...').click()

            cy.get('select').each($el => {
                cy.wrap($el).select(1)
            })
            cy.get('select').each($el => {
                cy.wrap($el).select(1)
            })
            cy.get('select').each($el => {
                cy.wrap($el).select(1)
            })
        })
    })
    it('Select Approaches', () => {
        cy.get('div[id*=recommender]').within(($approaches) => {
            cy.get('button').contains('Add approach...').click()

            cy.get('select').each($el => {
                cy.wrap($el).select(1)
            })

        })
    })
})

describe('Experiment Queue', () => {
    it('Check for item in queue', () => {
        //todo

    })
})

describe('Results', () => {
    it('Check if there are results for each dataset', () => {
        //todo

    })
    it('Check if there are results for each metric', () => {
        //todo

    })
})

describe('Result overview', () => {
    it('Check that result is in overview', () => {
        //todo

    })
    it('Check that metadata is correct', () => {
        //todo

    })
})