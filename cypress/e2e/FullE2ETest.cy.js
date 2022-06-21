/**
 * Performs a full End to end test of the application.
 * 
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
    it('Send Experiment', () => {
        cy.get('button').contains('Send').click()
    })
})

describe('Experiment Queue', () => {
    var queue
    it('Check for approaches in queue', () => {
        cy.wait(2000)
        queue = cy.get('div[data-testid*="Queue"]')
        queue.get('td').contains('Random, PopScore').should('be.visible')
    })
    it('Check for correct metrics in queue', () => {
        queue.get('td').contains('P@K, MAE').should('be.visible')
    })
    it('Cancel result', () => {
        queue.get('button[data-testid*="delete"]').click({ force: true })
        queue.get('button').contains('yes').should('be.visible').click({ force: true })
        queue.get('button').contains('Aborted').should('be.visible')
    })
})

describe('Simple mock for result', () =>{
    it('Send Computation', () => {
        cy.get('button').contains('New Experiment').click({ force: true })
        cy.get('button').contains('Metric Mock').click()
    })
    it('Waiting for result', () => {
        cy.scrollTo('top', {ensureScrollable: false})
        cy.wait(12500)
    })
})

describe('Results', () => {
    it('Visit results tab', () => {
        cy.get('button').contains('Results').click({ force: true })
    })
    it('Check if there are results', () => {
        cy.get('p').contains('Results for').should('be.visible')
    })
    it('Check if there are results for each dataset', () => {
        cy.get('caption').contains('LFM-1B').should('be.visible')
    })
    it('Check if there are results for metrics', () => {
        cy.get('th').contains('P@10').should('be.visible')
    })
})


describe('Result overview', () => {
    var overview
    var results
    it('Visit results overview tab', () => {
        cy.get('button').contains('All results').click({ force: true })
        overview = cy.get('div[data-testid*="AllResults"]')
    })
    it('Check that result is in overview', () => {
        overview.get('td').contains('LFM-2B_user-track-count_0').should('be.visible')
        results = overview.get('tbody').length
    })
    it('Check that metrics is correct', () => {
        overview.get('td').contains('Random').should('be.visible')
        overview.get('td').contains('P@K, P@K').should('be.visible')
    })
    it('Delete result', () => {
        overview.get('button["data-testid="delete"]').click()
        overview.get('button').contains('yes').should('be.visible').click()        
    })
    it('Check if result has been deleted', () =>
        overview.get('tbody').should('have.length',(results-1))
    )

})
