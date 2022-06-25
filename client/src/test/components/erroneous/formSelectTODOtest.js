/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { render, fireEvent, getByTestId } from '@testing-library/vue'
import { test } from 'vitest'
import TestSelect from '../../mock/TestSelect.vue'

test('test selecting an option', async () => {
  const { getByText, getByDisplayValue } = render(TestSelect)

  getByText('test select')

  const select = getByTestId('select')
  await fireEvent.focus(select)
  await fireEvent.click(select)
  getByDisplayValue('foo')
})
