/* This program has been developed by students from the bachelor Computer
Science at Utrecht University within the Software Project course. © Copyright
Utrecht University (Department of Information and Computing Sciences) */

import { render } from '@testing-library/vue'
import { test } from 'vitest'
import SettingsModal from '../../../components/Table/Modals/SettingsModal.vue'

/**
 * Test settings modal
 */
test('invalid result ID', async () => {
  // Render Dictionary Display
  const { getByText } = render(SettingsModal, {
    props: {
      resultId: -1,
    },
  })

  // TODO
})
