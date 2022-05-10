/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import {
  article,
  capitalise,
  underscoreToSpace,
} from '../helpers/resultFormatter'

const testWord = 'foo'

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
})

describe('underscore to space', () => {
  test('single underscore', () => {
    // TODO trim?
    expect(underscoreToSpace('_')).toBe(' ')
  })
  test('multiple words', () => {
    // TODO trim?
    expect(underscoreToSpace(testWord + '_' + testWord + '_')).toBe(
      testWord + ' ' + testWord + ' '
    )
  })
})
