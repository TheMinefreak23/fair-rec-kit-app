/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import { switchToTab, tabs } from '../store'
import { capitalise } from '../helpers/resultFormatter'

export function scrollToDocText(text) {
  const formattedText = capitaliseFirst(text)
  const itemWithText = flatTree.find((item) =>
    item.name.includes(formattedText)
  )
  if (itemWithText) {
    // console.log('Found item', itemWithText, 'for text')
    // switch to documentation tab
    switchToTab(tabs.documentation)
    openParents(itemWithText)
    // TODO refactor replace (used in documentation component as well)
    window.location.href =
      '#' + formattedText.replaceAll(' ', '_').replaceAll('@', 'a')
  } else {
    console.log('Documentation item for text', formattedText, 'not found!')
  }
}

function capitaliseFirst(string) {
  const [firstWord, ...rest] = string.split(' ')
  return [capitalise(firstWord), rest].join(' ').trim()
}

export const tree = {
  label: 'Documentation',
  nodes: [
    {
      label: 'FairRecKit',
    },
    {
      label: 'How to use',

      nodes: [
        {
          label: 'New Experiment Tab',
        },

        {
          label: 'Experiment Queue Tab',
        },
        {
          label: 'Results Tab',
        },

        {
          label: 'All Results Tab',
        },
      ],
    },

    {
      label: 'Datasets',
      nodes: [
        {
          label: 'LFM-2B',
        },
        {
          label: 'LFM-1B',
        },
        {
          label: 'LFM-360K',
        },
        {
          label: 'ML-100K',
        },
        {
          label: 'ML-25M',
        },
      ],
    },

    {
      label: 'Recommender approaches',
    },

    {
      label: 'Metrics',
      nodes: [
        {
          label: 'LensKit Metrics',
          nodes: [
            { label: 'HR@K' },
            { label: 'NDCG@K' },
            { label: 'P@K' },
            { label: 'R@K' },
            { label: 'MRR' },
            { label: 'RMSE' },
            { label: 'MAE' },
          ],
        },
        {
          label: 'Rexmex',
          nodes: [
            { label: 'MAPE' },
            { label: 'MSE' },
            { label: 'ItemCoverage' },
            { label: 'UserCoverage' },
          ],
        },
      ],
    },
  ],
}

export const flatTree = flattenTree(tree)

export function flattenTree(tree) {
  return flatten(tree.nodes, [], 0)
}

function flatten(nodes, parents, d) {
  let flattenedTree = []

  for (let i = 0; i < nodes.length; i++) {
    const newtree = nodes[i]
    // console.log(newtree)
    const item = { name: newtree.label, depth: d, parents }
    // console.log(item)
    flattenedTree.push(item)

    if (typeof newtree.nodes === 'undefined') {
    } else {
      const newparents = parents.concat([newtree.label])
      flattenedTree = flattenedTree.concat(
        flatten(newtree.nodes, newparents, d + 1)
      )
    }
  }

  return flattenedTree
}

export function openParents(item) {
  const collapse = document.getElementById(formatId(item.name))
  collapse.classList.add('show')

  for (let i = 0; i < item.parents.length; i++) {
    const c = document.getElementById(formatId(item.parents[i]))
    c.classList.add('show')
  }
}

export function formatId(itemId) {
  return itemId.replaceAll(' ', '_').replaceAll('@', 'a')
}
