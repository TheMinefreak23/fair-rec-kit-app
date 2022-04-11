import words from 'an-array-of-english-words'
import { API_URL } from '../api'
import { store } from '../store'
import {ref} from 'vue'

var metadata = {}
var form = {}

const options = ref()


// GET request: Get available options for selection from server
async function getOptions() {
  const response = await fetch(API_URL + '/computation/options')
  const data = await response.json()
  options.value = data.options
  console.log(options)
}

async function sendMockData() {
  await getOptions()
  form = {
    recommendations: rand(100),
    split: rand(100),
    splitMethod: 'timesplit',
    approaches: generateRandomApproach(),
    metrics: generateRandomMetrics(),
    datasets: generateRandomDatasets(),
    filters: toFormObject(randomWords()),
  }
  console.log(form)
  metadata = {
    name: 'Test' + rand() + ': ' + randomWord(),
    email: randomWord() + '@' + randomWord() + '.com',
    tags: randomWords(),
  }


  //form.approaches = reformat(form.approaches)
  //form.metrics = reformat(form.metrics)
  //form.datasets = reformat(form.datasets)

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ metadata: metadata, settings: form }),
  }
  const response = await fetch(
    API_URL + '/computation/calculation',
    requestOptions
  )
  // Update queue
  const data = response.json()
  store.queue = data
}

function generateRandomApproach() {
  let libraries = options.value.approaches.libraries
  let result = []
  for (let i = 0; i < (1 + Math.floor(Math.random * 3)); i++) {
    approaches = randomItems(randomItems(libraries, 1).options, 1)
    approachName = approaches.name
    choices = approaches.params.options

    randomOption = randomItems(choices, 1)
    randomOptionName = randomOption.map(x => x.text)
    randomOptionValue = randomOption.map(x => randomItems(x.options, 1))

    values = approaches.params.values

    randomValue = randomItems(values, 1)
    randomValuesName = randomValue.map(x => x.text)
    randomValuesValue = randomValue.map(x => (getRandomInt(x.min, x.max)))

    params = [{
      'name': randomOptionName,
      'value': randomOptionValue
    },
    {
      'name': randomValueName,
      'value': randomValueValue
    }]=

    result[i] = {
      'name': approachName,
      'params': params}
  }
  console.log(result)
  return result
}

function generateRandomMetrics(){
  let result = []
  for (let i = 0; i < (1 + Math.floor(Math.random * 3)) ; i++) {
    console.log(options.value.metrics)
    randomOption = randomItems(options.value.metrics.categories, 1)
    randomOptionName = randomOption.text

    result[i] = {
      'name': randomOptionName,
      'params': rand(20)
    }
  }
  console.log(result)
  return result
}

function generateRandomDatasets() {
  let result = []
  for (let i = 0; i < (1 + Math.floor(Math.random * 3)); i++) {

    randomDataset = randomItems(options.value.datasets, 1)
    randomDatasetName = randomDataset.text

    result[i] = {
      'name': randomDatasetName,
      'params': rand(20)
    }
  }
  return result
}

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
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

function randomItems(list, n = Math.floor(Math.random() * list.length)) {
  let set = new Set()
  for (let i = 0; i < n; i++) {
    set.add(list[Math.floor(Math.random() * list.length)])
  }
  if (set.size == 0) {
    return randomItems(list)
  }
  console.log(...set)
  return [...set]
}

function toFormObject(obj) {
  return obj.map((x) => ({
    name: x,
    parameter: null,
  }))
}

function reformat(property) {
  let choices = []
  for (let i in property.main) {
    let parameter = null
    if (property.lists[i] != null) {
      //console.log(property.lists[i])
      choices[i] = {
        name: property.main[i],
        settings: property.lists[i].map((setting) => ({
          [setting.name]: reformat(setting),
        })),
      }
    } else {
      if (property.inputs[i] != null) parameter = property.inputs[i]
      else if (property.selects[i] != null) parameter = property.selects[i]
      choices[i] = { name: property.main[i], parameter: parameter }
      //console.log('choices:' + choices)
    }
  }
  return choices
}

export { sendMockData }
