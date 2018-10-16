import {
  select,
  zoom, drag, event, max,
  forceSimulation, forceLink, forceManyBody, forceCenter, forceX, forceY
} from 'd3'

// const colorIndex = c => `${c.label}-${c.Subtipo}`
// https://coolors.co/app/41a6c1-ffaf87-ff715b-fff8e8-dc493a
const color = {
  'git.user': '#aaa',
  'git.repo': '#666',
  'twitter.user': '#41a6c1'
}
const r = 8

const ticked = (nodesDom, linksDom) => {
  nodesDom.selectAll('.node')
    .attr('transform', d => `translate(${d.x},${d.y})`)

  linksDom.selectAll('line')
    .attr('x1', d => d.source.x)
    .attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x)
    .attr('y2', d => d.target.y)
}

const handleMouseOver = () => function (d, i) {
  const el = select(this)

  el.raise()

  el.selectAll('circle')
    .attr('r', r * 1.5)

  el.selectAll('g')
    .style('display', null)
    .selectAll('text.textlabel')
    .attr('dx', d => (r * 1.5) + 2)
}

const handleMouseOut = () => function (d, i) {
  const el = select(this)

  el.selectAll('circle')
    .attr('r', r)

  el.selectAll('g')
    .style('display', 'none')
}

class Graph {
  constructor (element) {
    this.width = window.innerWidth - 10
    this.height = window.innerHeight - 10
    this.svg = select(element).append('svg')
      .attr('width', this.width)
      .attr('height', this.height)

    this.g = this.svg.append('g')
    this.linksDom = this.g.append('g').attr('class', 'links')
    this.nodesDom = this.g.append('g').attr('class', 'nodes')
    this.legendDom = this.svg.append('g').attr('class', 'legends')

    this.svg.call(zoom().scaleExtent([-100, 100]).on('zoom', this.rescale.bind(this)))

    this.width = +this.svg.node().getBoundingClientRect().width
    this.height = +this.svg.node().getBoundingClientRect().height

    this.simulation = forceSimulation()
      .force('charge_force', forceManyBody(-1000))
      .force('center_force', forceCenter(this.width / 2, this.height / 2))
      .force('link', forceLink().id(d => d.id).distance(40).strength(0.1))
      .force('x', forceX(this.width / 2).strength(0.02))
      .force('y', forceY(this.height / 2).strength(0.02))
      .alphaTarget(1)
      .on('tick', () => ticked(this.nodesDom, this.linksDom))
  }

  update (nodes, relationships) {
    this.simulation.nodes(nodes)
    this.simulation.force('link').links(relationships)
    this.simulation.alpha(1).restart()

    // add links
    let link = this.linksDom.selectAll('line')
      .data(relationships)

    const allLinks = link
      .enter().append('line')
      .attr('stroke-width', 1)
      .style('stroke', d => color[d.source.label] || 'grey')

    link.exit().remove()

    allLinks.append('title')
      .text(d => d.type)

    // Apply the general update pattern to the nodes.
    let node = this.nodesDom.selectAll('.node').data(nodes)

    const nodeEnter = node.enter()
      .append('g')
      .attr('class', 'node')
      .call(drag()
        .on('start', this.dragstarted.bind(this))
        .on('drag', this.dragged.bind(this))
        .on('end', this.dragended.bind(this)))

    nodeEnter
      .on('mouseover', handleMouseOver())
      .on('mouseout', handleMouseOut())

    nodeEnter.append('circle')
      .attr('r', d => r)
      .attr('fill', d => color[d.label])

    const label = nodeEnter.append('g')
      .attr('class', 'label')
      .style('display', 'none')

    label.append('rect')
      .attr('x', d => 0)
      .attr('y', -15)
      .attr('width', d => (d.name.length * 11) + 2)
      .attr('height', 30)
      .attr('fill', d => color[d.label])

    label.append('text')
      .attr('class', 'textlabel')
      .attr('dx', d => r + 2)
      .attr('dy', '.35em')
      .attr('fill', 'white')
      .text(d => `${d.name}`)

    node = nodeEnter.merge(node)

    node.exit().remove()

    // const legendData = nodes.map(n => n.label).reduce((acc, n) => acc.indexOf(n) < 0 ? [...acc, n] : acc, [])

    // this.legendDom
    //   .attr('transform', `translate(0, ${this.height - (legendData.length * 30) - 40})`)
    //   .append('rect')
    //   .attr('fill', 'white')
    //   .attr('width', max(legendData, l => l.split('-')[1].length) * 12)
    //   .attr('height', legendData.length * 30)
    //
    // const legends = this.legendDom.selectAll('.legend')
    //   .data(legendData)
    //
    // const legendsEnter = legends.enter()
    //   .append('g')
    //   .attr('class', 'legend')
    //   .attr('transform', (l, i) => `translate(0, ${(i * 30) + 10})`)
    //
    // legendsEnter
    //   .append('circle')
    //   .attr('r', 5)
    //   .attr('cx', 10)
    //   .attr('fill', l => this.colors[l])
    //
    // legendsEnter
    //   .append('text')
    //   .attr('x', 20)
    //   .attr('dx', 0)
    //   .attr('dy', '.35em')
    //   .attr('color', l => this.colors[l])
    //   .text(l => l.split('-')[1])
    //
    // legends.exit().remove()
  }

  stopSimulation () {
    this.simulation.stop()
  }

  rescale () {
    this.g.attr('transform', event.transform)
  }

  dragstarted (d) {
    if (!event.active) this.simulation.alphaTarget(0.3).restart()
    d.fx = d.x
    d.fy = d.y
    // this.handleMouseOver(d)
  }

  dragged (d) {
    d.fx = event.x
    d.fy = event.y
  }

  dragended (d) {
    if (!event.active) this.simulation.alphaTarget(0)
    d.fx = null
    d.fy = null
    // this.handleMouseOut(d)
  }
}

export default Graph
