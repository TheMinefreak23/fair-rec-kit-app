/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import { describe, test, expect } from 'vitest'
import { validateEmail, selectionOptions } from '../../helpers/optionsFormatter'

/**
 * Test creation of a list for option selection
 */
describe('selectionOptions', () => {
  // test that the empty options gets added correctly
  test('empty', () => {
    expect(selectionOptions([]).length).toBe(1)
  })
})

/**
 * Test email validation
 */
describe('validate email', () => {
  // test that both valid and invalid emails work
  test('valid', () => {
    expect(selectionOptions('mail@valid.com').length > 1).toBe(true)
  })
  test('invalid', () => {
    expect(validateEmail('Not a valid email adres')).toBe(null)
  })
})
