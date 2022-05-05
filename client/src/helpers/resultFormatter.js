/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

// Format data for a results overview
export function formatResults(allResults) {
  const results = []
  for (let i in allResults) {
    results[i] = {
      id: allResults[i].timestamp.stamp,
      datetime: allResults[i].timestamp.datetime,
      name: allResults[i].metadata.name,
      dataset: formatMultipleItems(allResults[i].settings.datasets),
      approach: formatMultipleItems(allResults[i].settings.approaches),
      metric: formatMultipleItems(allResults[i].settings.metrics),
    }
  }
  return results
}

// Format an array of named objects into a comma separated string
export function formatMultipleItems(items) {
  var string = ''
  if (items == null) {
    string = 'None'
  } else {
    string = items
      .map((item) => item.name)
      .filter(() => true) // remove empty array slots
      .join(', ')
  }
  //console.log(items)
  return string
}

// Format a result for the result tab
export function formatResult(result) {
  console.log(result)
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

  //console.log(formattedResult)
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
  const filtered = e.evaluation.filtered
    .map((filter) => Object.values(filter))
    .flat()
    .flat()
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
    return name.slice(0, -1) + evaluation.params[0].value
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
