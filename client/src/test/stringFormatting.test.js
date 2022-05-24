/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { expect } from 'vitest'
import {
  article,
  capitalise,
  underscoreToSpace,
} from '../helpers/resultFormatter'

const testWord = 'foo'

/**
 * Test different articles depending on the following word
 */
describe('article', () => {
  test('starts with a vowel', () => {
    expect(article('a')).toBe('an')
  })

  test('starts with a consonant', () => {
    expect(article('b')).toBe('a')
  })

  /* TODO how to handle empty input?
  test('empty', () => {
    expect(article('')).toBe(false)
  })*/
})

/**
 * Test capitalisation of a string
 */
describe('capitalise', () => {
  /* TODO how to handle empty input?
    test('empty')
    */
  test('single letter', () => {
    expect(capitalise('a')).toBe('A')
  })

  test('multiple letters', () => {
    // The first letter of the capitalised word
    // is the same as the first letter of the uppercase word
    expect(capitalise(testWord)[0] == testWord.toUpperCase()[0]).toBe(true)
  })

  // Note: Capitalise doesn't capitalise all words in the string/sentence
  // Just the first letter
  test('multiple words', () => {
    const testWords = testWord + ' ' + testWord
    const [_, ...restOriginal] = testWords
    const [firstLetter, ...rest] = capitalise(testWords)

    // Test that the first letter of the string is capitalised
    expect(firstLetter == testWord.toUpperCase()[0]).toBe(true)
    // Test that the rest of the string is the same
    expect(JSON.stringify(rest) == JSON.stringify(restOriginal)).toBe(true)
  })
})

/**
 * Test the string conversion of text separated by underscores to spaces
 */
describe('underscore to space', () => {
  // A single underscore should simply return a space
  test('single underscore', () => {
    // TODO trim?
    expect(underscoreToSpace('_')).toBe(' ')
  })
  // Multiple words with an underscore at the end should give back
  // the words with a space at the end
  test('multiple words', () => {
    // TODO trim?
    expect(underscoreToSpace(testWord + '_' + testWord + '_')).toBe(
      testWord + ' ' + testWord + ' '
    )
  })
})
