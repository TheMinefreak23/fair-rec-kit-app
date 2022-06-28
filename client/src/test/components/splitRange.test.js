import SplitRange from '../../components/Form/SplitRange.vue'
import { render, fireEvent } from '@testing-library/vue'

test('Range text', async () => {
  const { getByTestId, getByText, debug } = render(SplitRange)

  getByText('Train:')
  getByText('Test:')

  /*
  // Get input associated with label.
  const input = getByTestId('split-input')
  // Update the input field.
  const value = 666
  await fireEvent.update(input, value)
  // Assert that the update is successful.
  getByText(value)

  // View the current state of the dom.
  debug()*/
})
