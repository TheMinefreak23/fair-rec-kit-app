/**
 * Performs a full e2e test of the application.
 */
Cypress.config('viewportWidth', 1920)
Cypress.config('viewportHeight', 1080)
Cypress.config('baseUrl', 'http://localhost:3000')

describe('Visit', () => {
    it('Visits the local app', () => {
        cy.visit('/')
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

            cy.get('select').each(($el, index, $list) => {
                if (index == 1) {
                    cy.wrap($el).select(2)
                }
            })
            cy.get('select').each(($el) => {
                cy.wrap($el).select(1)
            })
            cy.get('select').each(($el) => {
                cy.wrap($el).select(1)
            })
        })
    })
    it('Select Approaches', () => {
        cy.get('div[id*=recommender]').within(($approaches) => {
            cy.get('button').contains('Add approach...').click()

            cy.get('select').each(($el) => {
                cy.wrap($el).select('Random', { force: true })
            })

            cy.get('#group-approach-1')
                .get('select')
                .each(($el, index, $list) => {
                    if (index > 0) {
                        cy.wrap($el).select('PopScore', { force: true })
                    }
                })
        })
    })
    it('Select Metrics', () => {
        cy.get('div[id*=metrics]').within(($metrics) => {
            cy.get('button').contains('Add metric...').click()
            cy.get('button').contains('Add metric...').click()

            cy.get('#group-metric-1')
                .get('select')
                .each(($el, index, $list) => {
                    if (index == 0) {
                        cy.wrap($el).select('P@K', { force: true })
                    }
                    if (index > 0) {
                        cy.wrap($el).select('MAE', { force: true })
                    }
                })
        })
    })
    it('Send Computation', () => {
        cy.get('button').contains('Send').click()
    })
})

describe('Experiment Queue', () => {
    var queue
    it('Check for approaches in queue', () => {
        queue = cy.get('div[data-testid*="Queue"]')
        cy.wait(1000)
        queue.get('td').contains('Random, PopScore').should('be.visible')
    })
    it('Check for correct metrics in queue', () => {
        queue.get('td').contains('P@K, MAE').should('be.visible')
    })
    it('Computing result', () => {
        cy.wait(10000)
    })
})

describe('Result overview', () => {
    var overview
    it('Visit results overview tab', () => {
        cy.get('button').contains('All results').click({ force: true })
        overview = cy.get('div[data-testid*="AllResults"]')
    })
    it('Check that result is in overview', () => {
        overview.get('td').contains('Cypress Test').should('be.visible')
    })
    it('Check that metadata is correct', () => {
        overview.get('td').contains('Random, PopScore').should('be.visible')
        overview.get('td').contains('P@K, MAE').should('be.visible')
    })

})

describe('Results', () => {
    it('Visit results tab', () => {
        cy.get('button').contains('Results').click({ force: true })
    })

    it('Check if there are results for each dataset', () => {
        cy.get('div').contains('Result Cypress Test').should('be.visible')
        cy.get('caption').contains('LFM-1B').should('be.visible')
    })
    it('Check if there are results for each metric', () => {
        cy.get('th').contains('P@10').should('be.visible')
        cy.get('th').contains('MAE').should('be.visible')
    })
})
