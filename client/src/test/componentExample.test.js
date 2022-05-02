import { render, fireEvent } from '@testing-library/vue'
import { test } from 'vitest'
import App from '../App.vue'

test('switchTab', async () => {
  // get utilities to query component
  const { getByText } = render(App)

  // get first node that matches tab text
  const tab = getByText('Documentation')

  await fireEvent.click(tab)

  // throws error if the view that appears on press does not have this text
  getByText('Documentation')
})
