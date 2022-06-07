/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { render, fireEvent, within } from '@testing-library/vue'
import { expect, test } from 'vitest'
import { NewExperiment } from '../components/NewExperiment.vue'

const property = {
    "visible": true,
    "groupCount": 1,
    "choices": [
        {
            "main": {
                "name": "Random",
                "params": {
                    "options": [],
                    "values": [
                        {
                            "default": null,
                            "max": 9223372036854776000,
                            "min": 0,
                            "name": "seed"
                        }
                    ]
                }
            },
            "inputs": [
                {
                    "name": "seed",
                    "value": null
                }
            ]
        }
    ]
}

test('', async () => {
    // Render NewExperiment
    const {
        getAllByText,
        getAllByTestId,
        getByTestId,
        getByLabelText,
        getByDisplayValue,
      } = render(NewExperiment, {})
    
  })
 
/**
 *Test reformatting of the selection fields
 */
// describe('reformatting', () => {
//   //
//   test('empty', () => {
//     expect(NewExperiment.reformat({})).toBe([])
//   })
//   test('not empty', () => {
//     expect(NewExperiment.reformat(property).length == property.choices.length).toBe(true)
//   })
//   test('correct format', () => {
//     expect(NewExperiment.reformat(property).name).toBe(property.choices.main.name)
//   })
// })
