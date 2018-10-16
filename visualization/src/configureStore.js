import { createStore, applyMiddleware } from 'redux'

import logger from 'redux-logger'
import thunkMiddleware from 'redux-thunk'

import reducers from './reducers'

// create store based on reducers
export default () => {
  const store = createStore(reducers, applyMiddleware(thunkMiddleware, logger))

  return store
}
