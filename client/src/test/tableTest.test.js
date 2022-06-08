/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { render, fireEvent, getByTestId } from '@testing-library/vue'
import { expect, it, test } from 'vitest'
import Table from '../components/Table.vue'

test('deleteTableItem', async () => {
  // get utilities to query component
  const { getByTestId, getByTitle } = render(Table, {
    props: {
      overview: false,
      results: [{ foo: 1, bar: 1 }],
      headers: [{ name: 'foo' }, { name: 'bar' }],
      buttonText: 'owo',
      removable: true,
    },
  })

  // get deletion button
  const button = getByTestId('delete')

  await fireEvent.click(button)

  // check if the modal shows up
  getByTitle('Remove entry?')
})

test('editTableItem', async () => {
  const { getByTestId, getByTitle } = render(Table, {
    props: {
      overview: true,
      results: [{ foo: 2, bar: 2 }],
      headers: [{ name: 'hello' }, { name: 'world' }],
      buttonText: 'button',
      removable: false,
    },
  })

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
  const headerbutton = getByText('change headers', { exact: false })

  await fireEvent.click(prevbutton)
  await fireEvent.click(nextbutton)
  await fireEvent.click(headerbutton)

  getByText('20')
})

test('viewMetadata', async () => {
  const { getByTestId, getByTitle } = render(Table, {
    props: {
      overview: true,
      results: [{ foo: 3, bar: 3 }],
      headers: [{ name: 'whats' }, { name: 'up' }],
      buttonText:
        'this part doesnt matter so I could put anything here and no-one will ever notice hehehe',
      removable: false,
    },
  })

  const button = getByTestId('view-meta')

  await fireEvent.click(button)

  // check if the modal shows up
  getByTitle('Result information')
})
