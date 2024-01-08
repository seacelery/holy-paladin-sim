const createBuffsLineGraph = (data, graphId, title, colour) => {
    const buffCountData = data;
    const buffCountDataArray = Object.keys(buffCountData).map(key => ({ key: +key, value: buffCountData[key] }));

    const margin = { top: 60, right: 20, bottom: 55, left: 65 },
        width = 600 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom;

    const svg = d3.select(graphId)
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

    svg.append("text")
        .attr("x", width / 2)
        .attr("y", -26)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("fill", "white")
        .text(`${title} Count`);

    const x = d3.scaleLinear()
        .domain(d3.extent(buffCountDataArray, d => d.key))
        .range([0, width]);
        
    const y = d3.scaleLinear()
        .domain([0, d3.max(buffCountDataArray, d => d.value)])
        .range([height, 0]);

    const line = d3.line()
        .x(d => x(d.key))
        .y(d => y(d.value))
        .curve(d3.curveMonotoneX);

    svg.append("path")
        .datum(buffCountDataArray)
        .attr("fill", "none")
        .attr("stroke", `${colour}`)
        .attr("stroke-width", 1.5)
        .attr("d", line);

    const xAxisGroup = svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

    xAxisGroup.append("text")
        .attr("class", "axis-label")
        .attr("x", (width / 2) - 10)
        .attr("y", 41)
        .style("text-anchor", "middle")
        .text("Time");

    xAxisGroup.selectAll("line").style("stroke", "white");
    xAxisGroup.selectAll("path").style("stroke", "white");
    xAxisGroup.selectAll("text").style("fill", "white");

    const yAxisGroup = svg.append("g")
        .call(d3.axisLeft(y));

    yAxisGroup.append("text")
        .attr("class", "axis-label")
        .attr("transform", "rotate(-90)")
        .attr("x", -height / 2)
        .attr("y", -35)
        .style("text-anchor", "middle")
        .text("Count");

    yAxisGroup.selectAll("line").style("stroke", "white");
    yAxisGroup.selectAll("path").style("stroke", "white");
    yAxisGroup.selectAll("text").style("fill", "white");

    return svg;
};

export { createBuffsLineGraph };