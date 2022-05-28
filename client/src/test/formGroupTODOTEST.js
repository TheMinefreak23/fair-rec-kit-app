/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { render, fireEvent, within } from '@testing-library/vue'
import { expect, test } from 'vitest'
import FormGroup from '../components/Form/FormGroup.vue'

function getProps(options) {
  return {
    data: {},
    name: 'foo',
    title: 'foos',
    options: options,
    required: 'true',
  }
}

const params = {
  selects: [],
  values: [{ default: 0, max: 1, min: -1, name: 'foo value' }],
}

const options = [
  { name: 'foo', value: { name: 'foo', params: params } },
  { name: 'hi', value: { name: 'hivalue' } },
  { name: 'foo3', value: { name: 'bar3' } },
]

/**
 * Test selecting a main option in a form group
 */
test('select main option', async () => {
  // Render FormGroupList
  const {
    getByText,
    getAllByTestId,
    getByTestId,
    getByLabelText,
    getByDisplayValue,
  } = render(FormGroup, {
    props: getProps(options),
  })

  getByLabelText('Select a foo *')

  getByTestId('main-option')
  getByText('Choose..')

  // Check the initial selection
  const mainSelect = getByTestId('main-select')
  await fireEvent.update(mainSelect, options[0].value)
  getByText(options[0].name)
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
