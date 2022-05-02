import { render, fireEvent, getAllByText} from '@testing-library/vue'
import { test } from 'vitest'
import App from '../App.vue'

test('switchTab', async () => {
  // get utilities to query component
  const { getByText } = render(App)

  // get first node that matches tab text
  const tab = getAllByText("Documentation")[2].parentNode

  await fireEvent.click(tab)

  // throws error if the view that appears on press does not have this text
  getAllByText('Documentation')
})
