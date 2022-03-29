function formatResults(allResults) {
  const results = []
  for (let i in allResults) {
    results[i] = {
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

export { formatResults }
