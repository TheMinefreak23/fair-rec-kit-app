<script>
let tree = {
    label: 'Root',
    nodes: [
        {
            label: 'FairRecKit'
        },
        {
            label: 'New Experiment',
            nodes: [
                {
                    label: 'Datasets',
                    nodes: [
                        {
                            label: 'LFM2B'
                        },
                        {
                            label: 'LFM1B'
                        },
                        {
                            label: 'LFM360K'
                        },
                        {
                            label: 'ML25M'
                        },
                        {
                            label: 'ML100K'
                        }
                    ]
                },
                {
                    label: 'Filters'
                },
                {
                    label: 'Recommender approaches',
                    nodes: [
                        {
                            label: 'Elliot',
                            nodes: [
                                {
                                    label: 'FunkSVD'
                                },
                                {
                                    label: 'ItemKNN'
                                },
                                {
                                    label: 'MultiVAE'
                                },
                                {
                                    label: 'MostPop'
                                }
                            ]
                        },
                        {
                            label: 'Surprise',
                            nodes: [
                                {
                                    label: 'PureSVD'
                                },
                                {
                                    label: 'Random'
                                }
                            ]
                        },
                        {
                            label: 'Implicit',
                            nodes: [
                                {
                                    label: 'AlternatingLeastSquares'
                                },
                                {
                                    label: 'BayesianPersonalizedRanking'
                                },
                                {
                                    label: 'LogisticMatrixFactorization'
                                }
                            ]
                        },
                        {
                            label: 'LensKit',
                            nodes: [
                                {
                                    label: 'BiasedMF'
                                },
                                {
                                    label: 'ImplicitMF'
                                },
                                {
                                    label: 'PopScore'
                                },
                                {
                                    label: 'Ra2ndom'
                                }
                            ]
                        }
                    ]
                },
                {
                    label: 'Metrics',
                    nodes: [
                        {
                            label: 'P@K'
                        },
                        {
                            label: 'R2andom'
                        },{
                            label: 'Random2'
                        }
                    ]
                },
                {
                    label: 'Meta'
                }
            ]
        },
        {
            label: 'Active Experiments'
        },
        {
            label: 'Documentation'
        },
        {
            label: 'Results'
        },
        {
            label: 'All Results'
        }
    ]
}
</script>
