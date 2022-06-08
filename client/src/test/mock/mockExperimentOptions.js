/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import words from 'an-array-of-english-words'
import { API_URL } from '../../api'
import { getCalculation, pollForResult, store } from '../../store'
import { ref, onMounted } from 'vue'
import mockLists from './mockLists.json'
import mockMetrics from './mockMetrics.json'
import { progress } from '../../helpers/queueFormatter'

let metadata = {}
let form = {}

async function sendMockData(options, simple = false, metrics = false) {
  console.log('options', options)
  form = {
    recommendations: rand(100),
    //split: rand(100),
    //splitMethod: 'timesplit',
    experimentMethod: 'recommendation', // todo random
  }
  if (simple) {
    form.lists = mockLists
  } else {
    form.lists = {
      approaches: generateRandomApproach(options),
      metrics: [], // TODO
      //metrics: generateRandomMetrics(options),
      datasets: generateRandomDatasets(options),
      //filters: toFormObject(randomWords()),
    }
  }
  if (metrics) {
    form.lists.metrics = mockMetrics.metrics
  }
  console.log('form', form)

  metadata = {
    name: 'Test' + rand() + '_' + randomWord(),
    //email: randomWord() + '@' + randomWord() + '.com',
    email: 'rajauitlimburg@hotmail.com',
    tags: randomWords(),
  }

  // TODO get from server?
  store.currentExperiment = {
    metadata: metadata,
    settings: form,
    progress: progress.notAvailable,
  }
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(store.currentExperiment),
  }
  const response = await fetch(API_URL + '/experiment/', requestOptions)
  // Update queue
  const data = await response.json()
  store.queue = data.queue
  console.log('sendToServer() queue', store.queue)
  // Switch to queue
  store.currentTab = 1
  pollForResult()
}

function generateRandomApproach(options) {
  //generate random settings for the Approaches part of a experiment
  console.log(options)
  let libraries = options.predictors
  let result = []
  const n = 1 + Math.floor(Math.random() * 3)

  for (let i = 0; i < n; i++) {
    const ops = randomItems(libraries, 1)[0].options

    const approach = randomItems(ops, 1)[0].value
    console.log('options', ops)

    const approachName = approach.name
    const choices = approach.params.options

    let params = []

    console.log('selects', choices)

    if (Array.isArray(choices) && choices.length) {
      console.log('selects exist', choices)
      const randomOption = randomItems(choices, 1)[0]
      console.log('random option', randomOption)
      const randomOptionName = randomOption.name
      const randomOptionValue = randomItems(randomOption.options, 1)
      params.push({
        name: randomOptionName,
        value: randomOptionValue,
      })
    }

    const values = approach.params.values

    console.log('inputs', values)

    if (Array.isArray(values) && values.length) {
      const randomValue = randomItems(values, 1)[0]
      const randomValuesName = randomValue.name
      const randomValuesValue = getRandomInt(randomValue.min, randomValue.max)
      params.push({
        name: randomValuesName,
        value: randomValuesValue,
      })
    }

    result[i] = {
      name: approachName,
      params: params,
    }
  }

  return result
}

function generateRandomMetrics(options) {
  //generate random settings for the Metrics part of a experiment
  let result = []
  var n = 1 + Math.floor(Math.random() * 3)
  for (let i = 0; i < n; i++) {
    console.log(options.metrics)
    var randomOption = randomItems(options.metrics, 1)[0]
    var randomOptionOptions = randomOption.options
    var randomOptionName = randomItems(randomOptionOptions, 1)[0].name

    result[i] = {
      name: randomOptionName,
      params: rand(20),
    }
  }

  return result
}

function generateRandomDatasets(options) {
  //generate random settings for the Datasets part of a experiment
  let result = []
  const n = 1 + Math.floor(Math.random() * 3)
  for (let i = 0; i < n; i++) {
    console.log(options.datasets)
    const randomDataset = randomItems(options.datasets, 1)[0].value
    console.log('random dataset', randomDataset)

    const randomDatasetParams = {
      name: randomDataset.params.values[0].name,
      value: randomDataset.params.values[0].default,
    }

    // TODO actual random choice, this is just a temp quick fix
    const splitting = randomDataset.params.dynamic[2].options[0].value
    console.log('splitting', splitting)

    // TODO refactor
    const randomMatrix = randomItems(
      randomDataset.params.dynamic[0].options,
      1
    )[0].value
    const matrix = {
      name: randomMatrix.name,
      params: [],
      conversion: [],
    }

    result[i] = {
      name: randomDataset.name,
      params: [randomDatasetParams],
      matrix: [matrix],
      splitting: [
        {
          // TODO actual random choice, this is just a temp quick fix
          name: randomDataset.params.dynamic[2].name,
          params: [
            {
              name: splitting.name,
              value: getRandomInt(
                splitting.params.values[0].min,
                splitting.params.values[0].max
              ),
            },
          ],
        },
      ],
    }
    console.log('dataset', result)
  }
  return result
}

function getRandomInt(min, max) {
  min = Math.ceil(min)
  max = Math.floor(max)
  return Math.floor(Math.random() * (max - min) + min) //The maximum is exclusive and the minimum is inclusive
}

function rand(n = 1000) {
  return Math.floor(Math.random() * n)
}

function randomWord() {
  return words[Math.floor(Math.random() * words.length)]
}

function randomWords() {
  let array = []
  for (let i = 0; i < 5; i++) {
    array[i] = randomWord()
  }
  return array
}

function randomItems(list = [], n = Math.floor(Math.random() * list.length)) {
  //takes a list and a number, selects a random amount of item in that list.

  /*if (list.length == 0) {
    return randomWord()
  }*/
  let set = new Set()
  for (let i = 0; i < n; i++) {
    set.add(list[Math.floor(Math.random() * list.length)])
  }
  if (set.size == 0) {
    return randomItems(list)
  }
  return [...set]
  /*const randomList = []
  for (let i = 0; i < n; i++) {
    randomList.push(list[Math.floor(Math.random() * list.length)])
  }
  return randomList*/
}

export { sendMockData }
