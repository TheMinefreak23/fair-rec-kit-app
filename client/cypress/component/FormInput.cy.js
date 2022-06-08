import { mount } from 'cypress/vue'
import FormInput from '../../src/components/Form/FormInput.vue'

describe('FormInput.cy.js', () => {
  it('input', () => {
    const value = { name: 'foo', min: 0, max: 1 }
    const form = { value: 0.5 }
    cy.mount(FormInput, { props: { value, modelValue: form, maxK: 10 } })
      .get('[data-testid=input]')
      .should('contain.text', 'Enter ')
  })
})
