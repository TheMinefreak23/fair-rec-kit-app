/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { render, fireEvent, getByTestId, getByText } from '@testing-library/vue'
import { describe, expect, it, test } from 'vitest'
import Table from '../../../components/Table.vue'
import HeadersModal from '../../../components/Table/Modals/HeadersModal.vue'
import DeletionModal from '../../../components/Table/Modals/DeletionModal.vue'
import EditModal from '../../../components/Table/Modals/EditModal.vue'
import InfoModal from '../../../components/Table/Modals/InfoModal.vue'

test('Filter button', async () => {
  const { getByText, getByTitle } = render(Table, {
    props: {
      expendable: true,
      results: [{ foo: 1, bar: 1 }],
      headers: [{ name: 'foo' }, { name: 'bar' }],
    },
  })

  const button = getByText('Filters')
  await fireEvent.click(button)
  getByTitle('Change filters')
})

test('Header button', async () => {
  const { getByText, getByTitle } = render(HeadersModal, {
    props: {
      headerOptions: true,
    },
  })

  const button = getByText('Select Headers')
  await fireEvent.click(button)
  getByText('Select the extra headers you want to be shown')
})

test('deleteTableItem', async () => {
  // get utilities to query component
  const { getByTestId, getByTitle } = render(DeletionModal, {
    props: {
      entry: true,
    },
  })

  // get deletion button
  const button = getByTestId('delete')

  await fireEvent.click(button)

  // check if the modal shows up
  getByTitle('Remove entry?')
})

test('editTableItem', async () => {
  const { getByTestId, getByTitle } = render(EditModal)

  const button = getByTestId('edit')
  await fireEvent.click(button)
  getByTitle('Editing results')
})

test('userItemTable', async () => {
  const { getByText, getByTitle } = render(Table, {
    props: {
      caption: 'testcaption',
      results: [{ foo: 2, bar: 2 }],
      headers: [{ name: 'hello' }, { name: 'world' }],
      headerOptions: [{ name: 'hello' }, { name: 'world' }],
      userOptions: [{ name: 'hello' }, { name: 'world' }],
      itemOptions: [{ name: 'hello' }, { name: 'world' }],
      pagination: true,
      expandable: true,
    },
  })

  //getByTitle(/select/)

  const prevbutton = getByText(/previous/i)
  const nextbutton = getByText(/next/i)
  const headerbutton = getByText('Select Headers', { exact: false })

  await fireEvent.click(prevbutton)
  await fireEvent.click(nextbutton)
  await fireEvent.click(headerbutton)

  getByText('20')
})

test('viewMetadata', async () => {
  const { getByTestId, getByTitle } = render(InfoModal)

  const button = getByTestId('view-meta')

  await fireEvent.click(button)

  // check if the modal shows up
  getByTitle('Result information')
})
