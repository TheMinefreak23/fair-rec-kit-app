/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import { statusPrefix, status } from './queueFormatter'

// Format data for a results overview
// TODO refactor so headers are dynamic (no separate case for status header)
export function formatResults(allResults, showStatus) {
  const results = []
  for (const i in allResults) {
    const rawResult = allResults[i]
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
  let string = ''
  if (array == null) {
    string = 'None'
  } else {
    string = array.filter(() => true).join(', ')
  }
  return string
}

// Format an array of named objects into a comma separated string
export function formatMultipleItems(items) {
  let string = ''
  if (items == null) {
    string = 'None'
  } else {
    string = items
      .filter(() => true) // remove empty array slots
      .map((item) => item.name)
      .filter(() => true) // remove empty array slots
      .join(', ')
  }
  return string
}

export function statusVariant(rawStatus) {
  const experimentStatus = rawStatus.slice(statusPrefix.length)
  //console.log('statusVariant experimentStatus', experimentStatus)
  switch (experimentStatus) {
    case status.toDo:
      return 'outline-warning'
    case status.active:
      return 'success'
    case status.aborted:
      return 'secondary'
    case status.cancelled:
      return 'secondary'
    case status.done:
      return 'outline-success'
  }
}

/**
 * Format a result for the result tab
 * @param {Object} result - The unformatted result
 * @return {Object} The formatted result
 */
export function formatResult(result) {
  console.log('before format', JSON.parse(JSON.stringify(result)))
  const formattedResult = {
    id: result.timestamp.stamp,
    metadata: result.metadata,
    result: result.result
      // Format result per dataset
      .map((datasetResult) => {
        datasetResult.results = []
        for (let runID = 0; runID < result.metadata.runs; runID++) {
          // Format result per approach
          datasetResult.results.push(
            datasetResult.recs.map((result) => {
              const headers = [{ name: 'Approach' }]

              // Use metric names as headers
              for (const [index, evaluation] of result.evals.entries()) {
                headers.push(formatEvaluation(evaluation, index, result, runID))
              }

              // Omit recommendation and evals (old properties)
              const { recommendation, evals, ...rest } = result
              datasetResult.headers = headers // TODO headers can be computed in outer loop
              return rest
            })
          )
        }

        // datasetResult.headers = makeHeaders(datasetResult.results[0])
        datasetResult.caption = showDatasetInfo(datasetResult.dataset)
        return datasetResult
      }),
  }
  formattedResult.metadata.datetime = result.timestamp.datetime

  console.log('formatted', formattedResult)
  return formattedResult
}

/**
 * Short result description, e.g. for a result tab
 * @param {Object} result - The result
 * @return {String} - The short description
 */
export function shortResultDescription(result) {
  //console.log(result)
  const datasets = []
  const approaches = []
  for (const datasetResult of result.result) {
    datasets.push(datasetResult.dataset.name)
    for (const rec of datasetResult.recs) {
      approaches.push(rec.approach)
    }
  }
  const datetime = result.metadata.datetime

  function formatNames(list) {
    //console.log(Array.from(new Set(list)))
    const formattedList = []
    for (const name of Array.from(new Set(list))) {
      // Remove index (part after last underscore)
      const lastIndex = name.lastIndexOf('_')
      formattedList.push(name.slice(0, lastIndex))
    }
    return formattedList
  }

  return [datetime, formatNames(datasets), formatNames(approaches)].join(' | ')
}

// Show dataset info as formatted caption
export function showDatasetInfo(dataset) {
  return (
    'Dataset: ' +
    dataset.name +
    (dataset.parameter ? 'with parameters ' + dataset.parameter : '')
  )
}

// Format evaluations (including filtered ones)
export function formatEvaluation(e, index, result, runID) {
  // TODO refactor and/or give option to set decimal precision in UI
  // TODO support several runs
  // Add index for unique metric key
  result[formatMetric(e) + '_' + index] = parseFloat(
    e.evaluations[runID].global
  ).toFixed(2)

  // Flatten filters
  // console.log(e.evaluation, e.evaluation.filtered)
  // Add filter category (main name) to filter parameter name
  // TODO refactor
  const filtered = []
  for (const filter of e.evaluations[0].filtered) {
    // console.log('filter', filter)
    for (const [mainName, params] of Object.entries(filter)) {
      // console.log(mainName, params)
      for (const param of params) {
        for (const [paramName, paramValue] of Object.entries(param)) {
          const filterItem = {}
          // console.log('paramValue', paramValue.toFixed(2))
          filterItem[mainName + ' ' + '(' + paramName + ')'] =
            paramValue.toFixed(2)
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
    .flat() */
  // console.log(filtered)

  // Get filtered values and make subheaders
  if (filtered.length === 0) {
    return { name: formatMetric(e) }
  } else {
    const subheaders = ['Global']
    filtered.map((filter) => {
      // Mock: get first entry for now
      const [name, val] = Object.entries(filter)[0]
      // const filterName = e.name + ' ' + name
      const filterName = formatMetric(e) + name
      result[filterName] = val
      // console.log(result)
      subheaders.push(capitalise(name))
      // console.log(subheaders)
    })

    return { name: formatMetric(e), subheaders }
  }
}

// Format metric name
export function formatMetric(evaluation) {
  // If it is a K metric, replace K with the parameter
  const name = evaluation.name
  if (name.slice(-1).toLowerCase() === 'k') {
    return name.slice(0, -1) + evaluation.params.K
  } else return name
}

/**
 * convert list of header names into supported header format, capitalise and remove underscores
 * @param {string}   header  - the header that needs to be formatted
 * @returns {Object}         - the formatted header inside an object
 */
export function makeHeader(header) {
  return {
    name: underscoreToSpace(capitalise(header.toString())),
  }
}

export function article(word) {
  return ['a', 'i', 'u', 'e', 'o'].includes(word[0]) ? 'an' : 'a'
}

export function capitalise(string) {
  // Convert word to upper if the last word if it's small enough (abbreviation)
  if (string.replace('?', '').length <= 2) {
    return string.toUpperCase()
  }
  const words = string.split(' ')
  if (words.length === 1) {
    return string[0].toUpperCase() + string.slice(1)
  }
  return words.map((word) => capitalise(word)).join(' ')
}

export function underscoreToSpace(string) {
  return string.replaceAll('_', ' ')
}

// export { formatResults, formatResult, capitalise, article, underscoreToSpace }
