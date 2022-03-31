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

function formatMultipleItems(items) {
  var string = ''
  if (items == null) {
    string = 'NULL'
  } else {
    string = items.map((item) => item.name).join(', ')
  }
  return string
}

function formatResult(result) {
  console.log(result)
  return {
    name: result.metadata.name,
    result: result.result
      .map((combo) =>
        combo.recs.map((rec) => ({
          dataset: combo.dataset.name,
          recommendation: rec.recommendation,
          evaluation: formatMultipleItems(rec.evals), // mock
        }))
      )
      .flat(),
  }
}

export { formatResults, formatResult }
