/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

// TODO get from server
export const status = {
  toDo: 'To Do',
  active: 'Active',
  aborted: 'Aborted',
  cancelled: 'Cancelled',
  done: 'Done',
}

export const statusPrefix = 'status_' // TODO hacky

// Format data for a results overview
// TODO refactor so headers are dynamic (no separate case for status header)
export function formatResults(allResults, showStatus) {
  const results = []
  for (let i in allResults) {
    const rawResult = allResults[i]
    //console.log('rawResult', rawResult)
    results[i] = {
      id: rawResult.timestamp.stamp,
      datetime: rawResult.timestamp.datetime,
      name: rawResult.metadata.name,
      tags: formatArray(rawResult.metadata.tags),
      dataset: formatMultipleItems(rawResult.settings.datasets),
      approach: formatMultipleItems(rawResult.settings.approaches),
      metric: formatMultipleItems(rawResult.settings.metrics),
    }
    if (showStatus) {
      results[i].status = statusPrefix + rawResult.status
    }
  }
  return results
}

// Format an array of strings into a comma separated string
export function formatArray(array) {
  var string = ''
  if (array == null) {
    string = 'None'
  } else {
    string = array.filter(() => true).join(', ')
  }
  return string
}

// Format an array of named objects into a comma separated string
export function formatMultipleItems(items) {
  //console.log('items before format', items)
  var string = ''
  if (items == null) {
    string = 'None'
  } else {
    string = items
      .filter(() => true) // remove empty array slots
      .map((item) => item.name)
      .filter(() => true) // remove empty array slots
      .join(', ')
  }
  //console.log(items)
  return string
}

export function statusVariant(rawStatus) {
  const experimentStatus = rawStatus.slice(statusPrefix.length)
  //console.log('statusVariant experimentStatus', experimentStatus)
  switch (experimentStatus) {
    case status.toDo:
      return 'warning'
    case status.active:
      return 'danger'
    case status.aborted:
      return 'light'
    case status.cancelled:
      return 'light'
    case status.done:
      return 'primary'
  }
}

// Format a result for the result tab
export function formatResult(result) {
  console.log('before format', JSON.parse(JSON.stringify(result)))
  const formattedResult = {
    id: result.timestamp.stamp,
    metadata: result.metadata,
    result: result.result
      // Format result per dataset
      .map((datasetResult) => {
        datasetResult.results = datasetResult.recs.map((result) => {
          const headers = [{ name: 'Approach' }]

          // Use metric names as headers
          result.evals.map((e) => {
            headers.push(formatEvaluation(e, result))
            //console.log(result)
          })
          // Omit recommendation and evals (old properties)
          const { recommendation, evals, ...rest } = result
          datasetResult.headers = headers // TODO headers can be computed in outer loop
          return rest
        })
        //console.log(datasetResult.results[0])
        //console.log(datasetResult.headers)
        //datasetResult.headers = makeHeaders(datasetResult.results[0])
        datasetResult.caption = showDatasetInfo(datasetResult.dataset)
        return datasetResult
      }),
  }
  formattedResult.metadata.datetime = result.timestamp.datetime

  console.log('formatted', formattedResult)
  return formattedResult
}

/*
// Omit the recommendation key from the result metric table
function omitRecommendation(arr) {
  return arr.map(
    // Omit recommendation
    (r) => ({
      ...r,
      recs: r.recs.map((rec) => {
        const { recommendation, ...rest } = rec
        return rest
      }),
    })
  )
}*/

// Show dataset info as formatted caption
export function showDatasetInfo(dataset) {
  return (
    'Dataset: ' +
    dataset.name +
    (dataset.parameter ? 'with parameters ' + dataset.parameter : '')
  )
}

// Format evaluations (including filtered ones)
export function formatEvaluation(e, result) {
  result[formatMetric(e)] = e.evaluation.global

  // Flatten filters
  console.log(e.evaluation, e.evaluation.filtered)
  // Add filter category (main name) to filter parameter name
  // TODO refactor
  const filtered = []
  for (let filter of e.evaluation.filtered) {
    console.log('filter', filter)
    for (const [mainName, params] of Object.entries(filter)) {
      console.log(mainName, params)
      for (const param of params) {
        for (const [paramName, paramValue] of Object.entries(param)) {
          const filterItem = {}
          console.log('paramValue', paramValue)
          filterItem[mainName + ' ' + '(' + paramName + ')'] = paramValue
          filtered.push(filterItem)
        }
      }
    }
  }
  /*
  const filtered = e.evaluation.filtered
    .map((filter) => Object.entries(filter))
    .map(([mainName, param] => { mainName + } ))
    .flat()
    .flat()*/
  //console.log(filtered)

  // Get filtered values and make subheaders
  if (filtered.length == 0) {
    return { name: formatMetric(e) }
  } else {
    const subheaders = ['Global']
    filtered.map((filter) => {
      // Mock: get first entry for now
      const [name, val] = Object.entries(filter)[0]
      //const filterName = e.name + ' ' + name
      const filterName = e.name + name
      result[filterName] = val
      subheaders.push(capitalise(name))
      //console.log(subheaders)
    })

    return { name: formatMetric(e), subheaders: subheaders }
  }
}

// Format metric name
export function formatMetric(evaluation) {
  // If it is a K metric, replace K with the parameter
  const name = evaluation.name
  if (name.toLowerCase()[name.length - 1] == 'k') {
    //console.log(evaluation)
    // TODO refactor K condition
    return name.slice(0, -1) + evaluation.params['K']
  } else return name
}

export function article(word) {
  return ['a', 'i', 'u', 'e', 'o'].includes(word[0]) ? 'an' : 'a'
}

export function capitalise(string) {
  return string[0].toUpperCase() + string.slice(1)
}

export function underscoreToSpace(string) {
  return string.replaceAll('_', ' ')
}

//export { formatResults, formatResult, capitalise, article, underscoreToSpace }
