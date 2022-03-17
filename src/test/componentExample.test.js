import { render, fireEvent } from '@testing-library/vue'
import { test } from 'vitest'
import Playground from '../components/Playground.vue'

test('collapse', async () => {
  // get utilities to query component
  const { getByText } = render(Playground)

  // get first node that matches button text
  const button = getByText('Toggle collapse')

  await fireEvent.click(button)

  // throws error if the button response is not this text
  getByText('RecCoons')
})
