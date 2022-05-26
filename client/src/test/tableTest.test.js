import { render, fireEvent } from '@testing-library/vue'
import { test } from 'vitest'
import Table from '../components/Table.vue'

test('deleteTableItem', async () => {
  // get utilities to query component
  const { getByText, getByTitle } = render(Table, {
    props: {
      overview: false,
      results: [{ foo: 1, bar: 1 }],
      headers: [{ name: 'foo' }, { name: 'bar' }],
      buttonText: 'owo',
      removable: true,
    },
  })

  // get deletion button
  const button = getByText('Delete')

  await fireEvent.click(button)

  // check if the modal shows up
  getByTitle('Remove entry?')
})

test('editTableItem', async () => {
  const { getByText, getByTitle } = render(Table, {
    props: {
      overview: true,
      results: [{ foo: 2, bar: 2 }],
      headers: [{ name: 'hello' }, { name: 'world' }],
      buttonText: 'button',
      removable: false,
    },
  })

  const button = getByText('Edit')

  await fireEvent.click(button)

  getByTitle('Editing results')
})

test('userItemTable', async () => {
  const { getByText, getByTitle, getByPlaceholderText } = render(Table, {
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

  getByTitle(/select/)

  const prevbutton = getByText(/previous/)
  const nextbutton = getByText(/next/)
  const headerbutton = getByText('change headers')

  await fireEvent.click(prevbutton)
  await fireEvent.click(nextbutton)
  await fireEvent.click(headerbutton)

  getByPlaceholderText('20')
})

test('viewMetadata', async () => {
  const { getAllByText, getByTitle } = render(Table, {
    props: {
      overview: true,
      results: [{ foo: 3, bar: 3 }],
      headers: [{ name: 'whats' }, { name: 'up' }],
      buttonText:
        'this part doesnt matter so I could put anything here and no-one will ever notice hehehe',
      removable: false,
    },
  })

  const button = getAllByText('View Metadata')[0]

  await fireEvent.click(button)

  // check if the modal shows up
  getByTitle('Metadata')
})
