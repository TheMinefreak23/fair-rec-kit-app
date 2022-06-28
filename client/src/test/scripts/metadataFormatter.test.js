/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { formatMetadata, insert } from '../../helpers/metadataFormatter'

describe('insert', () => {
  test('empty', () => {
    expect(insert('', '', 0)).toBe('')
  })
  test('apple', () => {
    expect(insert('An apple a day doctor away', ' keeps the', 14)).toBe(
      'An apple a day keeps the doctor away'
    )
  })
  test('empty insert', () => {
    expect(insert('yo gabba gabba', '', 5)).toBe('yo gabba gabba')
  })
})

describe('formatMetadata', () => {
  test('empty', () => {
    expect(formatMetadata('')).toBe('')
  })
  test('comma', () => {
    expect(formatMetadata(',')).toBe(',\n')
  })
  test('left brackets', () => {
    expect(formatMetadata('{[')).toBe('{\n\t[\n\t\t')
  })
  test('simple', () => {
    expect(formatMetadata('{}')).toBe('{\n\t\n}')
  })
  test('both brackets', () => {
    expect(formatMetadata('{[{hey}]}')).toBe(
      '{\n\t[\n\t\t{\n\t\t\they\n\t\t}\n\t]\n}'
    )
  })
  test('shortresult', () => {
    expect(
      formatMetadata(
        '{ "metadata": { "email": "not@reale.mail", "name": "funny", "tags": [ "tags, tags, tags," ] }}'
      )
    ).toBe(
      '{\n\t "metadata": {\n\t\t "email": "not@reale.mail",\n\t\t "name": "funny",\n\t\t "tags": [\n\t\t\t "tags,\n\t\t\t tags,\n\t\t\t tags,\n\t\t\t" \n\t\t] \n\t}\n}'
    )
  })
  test('longresult', () => {
    expect(
      formatMetadata(
        '{ "metadata": { "email": "fake@email.gov", "name": "help", "tags": [ "oof" ] }, "result": [ { "dataset": { "name": "ML-100K", "params": [ { "name": "Train/testsplit", "value": "80" } ], "settings": [ { "filters": [] } ] }, "recs": [ { "approach": "BiasedMF", "evals": [ { "evaluation": { "filtered": [], "global": 0.32 }, "name": "RMSE", "params": null } ], "recommendation": "ML-100KFMdesaiB" } ] } ], "settings": { "approaches": [ { "name": "BiasedMF", "params": [ { "name": "features", "value": 10 }, { "name": "iterations", "value": 20 }, { "name": "user_reg", "value": 0.1 }, { "name": "item_reg", "value": 0.1 }, { "name": "damping", "value": 5 }, { "name": "random_seed", "value": null } ] } ], "computationMethod": "recommendation", "datasets": [ { "name": "ML-100K", "params": [ { "name": "Train/testsplit", "value": "80" } ], "settings": [ { "filters": [] } ] } ], "metrics": [ { "name": "RMSE", "params": null, "settings": [ { "filters": [] } ] } ], "recommendations": 10, "split": 80, "splitMethod": "random" }, "timestamp": { "datetime": "2022-05-04 13:18:15", "stamp": "1651663095" } }'
      )
    ).toBe(
      '{\n\t "metadata": {\n\t\t "email": "fake@email.gov",\n\t\t "name": "help",\n\t\t "tags": [\n\t\t\t "oof" \n\t\t] \n\t},\n\t "result": [\n\t\t {\n\t\t\t "dataset": {\n\t\t\t\t "name": "ML-100K",\n\t\t\t\t "params": [\n\t\t\t\t\t {\n\t\t\t\t\t\t "name": "Train/testsplit",\n\t\t\t\t\t\t "value": "80" \n\t\t\t\t\t} \n\t\t\t\t],\n\t\t\t\t "settings": [\n\t\t\t\t\t {\n\t\t\t\t\t\t "filters": [\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t] \n\t\t\t\t\t} \n\t\t\t\t] \n\t\t\t},\n\t\t\t "recs": [\n\t\t\t\t {\n\t\t\t\t\t "approach": "BiasedMF",\n\t\t\t\t\t "evals": [\n\t\t\t\t\t\t {\n\t\t\t\t\t\t\t "evaluation": {\n\t\t\t\t\t\t\t\t "filtered": [\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t],\n\t\t\t\t\t\t\t\t "global": 0.32 \n\t\t\t\t\t\t\t},\n\t\t\t\t\t\t\t "name": "RMSE",\n\t\t\t\t\t\t\t "params": null \n\t\t\t\t\t\t} \n\t\t\t\t\t],\n\t\t\t\t\t "recommendation": "ML-100KFMdesaiB" \n\t\t\t\t} \n\t\t\t] \n\t\t} \n\t],\n\t "settings": {\n\t\t "approaches": [\n\t\t\t {\n\t\t\t\t "name": "BiasedMF",\n\t\t\t\t "params": [\n\t\t\t\t\t {\n\t\t\t\t\t\t "name": "features",\n\t\t\t\t\t\t "value": 10 \n\t\t\t\t\t},\n\t\t\t\t\t {\n\t\t\t\t\t\t "name": "iterations",\n\t\t\t\t\t\t "value": 20 \n\t\t\t\t\t},\n\t\t\t\t\t {\n\t\t\t\t\t\t "name": "user_reg",\n\t\t\t\t\t\t "value": 0.1 \n\t\t\t\t\t},\n\t\t\t\t\t {\n\t\t\t\t\t\t "name": "item_reg",\n\t\t\t\t\t\t "value": 0.1 \n\t\t\t\t\t},\n\t\t\t\t\t {\n\t\t\t\t\t\t "name": "damping",\n\t\t\t\t\t\t "value": 5 \n\t\t\t\t\t},\n\t\t\t\t\t {\n\t\t\t\t\t\t "name": "random_seed",\n\t\t\t\t\t\t "value": null \n\t\t\t\t\t} \n\t\t\t\t] \n\t\t\t} \n\t\t],\n\t\t "computationMethod": "recommendation",\n\t\t "datasets": [\n\t\t\t {\n\t\t\t\t "name": "ML-100K",\n\t\t\t\t "params": [\n\t\t\t\t\t {\n\t\t\t\t\t\t "name": "Train/testsplit",\n\t\t\t\t\t\t "value": "80" \n\t\t\t\t\t} \n\t\t\t\t],\n\t\t\t\t "settings": [\n\t\t\t\t\t {\n\t\t\t\t\t\t "filters": [\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t] \n\t\t\t\t\t} \n\t\t\t\t] \n\t\t\t} \n\t\t],\n\t\t "metrics": [\n\t\t\t {\n\t\t\t\t "name": "RMSE",\n\t\t\t\t "params": null,\n\t\t\t\t "settings": [\n\t\t\t\t\t {\n\t\t\t\t\t\t "filters": [\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t] \n\t\t\t\t\t} \n\t\t\t\t] \n\t\t\t} \n\t\t],\n\t\t "recommendations": 10,\n\t\t "split": 80,\n\t\t "splitMethod": "random" \n\t},\n\t "timestamp": {\n\t\t "datetime": "2022-05-04 13:18:15",\n\t\t "stamp": "1651663095" \n\t} \n}'
    )
  })
})
