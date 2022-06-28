/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { describe, test, expect } from 'vitest'
import {
  status,
  statusPrefix,
  statusVariant,
} from '../../helpers/queueFormatter'

/**
 * Test the status display variant in the queue table
 */
describe('get status variant', () => {
  // Test empty string
  test('check empty string', () => {
    expect(statusVariant('')).toBe(undefined)
  })
  // Test empty status
  test('check empty status', () => {
    expect(statusVariant('status_')).toBe(undefined)
  })
  // Test non-status
  test('check non-status', () => {
    expect(statusVariant('foo')).toBe(undefined)
  })
  // Test all statuses
  test('check status', () => {
    for (const statusName of Object.values(status)) {
      expect(statusVariant(statusName) != undefined)
    }
  })
})

/**
 * Test the status string format
 */
describe('get status from prefix', () => {
  // Test checking whether string is a status
  test('check status string', () => {
    expect('status_foo'.slice(statusPrefix.length)).toBe('foo')
  })
})
