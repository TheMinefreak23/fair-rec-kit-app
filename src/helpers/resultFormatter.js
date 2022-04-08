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
  console.log(result)
  const formattedResult = {
    name: result.metadata.name,
    result: result.result
      // Make all combination pairs of dataset and approach
      .map((dataset) => ({
        ...dataset,
        recs: dataset.recs.map((rec) => {
          const formatted = {
            approach: rec.approach,
            recommendation:
              // Stub for the format for now
              { user: 'User', item: rec.recommendation, score: 1 },
          }
          // Format evaluation: Use metric as header
          rec.evals.map((e) => {
            formatted[e.name] = e.evaluation
          })
          //console.log(formatted)
          return formatted
        }),
      })),
  }
  //console.log(formattedResult)
  return formattedResult
}

export { formatResults, formatResult }
