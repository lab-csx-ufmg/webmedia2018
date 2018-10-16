import Graph from './graph'
import { fetchTwitter } from './fetchData'

const graphDiv = document.createElement('div')
graphDiv.setAttribute('id', 'graph')
document.body.appendChild(graphDiv)

const graph = new Graph(graphDiv)

fetchTwitter()
  .then(data => {
    let edges = []
    data.edges.forEach((e, idx) => {
      data.nodes[e.source].out = (data.nodes[e.source].out || 0) + 1
      data.nodes[e.target].in = (data.nodes[e.target].in || 0) + 1
    })

    data.edges.forEach((e, idx) => {
      edges = [...edges, {
        id: `${e.source}-${e.target}`,
        type: e.type,
        source: e.source,
        target: e.target
      }]
    })

    const nodes = Object.keys(data.nodes).map((k, idx) => {
      const node = data.nodes[k]
      const props = data.nodes[k].properties
      return {
        id: k,
        label: node.label,
        name: props.login || props.full_name || props.screen_name || props.id,
        in: node.in,
        out: node.out
      }
    })

    graph.update(nodes, edges)
    setTimeout(() => graph.stopSimulation(), 3000)
  })
