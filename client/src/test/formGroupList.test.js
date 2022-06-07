/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { render, fireEvent, within } from '@testing-library/vue'
import { expect, test } from 'vitest'
import FormGroupList from '../components/Form/FormGroupList.vue'
import { emptyFormGroup } from '../helpers/optionsFormatter'

/**
 * Create mock props for a required Foo form group list
 * @param {Object} options
 * @return {{Object}} mock form group list props
 */
function getProps() {
  const form = emptyFormGroup(true)
  return {
    modelValue: form,
    name: 'foo',
    title: 'foos',
    options: [],
    required: 'true',
  }
}

/**
 * Test the form group add and remove button
 */
test('add and remove', async () => {
  let count = 1 // Keep track of count
  const {
    getAllByText,
    getAllByTestId,
    getByTestId,
    getByLabelText,
    getByDisplayValue,
  } = render(FormGroupList, {
    props: getProps(),
  })

  // Get the only add button and add an option
  const addButton = getByTestId('add-button')
  within(addButton).getByText('Add foo...')

  await fireEvent.click(addButton)

  // There should be two empty options now
  let mainSelects = getAllByTestId('main-select')
  expect(mainSelects.length).toBe(++count)

  // Check if there is one remove button
  const removeButton = within(getByTestId('remove-button')).getByText('X')

  // Press button
  await fireEvent.click(removeButton)

  // Check for decrease in options
  mainSelects = getAllByTestId('main-select')
  // There should be two empty options now
  expect(mainSelects.length).toBe(count - 1)

  // Check that you can't remove the required option
  mainSelects = getAllByTestId('main-select')
  expect(mainSelects.length).toBe(count - 1)
})

/**
 * Test adding a form group
 */
test('required option: test labels', async () => {
  // Render FormGroupList
  const { getByText } = render(FormGroupList, {
    props: getProps(),
  })

  // Check text rendering
  getByText('Foos')
})
