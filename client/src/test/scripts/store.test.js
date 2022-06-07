/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { describe, test, expect } from 'vitest'
import { addResult, store } from '../../store'

/**
 * Test result adding
 */
describe('add result', () => {
  test('array increase and tab switch', () => {
    const oldLength = store.currentResults.length
    addResult({})
    expect(store.currentResults.length).toBe(oldLength + 1)
    expect(store.currentResultTab).toBe(oldLength)
  })
})

/**
 * Test result removing
 */
describe('remove result', () => {
  test('array increase and tab switch', () => {
    const oldLength = store.currentResults.length
    addResult({})
    expect(store.currentResults.length).toBe(oldLength - 1)
    expect(store.currentResultTab).toBe(oldLength - 2)
  })
})
