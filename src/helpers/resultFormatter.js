// Format data for a results overview
function formatResults(allResults) {
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
function formatMultipleItems(items) {
  var string = ''
  if (items == null) {
    string = 'NULL'
  } else {
    string = items.map((item) => item.name).join(', ')
  }
  return string
}

// Format a result for the result tab
function formatResult(result) {
  //console.log(result)
  const formattedResult = {
    id: result.timestamp.stamp,
    name: result.metadata.name,
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
function showDatasetInfo(dataset) {
  return (
    'Dataset: ' +
    dataset.name +
    (dataset.parameter ? 'with parameters' + dataset.parameter : '')
  )
}

// Format evaluations (including filtered ones)
function formatEvaluation(e, result) {
  result[e.name] = e.evaluation.global

  //console.log(e.evaluation.filtered)
  const filtered = e.evaluation.filtered
    .map((filter) => Object.values(filter))
    .flat()
    .flat()
  //console.log(filtered)

  // Get filtered values and make subheaders
  if (filtered.length == 0) {
    return { name: e.name }
  } else {
    const subheaders = ['Global']
    filtered.map((filter) => {
      // Mock: get first entry for now
      const [name, val] = Object.entries(filter)[0]
      //const filterName = e.name + ' ' + name
      const filterName = capitalise(name)
      result[filterName] = val
      subheaders.push(filterName)
      //console.log(subheaders)
    })

    return { name: e.name, subheaders: subheaders }
  }
}

// Make headers from a result
function makeHeaders(result) {
  //console.log(result)
  const headers = Object.keys(result).map((key) => ({
    name: key,
  }))
  //console.log(headers)
  return headers
}

function capitalise(string) {
  return string.charAt(0).toUpperCase() + string.slice(1)
}

function underscoreToSpace(string) {
  return string.replaceAll('_', ' ')
}

export { formatResults, formatResult, capitalise, underscoreToSpace }
