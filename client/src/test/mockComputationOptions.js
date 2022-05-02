import words from 'an-array-of-english-words'
import { API_URL } from '../api'
import { store } from '../store'
import {ref, onMounted} from 'vue'

var metadata = {}
var form = {}


 async function sendMockData(options) {
  form = {
    recommendations: rand(100),
    split: rand(100),
    splitMethod: 'timesplit',
    approaches: generateRandomApproach(options),
    metrics: generateRandomMetrics(options),
    datasets: generateRandomDatasets(options),
    filters: toFormObject(randomWords()),
  }

  metadata = {
    name: 'Test' + rand() + ': ' + randomWord(),
    email: randomWord() + '@' + randomWord() + '.com',
    tags: randomWords(),
  }

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

function generateRandomApproach(options) {
  //generate random settings for the Approaches part of a computation
  let libraries = options.approaches.libraries.prediction
  let result = []
  var n = (1 + Math.floor(Math.random() * 3))

  for (let i = 0; i < n; i++) {
    var ops = randomItems(libraries, 1)[0].options

    var approach = randomItems(ops, 1)[0]

    var approachName = approach.text
    var choices = approach.params.options

    var randomOptionName = randomWord()
    var randomOptionValue = randomWord()
    if(choices != (undefined || [])){
      var randomOption = randomItems(choices, 1)[0]
      randomOptionName = randomOption.text
      randomOptionValue = randomItems(randomOption.options, 1)
    }

    var values = approach.params.values

    var randomValuesName = randomWord()
    var randomValuesValue = rand()
    if (values != (undefined || []))
    {
      var randomValue = randomItems(values, 1)[0]
      randomValuesName = randomValue.text
      randomValuesValue = (getRandomInt(randomValue.min, randomValue.max))
    }


    var params = [{
      'name': randomOptionName,
      'value': randomOptionValue
    },
    {
      'name': randomValuesName,
      'value': randomValuesValue
    }]

    result[i] = {
      'name': approachName,
      'settings': params}
  }

  return result
}

function generateRandomMetrics(options){
  //generate random settings for the Metrics part of a computation
  let result = []
  var n = (1 + Math.floor(Math.random() * 3))
  for (let i = 0; i < n ; i++) {
    console.log(options.metrics)
    var randomOption = randomItems(options.metrics.categories, 1)[0]
    var randomOptionOptions = randomOption.options
    var randomOptionName = randomItems(randomOptionOptions,1)[0].text

    result[i] = {
      'name': randomOptionName,
      'settings': rand(20)
    }
  }

  return result
}

function generateRandomDatasets(options) {
  //generate random settings for the Datasets part of a computation
  let result = []
  var n = (1 + Math.floor(Math.random() * 3))
  for (let i = 0; i < n; i++) {
    console.log(options.datasets)
    var randomDataset = randomItems(options.datasets, 1)[0]

    var randomDatasetName = randomDataset.text
    var randomDatasetParams = {'name' : randomDataset.params.values[0].text,
      'value': randomDataset.params.values[0].default}

    result[i] = {
      'name': randomDatasetName,
      'settings': randomDatasetParams
    }
    console.log(result)
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

function randomItems(list = [], n = Math.floor(Math.random() * list.length)) {
  //takes a list and a number, selects a random amount of item in that list.

  if (list.length == 0){
    return randomWord()
  }
  let set = new Set()
  for (let i = 0; i < n; i++) {
    set.add(list[Math.floor(Math.random() * list.length)])
  }
  if (set.size == 0) {
    return randomItems(list)
  }
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
    }
  }
  return choices
}

export { sendMockData }
