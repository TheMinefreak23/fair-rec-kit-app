<script>
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
                                    label: 'ML100K'
                                },
                                {
                                    label: 'ML25M'
                                }
                            ]
                        },
                        {
                            label: 'Recommender approaches'
                        },
                        {
                            label: 'Metrics',
                            nodes: [
                                {
                                    label: 'LensKit Metrics',
                                    nodes: [
                                        { label: 'HR@K' },
                                        { label: 'NDCG@K'},
                                        { label: 'P@K' },
                                        { label: 'R@K' },
                                        { label: 'MRR' },
                                        { label: 'RMSE' },
                                        { label: 'MAE' }
                                    ]
                                },
                                {
                                    label: 'Rexmex',
                                    nodes: [
                                        {label: 'MAPE'},
                                        {label: 'MSE'},
                                        {label: 'ItemCoverage'},
                                        {label: 'UserCoverage'}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            label: 'Experiment Queue'
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
