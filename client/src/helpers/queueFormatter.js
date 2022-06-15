/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

// TODO get from server
/**
 * Available types of experiment statuses
 */
export const status = {
  notAvailable: 'Not Available',
  toDo: 'To Do',
  active: 'Active',
  aborted: 'Aborted',
  cancelled: 'Cancelled',
  done: 'Done',
}

// TODO get from server
/**
 * Available types of experiment progress
 */
export const progress = {
  notAvailable: 'Not Available',
  started: 'Started',
  parsing: 'Parsing',
  processingData: 'Processing Data',
  filteringData: 'Filtering Data',
  splittingData: 'Splitting Data',
  model: 'Starting approach',
  modelLoad: 'Loading train set',
  training: 'Training',
  evaluating: 'Evaluating',
  finished: 'Finished',
}

/**
 * The string that comes before each status (prefix)
 */
export const statusPrefix = 'status_' // TODO hacky

/**
 * Get the status display variant from the status name for the queue table
 * @param {String} rawStatus - The status string
 * @return {String} The status variant
 */
export function statusVariant(rawStatus) {
  const experimentStatus = rawStatus.slice(statusPrefix.length)
  //console.log('statusVariant experimentStatus', experimentStatus)
  switch (experimentStatus) {
    case status.toDo:
      return 'outline-warning'
    case status.active:
      return 'success'
    case status.aborted:
      return 'light'
    case status.cancelled:
      return 'light'
    case status.done:
      return 'outline-success'
  }
}
