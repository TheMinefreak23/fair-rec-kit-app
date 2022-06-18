/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { render } from '@testing-library/vue'
import { test } from 'vitest'
import TestBootstrap from '../mock/TestBootstrap.vue'

/**
 * Test Bootstrap component
 */
test('Test', async () => {
  const { getByText } = render(TestBootstrap)
})
