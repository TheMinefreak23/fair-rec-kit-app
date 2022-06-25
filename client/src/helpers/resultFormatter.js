/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import { statusPrefix, status } from './queueFormatter'

export const STANDARD_HEADERS = [
  'track_spotify-uri',
  'track_name',
  'artist_name',
  'artist_mbID',
  'movie_imdbID',
  'movie_title',
  'movie_imdb url',
]

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
      .map((item) => underscoreToSpace(item.name))
      .filter(() => true) // remove empty array slots
      .join(', ')
  }
  return string
}

export function statusVariant(rawStatus) {
  const experimentStatus = rawStatus.slice(statusPrefix.length)
  // console.log('statusVariant experimentStatus', experimentStatus)
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
  // console.log('before format', JSON.parse(JSON.stringify(result)))
  const { rawSettings, ...restSettings } = result.settings
  const formattedResult = {
    id: result.timestamp.stamp,
    metadata: result.metadata,
    experiments: result.experiments,
    settings: restSettings,
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
        // Omit old properties TODO
        // const { recs, ...rest } = datasetResult
        return datasetResult
      }),
  }
  formattedResult.metadata.datetime = result.timestamp.datetime

  // console.log('formatted', formattedResult)
  return formattedResult
}

/**
 * Short result description, e.g. for a result tab
 * @param {Object} result - The result
 * @return {String} - The short description
 */
export function shortResultDescription(result) {
  // console.log(result)
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
function formatEvaluation(e, index, result, runID) {
  // console.log('before evaluation format', JSON.parse(JSON.stringify(e)))

  // Get filtered values and make subheaders
  let subgroupName = ''

  if (e.evaluations[0].subgroup.subset) {
    // console.log('subgroup subset', e.evaluations[0].subgroup.subset)
    for (const filter of e.evaluations[0].subgroup.subset) {
      // console.log('filter', filter)
      for (const filterPass of filter.filter_pass) {
        for (const [paramName, paramValue] of Object.entries(
          filterPass.params
        )) {
          subgroupName +=
            ' ' +
            capitalise(
              underscoreToSpace(filterPass.name) +
                ' ' +
                '(' +
                paramName +
                ' ' +
                paramValue +
                ')'
            )
        }
      }
    }
  } else subgroupName = 'Global'

  result[formatMetricName(e) + subgroupName + '_' + index] = parseFloat(
    e.evaluations[runID].value
  ).toFixed(2)

  // TODO runID shit?
  return { name: formatMetricName(e), subheaders: [subgroupName] }
}

// Format metric name
export function formatMetricName(evaluation) {
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
