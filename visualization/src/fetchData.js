import fetch from 'cross-fetch'
export const fetchTwitter = () => fetch('twitter.json')
  .then(res => {
    if (res.status >= 400) {
      throw new Error('Bad response from server')
    }
    return res.json()
  })
  .catch(err => {
    console.error(err)
  })
