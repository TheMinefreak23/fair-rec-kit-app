import words from 'an-array-of-english-words'
import { API_URL } from '../api'
import { store } from '../store'
import {ref, onMounted} from 'vue'

var metadata = {}
var form = {}


 async function sendMockData(options) {
  console.log(options)
  form = {
    recommendations: rand(100),
    split: rand(100),
    splitMethod: 'timesplit',
    approaches: generateRandomApproach(options),
    metrics: generateRandomMetrics(options),
    datasets: generateRandomDatasets(options),
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

function generateRandomApproach(options) {
  console.log(options)
  let libraries = options.approaches.libraries.prediction
  let result = []
  var n = (1 + Math.floor(Math.random() * 3))
  console.log(n)
  for (let i = 0; i < n; i++) {
    console.log(libraries)
    var ops = randomItems(libraries, 1)[0].options
    console.log(" xd")
    console.log(ops)
    var approach = randomItems(ops, 1)[0]
    console.log(" alsjlfjalsfj")
    console.log(approach)
    var approachName = approach.text
    var choices = approach.params.options

    var randomOptionName = randomWord()
    var randomOptionValue = randomWord()
    console.log("xdsfasf")
    console.log(choices)
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
      'params': params}
  }
  console.log(result)
  return result
}

function generateRandomMetrics(options){
  let result = []
  var n = (1 + Math.floor(Math.random() * 3))
  for (let i = 0; i < n ; i++) {
    console.log(options.metrics)
    randomOption = randomItems(options.metrics.categories, 1)
    randomOptionName = randomOption.text

    result[i] = {
      'name': randomOptionName,
      'params': rand(20)
    }
  }
  console.log(result)
  return result
}

function generateRandomDatasets(options) {
  let result = []
  var n = (1 + Math.floor(Math.random() * 3))
  for (let i = 0; i < n; i++) {
    console.log(options)
    console.log("test1")
    randomDataset = randomItems(options.datasets, 1)
    console.log(randomDataset)
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
  console.log('bingus')
  console.log(list)
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
