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
          // Use metric names as headers
          result.evals.map((e) => {
            result[e.name] = e.evaluation
          })
          // Omit recommendation
          const { recommendation, evals, ...rest } = result
          return rest
        })
        datasetResult.headers = makeHeaders(datasetResult.results[0])
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

// Make headers from a result
function makeHeaders(result) {
  //console.log(result)
  const headers = Object.keys(result).map((key) => ({
    name: key,
  }))
  //console.log(headers)
  return headers
}

export { formatResults, formatResult }
