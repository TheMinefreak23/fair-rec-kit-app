/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { render, fireEvent, within, getByText } from '@testing-library/vue'
import { expect, test } from 'vitest'
import FormGroupList from '../components/FormGroupList.vue'
import { capitalise } from '../helpers/resultFormatter'

const form = {
  main: [],
  inputs: [],
  selects: [],
  lists: [],
}

const values = {
  values: [{ default: 0, max: 1, min: -1, name: 'foo value' }],
}

const options = [
  { name: 'foo', value: { name: 'foo', params: values } },
  { name: 'hi', value: { name: 'hivalue' } },
  { name: 'foo3', value: { name: 'bar3' } },
]

function getProps(options) {
  return {
    data: form,
    name: 'foo',
    plural: 'foos',
    options: options,
    required: 'true',
  }
}

test('remove button', async () => {
  const count = 2
  form.groupCount = count
  const {
    getByText,
    getAllByTestId,
    getByTestId,
    getByLabelText,
    getByDisplayValue,
  } = render(FormGroupList, {
    props: getProps(options),
  })

  // Check if there is a remove button
  const removeButton = within(getByTestId('remove-button')).getByText('X')

  // Press button
  await fireEvent.click(removeButton)

  // Check for decrease in options
  const dropdowns = getAllByTestId('main-select')
  // There should be two empty options now
  expect(dropdowns.length).toBe(count - 1)
})

test('required option: test labels and adding option', async () => {
  // Initialise empty form

  //const testName = 'foo'
  //const testPlural = testName + 's'

  // Render FormGroupList
  const count = 1
  form.groupCount = count
  const {
    getByText,
    getAllByTestId,
    getByTestId,
    getByLabelText,
    getByDisplayValue,
  } = render(FormGroupList, {
    props: getProps(options),
  })

  // Check text rendering
  getByText('Foos')
  //getByLabelText('Select a foo') TODO causes Expected container error

  //getByDisplayValue('Choose..')

  // Add an option
  const addButton = getByText('Add foo...')
  await fireEvent.click(addButton)

  // Check for increase in options
  const dropdowns = getAllByTestId('main-select')
  // There should be two empty options now
  expect(dropdowns.length).toBe(count + 1)

  /*for (let dropdown in dropdowns) {
    expect(dropdown.value).toBe('')
  }*/
})

test('select main option', async () => {
  // Render FormGroupList
  const count = 1
  form.groupCount = count
  const {
    getByText,
    getAllByTestId,
    getByTestId,
    getByLabelText,
    getByDisplayValue,
  } = render(FormGroupList, {
    props: getProps(options),
  })

  // Check the initial selection
  const dropdown = getByTestId('main-select')
  //fireEvent.change(dropdown, options[0])
  //fireEvent.change(dropdown, options[0])
  //fireEvent.change(dropdown, { target: { value: options[0] } })
  //expect(dropdown.value).toBe('')
})

/* TODO not working
test('test train/test split', async () => {
  const splitValues = { ...values }
  splitValues.values[0].name = 'Train'
  options[0].value.params = splitValues

  // Render FormGroupList
  form.groupCount = 1
  const { getByTestId, getByText } = render(FormGroupList, {
    props: getProps(options),
  })

  // Select a dataset
  const dropdown = getByTestId('main-select')
  //await fireEvent.click(dropdown)
  //await fireEvent.keyDown(dropdown, { key: 'ArrowDown', code: 'ArrowDown' })
  //await fireEvent.click(dropdown)
  //await fireEvent.change(dropdown, { target: { value: options[0] } })
  await fireEvent.update(dropdown, options[0])
  await fireEvent.change(dropdown, options[0])

  // Check if the text is there
  getByText('Train:')
  getByText('Test:')
  //getByTestId('train-test-text')

  // Check if the slider is there and the standard value
  //const slider = getByTestId('split-input')
  expect(slider.value).toBe('20')
})*/

/*test('copy', async () => {
  // Render FormGroupList
  const count = 1 // Start with one option
  form.groupCount = count
  const { getByTestId, getAllByTestId } = render(FormGroupList, {
    props: getProps(options),
  })
  // Select
  //const nameField = getByLabelText('Select a foo')
  const dropdown = getByTestId('main-select')
  await fireEvent.update(dropdown, 'foo')

  // Check for copy button and click it
  const copyButton = getByText('Copy foo...')
  await fireEvent.click(copyButton)

  // Check for increase in options
  const dropdowns = getAllByTestId('main-select')
  // There should be two empty options now
  expect(dropdowns.length).toBe(count + 1)
})*/
