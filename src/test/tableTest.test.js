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
  const {getByText, getByTitle} = render(Table, {
    props: {
      overview: true,
      results: [{foo: 2, bar: 2}],
      headers: [{ name: 'hello'}, { name: 'world'}],
      buttonText: 'button',
      removable: false,
    },
  })

  const button = getByText('Edit')

  await fireEvent.click(button)

  getByTitle('Editing results')
})

// test('viewResult', async () => {
//   const {getByText, getByTitle} = render(Table, {
//     props: {
//       overview: true,
//       results: [{foo: 3, bar: 3}],
//       headers: [{ name: 'whats'}, { name: 'up'}],
//       buttonText: 'button',
//       removable: false,
//     },
//   })

//   const button = getByText('View result')

//   await fireEvent.click(button)


// })
