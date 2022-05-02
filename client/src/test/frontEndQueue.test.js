import { render, fireEvent, waitFor } from '@testing-library/vue'
import { expect, test} from 'vitest'
import App from '../App.vue'
import { sendMockData } from './mockComputationOptions.js'
import { API_URL } from '../api'


test('testQueue', async () => {
    var queueLength1
    await waitFor(() => fetch(API_URL + '/computation/queue')).then(response => queueLength1 = response.json().length)

    sendMockData()

    var queueLength2
    await waitFor(() => fetch(API_URL + '/computation/queue')).then(response => queueLength2 = response.json().length)

    expect(queueLength2 - queueLength1).toBe(1)
})
