/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { render, fireEvent, getByTestId } from '@testing-library/vue'
import { test } from 'vitest'
import App from '../App.vue'

test('switchTab', async () => {
  // get utilities to query component
  const { getAllByText } = render(App)

  const tab = getAllByText('Active Computations')[2]

  await fireEvent.click(tab)

  // throws error if the view that appears on press does not have this text
  getAllByText('Queue')
})
