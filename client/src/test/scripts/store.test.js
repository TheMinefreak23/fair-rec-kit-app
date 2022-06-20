/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { describe, test, expect } from 'vitest'
import { addResult, removeResult, store } from '../../store'

/**
 * Test result adding
 */
describe('add result', () => {
  test('array increase and tab switch', () => {
    store.currentResults = []
    addResult({})
    expect(store.currentResults.length).toBe(1)
    expect(store.currentResultTab).toBe(0)
  })
})

/**
 * Test result removing
 */
describe('remove result', () => {
  test('array decrease and tab switch', () => {
    store.currentResults = [{}]
    removeResult(0)
    expect(store.currentResults.length).toBe(0)
    expect(store.currentResultTab).toBe(0) // doesn't change current result tab
  })
})
